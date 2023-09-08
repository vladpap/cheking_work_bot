import time
from datetime import datetime

from environs import Env

import requests

import textwrap

from telegram import ParseMode
from telegram.ext import Updater


def main():
    env = Env()
    env.read_env(override=True)

    DEVMAN_API_TOKEN = env.str('DEVMAN_API_TOKEN')
    TG_TOKEN = env.str('TG_TOKEN')
    TG_CHAT_ID = env.int('TG_CHAT_ID')

    time_wait_long_polling = 10
    time_wait_without_connection = 90

    updater = Updater(TG_TOKEN)

    long_polling_url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {DEVMAN_API_TOKEN}'}

    timestamp = datetime.now().timestamp()

    while True:
        params = {'timestamp': timestamp}
        try:
            response = requests.get(long_polling_url,
                                    headers=headers,
                                    timeout=time_wait_long_polling,
                                    params=params)
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(time_wait_without_connection)
            continue

        response.raise_for_status()
        checked_works = response.json()
        if checked_works['status'] == 'timeout':
            timestamp = checked_works['timestamp_to_request']
            continue

        for checked_work in checked_works['new_attempts']:
            if checked_work['is_negative']:
                lesson_link = checked_work['lesson_url']
                summary_of_teacher = f'''
                К сожалению, в работе есть ошибки.

                <a href="{lesson_link}">Ссылка на урок</a>'''

            else:
                summary_of_teacher = '''
                Преподавателю все понравилось,
                можно приступать к следующему уроку.'''

            text_message = f'''
                У вас проверили работу
                <b>{checked_work["lesson_title"]}</b>


                {summary_of_teacher}'''

            updater.bot.send_message(chat_id=TG_CHAT_ID,
                                     text=textwrap.dedent(text_message),
                                     parse_mode=ParseMode.HTML)
            print(textwrap.dedent(text_message))
        timestamp = checked_works['last_attempt_timestamp']


if __name__ == '__main__':
    main()
