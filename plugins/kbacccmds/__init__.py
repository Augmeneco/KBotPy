import plugins.kbchatbot.kbcblib as kbcblib
import kbotlib
import requests

class KBotAccountCommand(kbcblib.KBCBCmd):
    name = 'Регистрация в БД КБота'

    description = 'Управление аккаунтом КБота'

    commands = ['акк', 'acc']

    def handler(self, msg):
        #if (msg.pretty_text[2] is None):

        if (msg.pretty_text[2] == 'рег') or (msg.pretty_text[2] == 'reg'):
            if kbcblib.KBotAccount.register(msg.from_id, msg.from_id, 1, 100, 0) == True:
                text = 'Поздравляю вы зарегестрированы в системе'
            else:
                text = 'Вы уже есть в системе'
            param = (('v', '5.68'), ('peer_id', msg.chat_id), ('access_token', kbotlib.KBot.SETTINGS['TOKEN']),
                    ('message', text), ('forward_messages', msg.id))
            requests.post('https://api.vk.com/method/messages.send', param)

        elif (msg.pretty_text[2] == 'инфо') or (msg.pretty_text[2] == 'info'):
            info = kbcblib.KBotAccount.get(msg.from_id)
            if info == None:
                text = 'Вы не зарегестрированы в системе'
            else:
                text = '[ Информация о вашем аккаунте КБ ]\n'\
                       'Ваш никнейм: '+info['nickname']+'\n' \
                       'Баланс: '+str(info['balance'])+' КБК\n' \
                       'Клан: '+str(info['clan'])+'\n' \
                       'Привелегии: '+str(info['privileges'])+''

            param = (('v', '5.68'), ('peer_id', msg.chat_id), ('access_token', kbotlib.KBot().SETTINGS['TOKEN']),
                     ('message', text), ('forward_messages', msg.id))
            requests.post('https://api.vk.com/method/messages.send', param)

        elif (msg.pretty_text[2] == 'ник') or (msg.pretty_text[2] == 'nick'):
            kbcblib.KBotAccount.setattr(msg.from_id, nickname=msg.text.split(' ', 3)[3])
            param = (('v', '5.68'), ('peer_id', msg.chat_id), ('access_token', kbotlib.KBot().SETTINGS['TOKEN']),
                     ('message', 'Ваш ник изменён на: '+msg.text.split(' ', 3)[3]), ('forward_messages', msg.id))
            requests.post('https://api.vk.com/method/messages.send', param)

def load():
    kbcblib.cmdslist.append(KBotAccountCommand())