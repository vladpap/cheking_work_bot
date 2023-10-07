import logging
import textwrap
import time
from datetime import datetime

import requests
from environs import Env
from telegram import ParseMode
from telegram.ext import Updater


log = logging.getLogger('checking_work_bot')


class TelegramLogHandler(logging.Handler):
    def __init__(self, tg_token, tg_chat_id):
        super().__init__()
        self.tg_token = tg_token
        self.tg_chat_id = tg_chat_id

    def emit(self, record):
        log_record = self.format(record)
        self.tg_token.send_message(chat_id=self.tg_chat_id, text=log_record)


def main():

    env = Env()
    env.read_env(override=True)

    devman_api_token = env.str('DEVMAN_API_TOKEN')
    tg_token = env.str('TG_TOKEN')
    tg_chat_id = env.int('TG_CHAT_ID')

    log.addHandler(
        TelegramLogHandler(tg_token=tg_token, tg_chat_id=tg_chat_id))
    log.setLevel(logging.INFO)
    log.info("Starting bot")

    time_wait_long_polling = 10
    time_wait_without_connection = 90

    updater = Updater(tg_token)

    long_polling_url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {devman_api_token}'}

    timestamp = datetime.now().timestamp()

    while True:
        params = {'timestamp': timestamp}
        try:
            response = requests.get(long_polling_url,
                                    headers=headers,
                                    timeout=time_wait_long_polling,
                                    params=params)
            response.raise_for_status()

        except requests.exceptions.ReadTimeout:
            continue

        except requests.exceptions.ConnectionError as connect_err:
            log.error(connect_err, exc_info=True)
            log.error('Problem connection.')
            time.sleep(time_wait_without_connection)
            continue

        except Exception as err:
            logging.exception(err)
            continue

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

            updater.bot.send_message(chat_id=tg_chat_id,
                                     text=textwrap.dedent(text_message),
                                     parse_mode=ParseMode.HTML)

        timestamp = checked_works['last_attempt_timestamp']


if __name__ == '__main__':
    main()
