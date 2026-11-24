# PyTutor-AI — Final Year Project Report

**Team 10**

- Chen Letian (2330026013)
- Zeng Qikai (2330013039)
- Lian Youbo (2330026086)

Supervisor: Professor Ji Chunyan  
Date: 21 November 2026

**Title:** PyTutor-AI: Design and Evaluation of a Misconception-Aware Python Tutoring System

## Deliverables

| File | Description |
|------|-------------|
| `main.pdf` | LaTeX-compiled final report (37 pages); recommended submission PDF |
| `PyTutor_Final_Report.docx` | Word version using the school template; TOC updates automatically |
| `PyTutor_Final_Report_word.pdf` | PDF exported from the Word version (32 pages) |

## Source

| Path | Contents |
|------|----------|
| `main.tex` | LaTeX entry point, template layout, fonts and heading styles |
| `sections/` | Abstract, introduction, literature review, method, experiments, conclusion, front matter and appendices |
| `references.bib` | Bibliography (12 entries, all cited in the text) |
| `figures/` | Standalone TikZ figures, exported PNGs and `figure_map.json` |
| `word_front.md`, `word_body.md`, `word_full.md` | Markdown sources used to build the Word version |
| `media/` | Images referenced by the Word Markdown |
| `evidence/` | Component recheck script, validation JSON, reference checks, historical experiment artefacts |
| `FYP-1 Projects 20XX.docx` | School report template |

## Build

LaTeX (XeLaTeX, Times New Roman):

```bash
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

Word: `word_full.md` is converted with Pandoc using `FYP-1 Projects 20XX.docx` as the reference document, then the school margins/fonts and table/figure layout are applied. The Word TOC is a field; after edits, right-click it and choose **Update Field**.

## Notes

- The primary submission version is `main.pdf`; the Word version is provided for editing and template compliance.
- All reported numbers, tables, figures, equations and citations are retained in both versions.
- The evaluation data are project-authored and single-author; the report states this limitation explicitly.
