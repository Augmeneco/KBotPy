import plugins.kbchatbot.kbcblib as kbcblib
import kbotlib
import requests

class KBotHelpCommand(kbcblib.KBCBCmd):
    name = 'Помощь по командам КБота'

    description = 'Помощь по командам КБота'

    privileges = 15

    commands = ['помощь', 'help']

    def handler(self, msg):
        if len(msg.pretty_text) == 2:
            text = '[ Помощь ]\n'
            for cmd in kbcblib.cmdslist:
                text += cmd.commands[0]+' - '+cmd.description+'\n'

            param = (('v', '5.68'), ('peer_id', msg.chat_id), ('access_token', kbotlib.KBot.SETTINGS['TOKEN']),
                     ('message', text), ('forward_messages', msg.id))
            requests.post('https://api.vk.com/method/messages.send', param)
        else:
            cmds = [x for x in kbcblib.cmdslist if (msg.pretty_text[2] in x.commands)]

            if (len(cmds) > 0):
                text = ''
                for cmd in cmds:
                    text += '[ Помощь для команды '+cmd.commands[0]+' ]\n'+cmd.help

                param = (('v', '5.68'), ('peer_id', msg.chat_id), ('access_token', kbotlib.KBot.SETTINGS['TOKEN']),
                         ('message', text), ('forward_messages', msg.id))
                requests.post('https://api.vk.com/method/messages.send', param)
            else:
                param = (('v', '5.68'), ('peer_id', msg.chat_id), ('access_token', kbotlib.KBot.SETTINGS['TOKEN']),
                         ('message', 'Команды для которой вы зпросили помощь не существует'), ('forward_messages', msg.id))
                requests.post('https://api.vk.com/method/messages.send', param)


def load():
    kbcblib.cmdslist.append(KBotHelpCommand())