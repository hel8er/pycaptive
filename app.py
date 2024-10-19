import os
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pyrad.client import Client
from pyrad.dictionary import Dictionary
from pyrad.packet import AccessRequest, AccessAccept, AccessReject
from starlette.requests import Request
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Настройки RADIUS сервера
RADIUS_SERVER = os.getenv('RADIUS_SERVER')  # IP адрес RADIUS сервера из переменной окружения
RADIUS_SECRET = os.getenv('RADIUS_SECRET').encode()  # Секретный ключ из переменной окружения
RADIUS_PORT = int(os.getenv('RADIUS_PORT', 1812))  # Порт для аутентификации из переменной окружения

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
            return {"message": "Аутентификация успешна!"}
        else:
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

