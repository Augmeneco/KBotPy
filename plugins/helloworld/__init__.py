import plugins.kbchatbot.kbcblib as kbchatbot
import time
import kbotlib
import vk_api

user = ''

class HelloWorld(kbchatbot.KBCBCmd):
    name = 'Unnamed command'

    description = 'Description of command'

    commands = ['hello', 'привет']

    def handler(self, msg):
        vk = vk_api.VkApi(token=kbotlib.KBot().SETTINGS['TOKEN'])
        vk = vk.get_api()
        vk.messages.send(user_id=msg[3], message='Hello, '+user+'!')
        time.sleep(10)


class Iam(kbchatbot.KBCBCmd):
    name = 'Unnamed command'

    description = 'Description of command'

    commands = ['менязовут']

    def handler(self, msg):
        global user
        user = msg[5].split(' ')[2]
        time.sleep(10)


def load():
    kbchatbot.cmdslist.append(HelloWorld())
    kbchatbot.cmdslist.append(Iam())