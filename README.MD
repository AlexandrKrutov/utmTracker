# Установка на сервере
>По хорошему ставить на чистый Ubuntu

docker compose содержит 2 сервиса: nginx и django-app. В prod файле добавлен еще certbot, для получения бесплатного ssl сертификата на 3 месяца.

##### Список файлов:
1. docker-compose.dev.yml - Описание контейнеров для develpment сборки
2. docker-compose.prod.yml - Описание контейнеров для production сборки
3. Dockerfile - Файл, исполняющийся во время билда контейнера с веб приложением
4. entrypoint.sh - Файл, исполняющийся во время запуска контейнера с веб приложением
5. docker/nginx - Указаны конфигурации для nginx сервера для prod/dev версии
### 1. Создание пользователя
Создаем юзера
```
sudo adduser {username}
```
Даём sudo привелегии

```
sudo usermod -aG sudo {username}
```
### 2. Устанавливаем Docker ([Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/))

Удаление, если он уже установлен
```
sudo apt-get remove docker docker-engine docker.io containerd runc
```
Устанавливаем
```
sudo apt-get update

sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

sudo mkdir -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```
Проверяем версию
```
docker -v
```
### 3. Установка docker-compose ([How To Install and Use Docker Compose on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04))

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

docker-compose --version
```

### 4. Важно, добавляем пользователя в группу Docker

```
sudo usermod -aG docker {username}
```
Перезаходим за пользователя, если права были применены на текущего

### 5. Запуск проекта

Клонируем репозиторий, переходим в папку с файлами docker-compose. Далее необходимо создать файл с переменными окружения

```
nano .env
```
Добавляем необоходимые переменные со своими данными
```
EMAIL=email@email.ru
DOMAIN=testdomain.ru
```
Минимальный набор для получения сертификата
> Если запускать контейнер с Windows, то так же нужно создать этот файл

Изменим права на файл entrypoint.sh
```
chmod +x entrypoint.sh
```

Делаем билд (один раз)
```
docker-compose -f docker-compose.dev.yml build
```
После успешной сборки, запускать его следующей командой
```
docker-compose -f docker-compose.dev.yml up
```

### Запуск в прод с бесплатным сертификатом

Билд делать с помощью команды
```
docker-compose -f docker-compose.prod.yml build
```
Запуск
```
docker-compose -f docker-compose.prod.yml up
```
Обновление сертификата
```
docker-compose -f docker-compose.prod.yml certbot renew
```

## Возможные проблемы

Может быть занят порт 80, если на Ubuntu уже установлен веб сервер nginx, можем отключить его следующей командой, но лучше удалить полностью
```
sudo service nginx stop
```

Для корректной работы Docker, нужно поменять тип перевода строк в файлах на LF.
Если выбран CRLF, нужно менять во всех файлах, связанных с докером, на LF