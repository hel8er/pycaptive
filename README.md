# Authentication Page for FreeRadius
Build on python FastAPI

### Quick start
```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```
edit .env with your FreeRadius secret

```bash
uvicorn app:app
```

Access page on 127.0.0.1:8000
