# python-project

一个使用 uv 管理依赖、通过本机 Ollama 调用 Qwen 判断钓鱼邮件的 Python 项目。

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

程序默认分析完整的 `data/raw/train.csv`。该文件未上传到 GitHub，下载或克隆代码后，需要先从原电脑复制到这个位置。仓库包含 `train2.csv`（100 条记录），可以用 `--input` 指定它进行小规模试跑。

```bash
git clone https://github.com/LeoCa2026/python-project.git
cd python-project
uv sync --locked
uv run --locked python-project
```

运行前保持 Ollama 运行，并安装 `qwen3:1.7b`。程序默认使用这个模型，读取 `data/raw/train.csv`，逐条显示识别进度，将结果保存到 `outputs/train_results.json`，并生成易读的 `outputs/train_results.md` 报告。

也可以按模块运行：

```bash
uv run --locked python -m python_project
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
├── data/
│   └── raw/
│       ├── .gitkeep
│       ├── README.txt
│       ├── train1.csv
│       ├── train2.csv
│       ├── validation.csv
│       └── test.csv
├── src/
│   └── python_project/
│       ├── __init__.py
│       ├── detector.py
│       └── __main__.py
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

在 `src/python_project/` 中添加项目代码，使用 `uv add` 管理依赖。
详细说明见 [uv 项目指南](https://docs.astral.sh/uv/guides/projects/)。

## 数据集

数据放在项目根目录下的 `data/raw/`。仓库已包含：

- `train1.csv`（前 10 条训练集记录）
- `train2.csv`（前 100 条训练集记录，可指定用于试跑）
- `validation.csv`
- `test.csv`
- `README.txt`（数据集说明）

完整的 `train.csv` 是程序的默认输入，仅保留在本地，未上传到 GitHub。运行默认命令前请将它放入 `data/raw/`。

`.gitkeep` 用于让 Git 保留目录，不影响数据读取。
保留原始数据；后续处理后的数据可另存到 `data/processed/`。

## 本地邮件识别试跑

`detector.py` 只把 `email_text` 发给本机模型；`label` 只用于核对结果。模型输出判断（0=正常，1=钓鱼）、中文理由和原文引用。程序检查引用是否逐字出现在输入邮件中，这项检查不代表证据一定能支持判断。

默认运行：

```powershell
uv run --locked python-project
```

也可以指定输入、输出和模型，用 100 条数据进行试跑：

```powershell
uv run --locked python-project --input data/raw/train2.csv --output outputs/train2_results.json --model qwen3:1.7b
```

结果每处理完一条就保存一次。请求或解析失败会明确记录为错误，不能当作正常邮件。当前本地的 `train2.csv` 保留前 100 条训练集数据，用于试跑，不代表正式测试效果。

## 在安装 4B Instruct 模型的新电脑上运行

先把完整版 `train.csv` 放入 `data/raw/`，并保持本机 Ollama 运行。进入包含 `pyproject.toml` 的项目目录后执行：

```powershell
uv sync --locked
uv run --locked python-project --model qwen3:4b-instruct-2507-q4_K_M
```

程序通过 `http://localhost:11434` 连接当前电脑上的 Ollama。`--model` 会覆盖默认的 `qwen3:1.7b`，指定的模型必须已安装在当前电脑上。

当前请求等待超时仍为 180 秒，上下文容量仍为 4096 token；较长邮件可能超过容量限制。单条请求失败会记录错误并继续处理下一条。程序再次运行会从第一条开始，覆盖指定位置的旧结果；如需保留旧结果，可用 `--output` 指定新的文件名。
