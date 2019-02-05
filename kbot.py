# -*- coding: utf-8 -*-
from datetime import datetime
print('[' + datetime.now().strftime("%H:%M:%S") + '] Запуск KBot v4.0.')
print('[' + datetime.now().strftime("%H:%M:%S") + '] Инициализация ...')
print('[' + datetime.now().strftime("%H:%M:%S") + '] Загружаю библиотеки ...')
import threading
import requests
import os
import json
import time
import kbotlib
import sys
import queue
kbotlib.log_print('Бибилотеки загружены.', 'info')
sys.dont_write_bytecode = True

updates_queue = queue.LifoQueue()

def longpollserver():
    def get_lp_server():
        lp_info = 'https://api.vk.com/method/messages.getLongPollServer?lp_version=3&v=5.68&access_token='+str(kbotlib.KBot().SETTINGS['TOKEN'])
        lp_info = requests.get(lp_info)
        lp_info = json.loads(lp_info.text)['response']
        kbotlib.log_print('Новая информация о longpoll сервере успешно получена','info')
        return lp_info

    lp_info = get_lp_server()
    while True:
        time.sleep(10 / 1000000.0)
        lp_url = 'https://' + lp_info['server'] + '?act=a_check&key=' + lp_info['key'] + '&ts=' + \
                 str(lp_info['ts']) + '&wait=60&mode=2&version=3'
        result = json.loads(requests.get(lp_url).text)
        try:
            lp_info['ts'] = result['ts']
            for update in result['updates']:
                updates_queue.put(update)
        except KeyError:
            lp_info = get_lp_server()


if __name__ == '__main__':
    kbotlib.log_print('Подключение плагинов ...', 'info')
    import plugins
    plugins.load()
    kbotlib.log_print('Плагины подключены.', 'info')

    kbotlib.log_print('Запуск longpoll потока ...', 'info')
    thread_longpoll = threading.Thread(target=longpollserver)
    thread_longpoll.start()
    kbotlib.log_print('Longpoll поток запущен.', 'info')

    kbotlib.log_print('Инициализация завершена.', 'info')
    try:
        while True:
            time.sleep(10/1000000.0)
            if not updates_queue.empty():
                update = updates_queue.get()

                if update[0] == 4:
                    task = threading.Thread(target=kbotlib.KBot().onMessage.fire, args=(update,))
                    task.setName(str(update[1]))
                    task.start()
    except KeyboardInterrupt:
        kbotlib.log_print('Получен сигнал завершения. Завершаю работу!', 'info')
        os._exit(0)

# Выбрать объявлять ли вручную в плагине или автоматически
# http://www.apmath.spbu.ru/ru/education/aspirantura/quest/05-13-11.html
