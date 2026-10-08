# python-project

一个使用 uv 管理 Python 版本、虚拟环境和依赖的基础项目。

## 安装 uv

Windows PowerShell：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS / Linux：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

安装后重新打开终端，并运行 `uv --version` 检查。

官方文档：[安装 uv](https://docs.astral.sh/uv/getting-started/installation/)。

## 快速开始

```bash
git clone https://github.com/LeoCa2026/python-project.git
cd python-project
uv sync --locked
uv run --locked python-project --name Leo
```

预期输出：`Hello, Leo!`

也可以按模块运行：

```bash
uv run --locked python -m python_project --name Leo
```

项目默认使用 Python 3.11.17，由 `.python-version` 指定；缺少合适的 Python 时，uv 会自动下载。
`uv sync` 会创建 `.venv` 并安装项目，无需手动激活虚拟环境。

## 管理依赖

添加运行依赖（示例）：

```bash
uv add requests
```

添加开发依赖（示例）：

```bash
uv add --dev pytest
```

移除依赖：

```bash
uv remove requests
```

更新指定依赖：

```bash
uv lock --upgrade-package requests
uv sync --locked
```

添加或更新依赖后，将 `pyproject.toml` 和 `uv.lock` 一起提交。
`uv.lock` 由 uv 自动生成和维护，请勿手动编辑；`.venv` 不提交到 Git。

## 构建项目

```bash
uv build
```

构建文件输出到 `dist/`。

## 项目结构

```text
python-project/
├── src/
│   └── python_project/
│       ├── __init__.py
│       └── __main__.py
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

在 `src/python_project/` 中添加项目代码，使用 `uv add` 管理依赖。
详细说明见 [uv 项目指南](https://docs.astral.sh/uv/guides/projects/)。
