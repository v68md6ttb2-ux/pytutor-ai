"""Recheck unchanged diagnosis components; no database, execution, or LLM calls.

Usage: python evidence/recheck_components.py [--repo PATH]
The logger shim only removes the optional structured-logging dependency.
Regex matching is compiled from the original function's AST, not rewritten.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
import platform
import re
import subprocess
import sys
import types
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class QuietLogger:
    def __getattr__(self, name):
        return lambda *args, **kwargs: None


def scores(rows, clean):
    per_class = {}
    for label in [f"M{i}" for i in range(1, 9)]:
        tp = sum(r["predicted"] == label and r["expected"] == label for r in rows)
        fp = sum(r["predicted"] == label and r["expected"] != label for r in rows)
        fn = sum(r["predicted"] != label and r["expected"] == label for r in rows)
        precision = tp / (tp + fp) if tp + fp else 0
        recall = tp / (tp + fn) if tp + fn else 0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
        per_class[label] = dict(tp=tp, fp=fp, fn=fn, precision=precision, recall=recall, f1=f1)
    return {
        "correct": sum(r["predicted"] == r["expected"] for r in rows),
        "total": len(rows),
        "exact_match": sum(r["predicted"] == r["expected"] for r in rows) / len(rows),
        "macro_f1": sum(r["f1"] for r in per_class.values()) / 8,
        "clean_false_positives": sum(r["predicted"] is not None for r in clean),
        "clean_total": len(clean),
        "per_class": per_class,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2] / "pytutor_latest_20261101")
    args = parser.parse_args()
    repo = args.repo.resolve()
    app = repo / "backend/app"
    for name, path in [("app", app), ("app.analysis", app / "analysis"), ("app.observability", app / "observability")]:
        package = types.ModuleType(name)
        package.__path__ = [str(path)]
        sys.modules[name] = package
    shim = types.ModuleType("app.observability.logger")
    shim.get_logger = lambda *args, **kwargs: QuietLogger()
    sys.modules[shim.__name__] = shim
    load("app.analysis.ast_visitors", app / "analysis/ast_visitors.py")
    analyzer = load("app.analysis.ast_analyzer", app / "analysis/ast_analyzer.py")
    confidence = load("thesis_confidence", app / "analysis/confidence.py")
    service = app / "services/misconception_service.py"
    tree = ast.parse(service.read_text(encoding="utf-8"))
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_rule_match")
    scope = {"re": re}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), str(service), "exec"), scope)
    catalogue = json.loads((app / "data/misconceptions.json").read_text(encoding="utf-8"))

    def predict(case, mode):
        code, stderr = case["code"], case.get("stderr", "")
        if mode == "regex":
            # All native regex candidates receive 0.85; max() returns the first.
            found = next((m["code"] for m in catalogue if scope["_rule_match"](code, stderr, m)), None)
        else:
            question = case.get("student_question", "") if mode == "ast" else ""
            findings = analyzer.analyze_misconceptions(code, stderr, question)
            found = findings[0]["misconception_id"] if findings else None
        return {"case_id": case["case_id"], "expected": case.get("expected_misconception"), "predicted": found}

    result = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "commit": subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip(),
        "protocol": "Native source; inert logging shim; no service/DB/LLM; existing question field supplied only to AST as supported by its interface; regex receives native code+stderr input.",
        "datasets": {},
        "results": {},
    }
    for name, positives, clean_name in [("development", "v2_test_cases.json", "clean_code_cases.json"), ("holdout", "v2_holdout_cases.json", "holdout_clean_cases.json")]:
        cases = json.loads((repo / "evaluation" / positives).read_text(encoding="utf-8"))
        clean_cases = json.loads((repo / "evaluation" / clean_name).read_text(encoding="utf-8"))
        for filename in [positives, clean_name]:
            data = (repo / "evaluation" / filename).read_bytes()
            result["datasets"][filename] = {"sha256": hashlib.sha256(data).hexdigest()}
        result["datasets"][positives]["class_counts"] = dict(Counter(c["expected_misconception"] for c in cases))
        result["results"][name] = {}
        for mode in ["regex", "ast_code_stderr", "ast"]:
            rows = [predict(c, mode) for c in cases]
            clean = [predict(c, mode) for c in clean_cases]
            result["results"][name][mode] = {"summary": scores(rows, clean), "predictions": rows, "clean_predictions": clean}
        # Verify the historical AST primary labels, including each failed case.
        historical = json.loads((repo / "evaluation" / ("v2_eval_results.json" if name == "development" else "v2_holdout_results.json")).read_text(encoding="utf-8"))
        expected = {r["case_id"]: r["predicted"] for r in historical["results"]}
        actual = {r["case_id"]: r["predicted"] for r in result["results"][name]["ast"]["predictions"]}
        assert expected == actual, (name, expected, actual)
    example = analyzer.analyze_misconceptions("items = [1, 2]\nnew = items.append(5)\nprint(new)")
    assert example[0]["misconception_id"] == "M3"
    assert confidence.from_visitor_finding(example[0], stderr="").confidence == 0.575
    result["m3_example"] = {"primary": example[0], "score": 0.575}
    output = Path(__file__).with_name("component_recheck.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    for name, modes in result["results"].items():
        for mode, values in modes.items():
            s = values["summary"]
            print(name, mode, f"{s['correct']}/{s['total']}", f"macro-F1={s['macro_f1']:.3f}", f"clean FP={s['clean_false_positives']}/{s['clean_total']}")
    print("Historical AST predictions reproduced; M3 example checked.")


if __name__ == "__main__":
    main()
