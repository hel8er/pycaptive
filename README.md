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
User=your_username  # Replace with the username under which the application will run
Group=your_group     # Replace with the group to which the user belongs
WorkingDirectory=/path/to/your/app  # Replace with the path to your application's directory
Environment="PATH=/path/to/your/venv/bin"  # Replace with the path to your virtual environment, if you are using one
ExecStart=/path/to/your/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000  # Replace with the path to uvicorn and your application name
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
