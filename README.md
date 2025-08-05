# ライブチャット API

## 開発準備

```powershell
> poetry --version
Poetry (version 2.1.1)
```

```powershell
> pyenv --version
pyenv 3.1.1
```

```powershell
> poetry new livechatapi --name app
> cd .\livechatapi
```

```powershell
> pyenv install 3.13.2
> pyenv local 3.13.2
> python -V
Python 3.13.2
```

```powershell
> poetry env use C:\Users\[user]\.pyenv\pyenv-win\versions\3.13.2\python.exe
> .\.venv\Scripts\activate
> deactivate
```

```powershell
> poetry add fastapi
> poetry add requests
> poetry add types-requests
> poetry add uvicorn
> poetry add python-dotenv
> poetry add pydantic
```

## 実行

```powershell
> uvicorn app.main:app --reload
```
