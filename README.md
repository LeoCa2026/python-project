# python-project

一个基础 Python 项目，使用 `src` 目录组织代码，包含可直接运行的命令行示例。

## 环境要求

Python 3.11 或更高版本。

## 快速开始

```bash
git clone https://github.com/LeoCa2026/python-project.git
cd python-project
python -m venv .venv
```

激活虚拟环境：

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS / Linux：

```bash
source .venv/bin/activate
```

安装项目：

```bash
python -m pip install -e .
```

运行示例：

```bash
python -m python_project
python -m python_project --name Leo
```

也可以使用安装后的命令：

```bash
python-project --name Leo
```

预期输出：`Hello, Leo!`

## 项目结构

```text
python-project/
├── src/
│   └── python_project/
│       ├── __init__.py
│       └── __main__.py
├── .gitignore
├── pyproject.toml
└── README.md
```

在 `src/python_project/` 中添加项目代码，在 `pyproject.toml` 的 `dependencies` 中声明运行依赖。
