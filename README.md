
## Gefest PRO (backend)
### Документация OpenAPI

```
  GET /docs
```
### Учетные данные администратора

| Логин     | Пароль  |
| :-------- | :-------|
| `admin`   | `admin` |

### Инструкция по развертыванию

Предварительно, для развертывания сервиса необходимо установить 
dokku на сервер:
```bash
wget -NP . https://dokku.com/install/v0.30.5/bootstrap.sh
sudo DOKKU_TAG=v0.30.5 bash bootstrap.sh
```
Далее, необходимо настроить окружение dokku.
1. Добавить ключи:
```bash
cat ~/.ssh/authorized_keys | dokku ssh-keys:add admin
```
2. Установить плагин для PostgreSQL:
```bash
sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git
```
3. Создать контейнер PostgreSQL:
```bash
dokku postgres:create gefest-back-db
```
4. Создать приложение dokku:
```bash
dokku apps:create gefest-back
```
5. Подключить контейнер PostgreSQL к созданному приложению:
```bash
dokku postgres:link gefest-back-db gefest-back
```
6. Подключить к приложению IP-адрес или домен:
```bash
dokku domains:set gefest-back <ip-address>
```
```bash
dokku domains:set gefest-back <domain-name>
```
7. Для подключения к бд извне пробросить порт:
```bash
dokku postgres:expose 5050
```
8. Для работы по HTTPS установить плагин letsencrypt:
```bash
dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
```
9. Установить адрес почты:
```bash
dokku letsencrypt:set gefest-back email <email-address>
```
10. Включить HTTPS для приложения:
```bash
dokku letsencrypt:enable gefest-back
```
После выполнения всех вышеописанных действий, необходимо подключить репозиторий приложения dokku к локальному репозиторию:
```bash
git remote add dokku <ip-address>:<app-name>
```
и запушить изменения:
```bash
git push dokku main(master)
```
### Дополнительные настройки
Для взаимодействия с фронтэндом необходимо изменить настройки CORS в файле */src/main.py*:
```code
app.add_middleware(
        CORSMiddleware,
        allow_origins=['https://gefest-pro.tech', 'http://127.0.0.1:5501', 'http://localhost:3000'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
```
При такой настройке разрешаются запросы ТОЛЬКО от:
- https://gefest-pro.tech
- http://127.0.0.1:5501
- http://localhost:3000
