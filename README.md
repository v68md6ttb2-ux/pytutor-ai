# PyTutor — AI Python 编程智能导师

> 本科毕业设计（FYP）项目：基于 Agentic RAG、AST 误区诊断与安全代码执行沙箱的 Python 编程智能导师平台。

PyTutor 面向 Python 零基础/初学者，提供：

- 基于知识库检索（RAG）的自然语言问答与概念讲解
- 统一沙箱边界内的学生代码运行与判题
- AST 结构分析 + 规则诊断 8 类典型初学者误区（M1–M8）
- 按教学策略与渐进提示等级给出提示，而非直接给答案
- 学习画像（薄弱点、误区历史、提示依赖）与下一步推荐
- 教师端班级误区排行、薄弱点排行与提示依赖分布

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Next.js 16 + React 19 + TypeScript + Zustand + Monaco 编辑器 |
| 后端 | FastAPI + Python 3.12 + SQLAlchemy 2.0（async） |
| AI | DeepSeek（OpenAI 兼容）+ DashScope `text-embedding-v3` |
| 检索 | ChromaDB 向量检索 + TF-IDF 关键词检索，可降级 |
| 数据库 | SQLite（开发）/ PostgreSQL（生产）；Alembic 迁移 |
| 部署 | 本地/Docker Compose；Render + Vercel（聊天/RAG） |

## 仓库结构

```
.
├── pytutor-ai-main/pytutor-ai-main/   # 项目源代码、文档与评测
│   ├── backend/                       # FastAPI 后端
│   ├── frontend/                      # Next.js 前端
│   ├── evaluation/                    # 评测数据与脚本
│   ├── research/                      # 研究实验
│   └── docs/                          # 设计与部署文档
├── thesis/                            # 毕业论文终稿、Word/LaTeX 源码与 evidence
├── FYP文献/                            # 毕业论文、文献综述与研究资料
└── PyTutorFYP.pptx                    # 答辩演示文稿
```

## 最终报告

- [main.pdf](thesis/main.pdf) — LaTeX 终稿 PDF（推荐提交版）
- [PyTutor_Final_Report.docx](thesis/PyTutor_Final_Report.docx) — Word 版
- [thesis/](thesis/) — LaTeX/Word 源码、图表与 evidence

## 快速开始

安装、配置与运行说明见 [项目 README](pytutor-ai-main/pytutor-ai-main/README.md)。

> 生产环境运行学生代码需要 Docker；环境变量请参考
> `pytutor-ai-main/pytutor-ai-main/backend/.env.example`，不要提交真实密钥。
