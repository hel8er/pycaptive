from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pyrad.client import Client
from pyrad.dictionary import Dictionary
from pyrad.packet import AccessRequest, AccessAccept, AccessReject
from starlette.requests import Request

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Настройки RADIUS сервера
RADIUS_SERVER = '127.0.0.1'  # IP адрес RADIUS сервера
RADIUS_SECRET = b'testing123'  # Секретный ключ
RADIUS_PORT = 1812  # Порт для аутентификации (по умолчанию 1812)

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/auth")
async def authenticate(username: str = Form(...), password: str = Form(...)):
    # Создаем клиента RADIUS, используя словарь атрибутов
    client = Client(server=RADIUS_SERVER, secret=RADIUS_SECRET, dict=Dictionary("./dictionary"))
    client.authport = RADIUS_PORT

    # Создаем запрос Access-Request
    req = client.CreateAuthPacket(code=AccessRequest, User_Name=username)
    req["User-Password"] = req.PwCrypt(password)

    # Отправляем запрос и получаем ответ
    try:
        reply = client.SendPacket(req)

        # Проверяем код ответа сервера
        if reply.code == AccessAccept:
            return {"message": "Access granted"}
        elif reply.code == AccessReject:
            raise HTTPException(status_code=403, detail="Access denied")
        else:
            raise HTTPException(status_code=500, detail=f"Unknown reply code: {reply.code}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to authenticate: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

