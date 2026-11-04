# projeto-a3-ibmr-2026

## Instalação no Replit/Linux

O projeto utiliza um ambiente virtual local em `.venv`, gerenciado pelo `uv`.

### Criar o ambiente Python

```bash
export UV_PYTHON_DOWNLOADS=manual
export UV_PYTHON_PREFERENCE=only-managed
uv python install 3.13.16
rm -rf .venv
uv venv --python 3.13.16 .venv
```

### Instalar as dependências

```bash
uv pip install --python .venv/bin/python -r requirements.txt
```

### Verificar a instalação

```bash
./.venv/bin/python --version
./.venv/bin/python -c "import flask, flask_sqlalchemy, bcrypt; print('Dependencias OK')"
```

O resultado esperado para a versão do Python é `Python 3.13.16`.

### Executar o projeto

```bash
uv run --python .venv/bin/python python run.py
```

Alternativamente:

```bash
./.venv/bin/python run.py
```