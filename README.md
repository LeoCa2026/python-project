# python-project

һ��ʹ�� uv ����������ͨ������ Ollama ���� Qwen �жϵ����ʼ��� Python ��Ŀ��

## ��װ uv

Windows PowerShell��

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS / Linux��

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

��װ�����´��նˣ������� `uv --version` ��顣

�ٷ��ĵ���[��װ uv](https://docs.astral.sh/uv/getting-started/installation/)��

## ���ٿ�ʼ

���ش�����Ƚ��������� `train2.csv` ���� `data/raw/`�������ļ�����׼��������ֿ�Ŀǰֻ�и�Ŀ¼��ռλ�ļ���

```bash
git clone https://github.com/LeoCa2026/python-project.git
cd python-project
uv sync --locked
uv run --locked python-project
```

����ǰ���� Ollama ���У�����װ `qwen3:1.7b`������Ĭ��ʹ�����ģ�ͣ���ȡ `data/raw/train2.csv`��������ʾʶ����ȣ���������浽 `outputs/train2_results.json`���������׶��� `outputs/train2_results.md` ���档

Ҳ���԰�ģ�����У�

```bash
uv run --locked python -m python_project
```

��ĿĬ��ʹ�� Python 3.11.17���� `.python-version` ָ����ȱ�ٺ��ʵ� Python ʱ��uv ���Զ����ء�
`uv sync` �ᴴ�� `.venv` ����װ��Ŀ�������ֶ��������⻷����

## ��������

��������������ʾ������

```bash
uv add requests
```

���ӿ���������ʾ������

```bash
uv add --dev pytest
```

�Ƴ�������

```bash
uv remove requests
```

����ָ��������

```bash
uv lock --upgrade-package requests
uv sync --locked
```

���ӻ���������󣬽� `pyproject.toml` �� `uv.lock` һ���ύ��
`uv.lock` �� uv �Զ����ɺ�ά���������ֶ��༭��`.venv` ���ύ�� Git��

## ������Ŀ

```bash
uv build
```

�����ļ������ `dist/`��

## ��Ŀ�ṹ

```text
python-project/
������ data/
��   ������ raw/
��       ������ .gitkeep
������ src/
��   ������ python_project/
��       ������ __init__.py
��       ������ detector.py
��       ������ __main__.py
������ .gitignore
������ .python-version
������ pyproject.toml
������ uv.lock
������ README.md
```

�� `src/python_project/` ��������Ŀ���룬ʹ�� `uv add` ����������
��ϸ˵���� [uv ��Ŀָ��](https://docs.astral.sh/uv/guides/projects/)��

## ���ݼ�

ԭʼ���ݷ�����Ŀ��Ŀ¼�µ� `data/raw/`���뽫���ݼ��е������ļ��ϴ������Ŀ¼��

- `train.csv`
- `validation.csv`
- `test.csv`
- `README.txt`�����ݼ�˵����

`.gitkeep` ������ Git ����Ŀ¼����Ӱ�����ݶ�ȡ��
����ԭʼ���ݣ���������������ݿ����浽 `data/processed/`��

## �����ʼ�ʶ������

`detector.py` ֻ�� `email_text` ��������ģ�ͣ�`label` ֻ���ں˶Խ����ģ������жϣ�0=������1=���㣩���������ɺ�ԭ�����á������������Ƿ����ֳ����������ʼ��У������鲻����֤��һ����֧���жϡ�

Ĭ�����У�

```powershell
uv run --locked python-project
```

Ҳ����ָ�����롢�����ģ�ͣ�

```powershell
uv run --locked python-project --input data/raw/train2.csv --output outputs/train2_results.json --model qwen3:1.7b
```

���ÿ������һ���ͱ���һ�Ρ���������ʧ�ܻ���ȷ��¼Ϊ���󣬲��ܵ��������ʼ�����ǰ���ص� `train2.csv` ����ǰ 100 ��ѵ�������ݣ��������ܣ���������ʽ����Ч����

## �ڰ�װ 4B Instruct ģ�͵��µ���������

�������ļ��źã������ֱ��� Ollama ���С�������� `pyproject.toml` ����ĿĿ¼��ִ�У�

```powershell
uv sync --locked
uv run --locked python-project --model qwen3:4b-instruct-2507-q4_K_M
```

����ͨ�� `http://localhost:11434` ���ӵ�ǰ�����ϵ� Ollama��`--model` �Ḳ��Ĭ�ϵ� `qwen3:1.7b`��ָ����ģ�ͱ����Ѱ�װ�ڵ�ǰ�����ϡ�

��ǰ����ȴ���ʱ��Ϊ 180 �룬������������Ϊ 4096 token���ϳ��ʼ����ܳ����������ơ���������ʧ�ܻ��¼���󲢼���������һ���������ٴ����л�ӵ�һ����ʼ������ָ��λ�õľɽ�������豣���ɽ�������� `--output` ָ���µ��ļ�����
