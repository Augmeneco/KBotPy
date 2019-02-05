import subprocess
from io import StringIO
import contextlib
import plugins.kbchatbot.kbcblib as kbcblib
import kbotlib
import requests
import sys
import os
import json
import psutil

class KBotAdminCommand(kbcblib.KBCBCmd):
    name = 'Админ команды КБота'

    description = 'Админ команды КБота'

    privileges = 8

    commands = ['адм', 'adm']

    help = 'выход / exit - выключение бота\n' \
           'терм / term <команда> - выполнить команду в терминале\n' \
           'вып / exec <код> - выполнить код Python\n' \
           'стат / stat - Стаистика бота и системы'

    def handler(self, msg):
        if (msg.pretty_text[2] == 'выход') or (msg.pretty_text[2] == 'exit'):
            kbotlib.log_print('(CmdID: ' + str(msg.id) + ') Команда вызвала завершение программы.', 'info')
            param = (('v', '5.68'), ('peer_id', msg.chat_id), ('access_token', kbotlib.KBot.SETTINGS['TOKEN']),
                     ('message', 'Выключаюсь!'), ('forward_messages', msg.id))
            requests.post('https://api.vk.com/method/messages.send', param)
            os._exit(0)

        elif (msg.pretty_text[2] == 'терм') or (msg.pretty_text[2] == 'term'):
            text = subprocess.run(msg.text.split(' ', 3)[3], shell=True, stdout=subprocess.PIPE)

            text = text.stdout.decode('utf-8').replace(' ', '&#8196;').replace('    ', '&#8195;')

            param = (('v', '5.68'), ('peer_id', msg.chat_id), ('access_token', kbotlib.KBot.SETTINGS['TOKEN']),
                     ('message', text), ('forward_messages', msg.id))
            requests.post('https://api.vk.com/method/messages.send', param)

        elif (msg.pretty_text[2] == 'вып') or (msg.pretty_text[2] == 'exec'):
            code = msg.text.split(' ', 3)[3]

            @contextlib.contextmanager
            def stdoutIO(stdout=None):
                old = sys.stdout
                if stdout is None:
                    stdout = StringIO()
                sys.stdout = stdout
                yield stdout
                sys.stdout = old

            with stdoutIO() as s:
                exec(code)

            text = s.getvalue().replace(' ', '&#160;').replace('    ', '&#8195;')

            param = (('v', '5.68'), ('peer_id', msg.chat_id), ('access_token', kbotlib.KBot.SETTINGS['TOKEN']),
                     ('message', text), ('forward_messages', msg.id))
            requests.post('https://api.vk.com/method/messages.send', param)

        elif (msg.pretty_text[2] == 'стат') or (msg.pretty_text[2] == 'stat'):
            with open('./plugins/kbchatbot/statistics.json', 'r+') as f:
                stats = json.loads(f.read())

            text = '[ Статистика ]\n' \
                   'Cреднее время ответа: '+str(stats['mid'])[:4]+' сек.\n' \
                   'Вызовы:\n' \
                   '&#8195;За всё время: '+str(stats['calls']['alltime'])+'\n' \
                   '&#8195;За день: '+str(stats['calls']['day']['count'])+'\n' \
                   'Система:\n' \
                   '&#8195;Процессор:\n'
            for idx, cpu in enumerate(psutil.cpu_percent(interval=1, percpu=True)):
                text += '&#8195;&#8195;Ядро №'+str(idx+1)+': '+str(cpu)+'%\n'

            mem = psutil.virtual_memory()
            MB = 1024 * 1024
            text += '&#8195;ОЗУ:\n' \
                    '&#8195;&#8195;Всего: '+str(int(mem.total / MB))+'MB\n' \
                    '&#8195;&#8195;Использовано: '+str(int((mem.total - mem.available) / MB))+'MB\n' \
                    '&#8195;&#8195;Свободно: '+str(int(mem.available / MB))+'MB\n' \
                    '&#8195;&#8195;Использовано ботом: '+str(int(psutil.Process().memory_info().vms / MB))+'MB\n' \
                    '&#8195;&#8195;'

            param = (('v', '5.68'), ('peer_id', msg.chat_id), ('access_token', kbotlib.KBot.SETTINGS['TOKEN']),
                     ('message', text), ('forward_messages', msg.id))
            requests.post('https://api.vk.com/method/messages.send', param)

        elif msg.pretty_text[2] in ['акк', 'acc']:
            if msg.pretty_text[3] in ['сет', 'set']:
                attrs = {x.split('=')[0]: x.split('=')[1] for x in msg.text.split(' ')[5:]}
                if kbcblib.KBotAccount.setattr(msg.text.split(' ')[4], **attrs):
                    text = 'Атрибуты обновлены.'
                else:
                    text = 'Возникла ошибка и атрибуты не были обновлены.'

                param = (('v', '5.68'), ('peer_id', msg.chat_id), ('access_token', kbotlib.KBot.SETTINGS['TOKEN']),
                         ('message', text), ('forward_messages', msg.id))
                requests.post('https://api.vk.com/method/messages.send', param)
            elif msg.pretty_text[3] in ['лист', 'list']:
                if kbcblib.KBotDB.execute('SELECT * FROM users') is not None:
                    pass



def load():
    kbcblib.cmdslist.append(KBotAdminCommand())