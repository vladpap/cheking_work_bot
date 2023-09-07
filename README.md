![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

# Бот уведомления о проверке работ

Телеграм бот уведомлений о статусе проверки работ на девмане. 

## Установка.
- Python3 должен быть уже установлен.
- Рекомендуется использовать среду окружения [venv](https://docs.python.org/3/library/venv.html) 
для изоляции проекта.
 - Используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей
```console
$ pip install -r requirements.txt
```

### Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env`  запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

- `DEVMAN_API_TOKEN` - ваш персональный токен API Девмана
- `BOT_TOKEN` - ключ телеграм бота
- `CHAT_ID` - ваш chat_idю Чтобы получить свой chat_id, напишите в Telegram специальному боту: [@userinfobot](@userinfobot)

Пример файла `.env`
```console
DEVMAN_API_TOKEN=09845986af64e6751206d26faadc5d147d5fab
BOT_TOKEN=95132391:wP3db3301vnrob33BZdb33KwP3db3F1I
CHAT_ID=9954393459
```

## Запуск

```console
$ python3 check_work_bot.py
```

## Цели проекта

Код написан в учебных целях — это командный проект на курсе по Python [Devman](https://dvmn.org).


<img src="https://dvmn.org/assets/img/logo.8d8f24edbb5f.svg" alt= “” width="102" height="25">