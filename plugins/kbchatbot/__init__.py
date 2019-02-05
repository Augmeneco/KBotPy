import plugins.kbchatbot.kbcblib
import kbotlib
import requests
import types
from datetime import datetime
import time
import json


def handler(self, update):
    timer = time.time()

    if (len(update[5].split(' ')) < 2) or (update[2] & 2) or (update[5].lower().split(' ')[0] not in ('kb', 'кб')):
        return

    if 'from' in update[6]:
        from_id = int(update[6]['from'])
    else:
        from_id = update[3]

    kbotlib.log_print('(CmdID: '+str(update[1])+') Получено. '
                      '{SndTime: '+datetime.fromtimestamp(update[4]).strftime('%Y.%m.%d %H:%M:%S')+','
                      ' Chat: '+str(update[3])+','
                      ' From: '+str(from_id)+','
                      ' AttchmntsNum: '+str(int(len(update[7])/2))+','
                      ' Text: "' + update[5] + '"', 'info')

#########################

    if (update[3] > 0) and (update[3] < 200000000):
        chat_type = 'dialog'
    elif (update[3] > 0) and (update[3] > 200000000):
        chat_type = 'chat'
    elif update[3] < 0:
        chat_type = 'group_dialog'

    attachments = []
    for i in range(1, int(len(update[7]) / 2)):
        attachments.append({'type': update[7]['attach'+str(i)+'_type'], 'id': update[7]['attach'+str(i)]})

    update[5] = update[5].replace('<br>', '\n')
    update[5] = update[5].replace('&quot;', '"')
    update[5] = update[5].replace('&amp;', '&')

    db_user_info = plugins.kbchatbot.kbcblib.KBotAccount.get(from_id)
    if db_user_info is None:
        plugins.kbchatbot.kbcblib.KBotAccount.register(from_id, from_id, 1, 100, 0)
        db_user_info = plugins.kbchatbot.kbcblib.KBotAccount.get(from_id)

    msg = types.SimpleNamespace()
    setattr(msg, 'id', update[1])
    setattr(msg, 'flags', update[2])
    setattr(msg, 'chat_type', chat_type)
    setattr(msg, 'chat_id', update[3])
    setattr(msg, 'from_id', from_id)
    setattr(msg, 'time', update[4])
    setattr(msg, 'text', update[5])
    setattr(msg, 'pretty_text', update[5].lower().split(' '))
    setattr(msg, 'attachments', attachments)
    setattr(msg, 'db_user', db_user_info)

#########################

    if msg.pretty_text[0] in ['кб', 'kb', 'хз']:
        cmds = [x for x in plugins.kbchatbot.kbcblib.cmdslist
                if (msg.pretty_text[1] in x.commands)
                and (x.enabled == True)
                and (x.privileges & msg.db_user['privileges'])]

        if(len(cmds) > 0):
            for cmd in cmds:
                cmd.handler(msg,)
            kbotlib.log_print('(CmdID: ' + str(update[1]) + ') Обработано.', 'info')
        else:
            kbotlib.log_print('(CmdID: ' + str(update[1]) + ') Неверно!', 'info')
            param = (('v', '5.68'), ('peer_id', update[3]), ('access_token', kbotlib.KBot().SETTINGS['TOKEN']),
                     ('message', 'Команда не существует или доступ к команде запрещён'), ('forward_messages', update[1]))
            requests.post('https://api.vk.com/method/messages.send', param)

    elif update[5].split(' ')[0] == 'kbr':
        #text = update[5].split(' ')
        #del text[0]
        #text = text.join(' ')
        #data = json.load(open('./plugins/kbstandart/data.json').read())
        #for cmd in data[text]:
        pass

    with open('./plugins/kbchatbot/statistics.json', 'r+') as f:
        stats = json.loads(f.read())

        now = time.time()
        stats['mid'] = (stats['mid'] + ((now - update[4]) + (now - timer))) / 2
        stats['calls']['alltime'] += 1
        if stats['calls']['day']['update_time'] != datetime.now().strftime("%d%m%Y"):
            stats['calls']['day']['count'] = 1
            stats['calls']['day']['update_time'] = datetime.now().strftime("%d%m%Y")
        else:
            stats['calls']['day']['count'] += 1

        f.seek(0)
        f.write(json.dumps(stats))
        f.truncate()


def load():
    kbotlib.KBot().onMessage.add(handler)

'''
0 - номер события (сообщение - 4)
1 - айди сообщения
2 - бинарные флаги
3 - айди беседы (для пользователя: айди собеседника, для чата: -200000000, для сообщества: )
4 - юникс время отправления сообщеиния
5 - текст сообщения
6 - вложения
    from - айди отправителя в чате
    title - заголовок соообщения
'''