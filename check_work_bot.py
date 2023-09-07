import time
from datetime import datetime

from environs import Env

import requests

from telegram import ParseMode
from telegram.ext import Updater


def main():
    env = Env()
    env.read_env(override=True)

    DEVMAN_API_TOKEN = env.str('DEVMAN_API_TOKEN')
    TG_TOKEN = env.str('TG_TOKEN')
    TG_CHAT_ID = env.int('TG_CHAT_ID')

    TIME_WAIT_LONG_POLLiNG = 10
    TIME_WAIT_WITHOUT_CONNECTION = 90

    updater = Updater(TG_TOKEN)

    long_polling_url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {DEVMAN_API_TOKEN}'}

    timestamp = datetime.now().timestamp()

    while True:
        params = {'timestamp': timestamp}
        try:
            response = requests.get(long_polling_url,
                                    headers=headers,
                                    timeout=TIME_WAIT_LONG_POLLiNG,
                                    params=params)
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(TIME_WAIT_WITHOUT_CONNECTION)
            continue

        response_check_works = response.json()
        for attempt in response_check_works['new_attempts']:
            if attempt['is_negative']:
                lesson_link = attempt['lesson_url']
                summary_of_teacher = 'К сожалению, в работе есть ошибки.'\
                    f'\n <a href="{lesson_link}">Ссылка на урок</a>'
            else:
                summary_of_teacher = 'Преподавателю все понравилось,'\
                    'можно приступать к следующему уроку.'
            text_message = 'У вас проверили работу <b>'\
                f'"{attempt["lesson_title"]}"</b>'\
                f'\n\n {summary_of_teacher}'
            updater.bot.send_message(chat_id=TG_CHAT_ID,
                                     text=text_message,
                                     parse_mode=ParseMode.HTML)

        timestamp = response_check_works['last_attempt_timestamp']


if __name__ == '__main__':
    main()
