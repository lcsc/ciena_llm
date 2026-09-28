# Installing the project locally
```bash
python3 -m venv --upgrade-deps .venv
. .venv/bin/activate
pip install --user poetry
poetry self update
deactivate
. .venv/bin/activate
poetry install 
```
> if poetry/pip hangs while installing dependencies, try without password back end
`export PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring`

## 