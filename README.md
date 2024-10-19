# Authentication Page for FreeRadius
Build on python FastAPI

## Quick start
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

## systemd unit
```
sudo vi /etc/systemd/system/pycaptive.service
```


```
[Unit]
Description=Captive Page
After=network.target

[Service]
User=your_username  # Замените на имя пользователя, под которым будет запускаться приложение
Group=your_group     # Замените на группу, к которой принадлежит пользователь
WorkingDirectory=/path/to/your/app  # Замените на путь к директории вашего приложения
Environment="PATH=/path/to/your/venv/bin"  # Замените на путь к вашему виртуальному окружению, если используете его
ExecStart=/path/to/your/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000  # Замените на путь к uvicorn и имя вашего приложения
Restart=always

[Install]
WantedBy=multi-user.target
```

```
sudo systemctl daemon-reload  # Перезагрузите конфигурацию systemd
sudo systemctl start pycaptive.service  # Запустите службу
sudo systemctl enable pycaptive.service  # Включите автозапуск при загрузке
sudo systemctl status pycaptive.service
journalctl -u pycaptive -f
```

## Troubleshooting

Test your FreeRadius connection with `radtest <username> <password> <radiusip> <radiusport> <radiussecret>`

Example:
```bash
radtest bob hello 127.0.0.1 1812 testing123
```
