# Authentication Page for FreeRadius
Build on python FastAPI

### Quick start
```bash
git clone https://github.com/hel8er/pycaptive.git
cd pycaptive
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```
edit `.env` file with your FreeRadius secret

```bash
uvicorn app:app
```

Access page on http://127.0.0.1:8000

### Troubleshooting

Test your FreeRadius connection with `radtest <username? <password> <radiusip> <radiusport> <radiussecret>`

Example:
```bash
radtest bob hello 127.0.0.1 1812 testing123
```
