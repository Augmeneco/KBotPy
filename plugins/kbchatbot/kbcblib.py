import MySQLdb
import MySQLdb.cursors
import os
import kbotlib


cmdslist = []


class KBCBCmd:
    name = 'Unnamed command'

    description = 'Description of command'

    commands = []

    enabled = True

    privileges = 15

    help = '''Help for unnamed command'''

    def handler(self, msg):
        pass


class KBotDB:
    @staticmethod
    def execute(query):
        db = MySQLdb.connect(host=kbotlib.KBot().SETTINGS['PluginsSettings']['kbchatbot']['ChatbotDB']['Host'],
                             user=kbotlib.KBot().SETTINGS['PluginsSettings']['kbchatbot']['ChatbotDB']['User'],
                             passwd=kbotlib.KBot().SETTINGS['PluginsSettings']['kbchatbot']['ChatbotDB']['Passwd'],
                             db=kbotlib.KBot().SETTINGS['PluginsSettings']['kbchatbot']['ChatbotDB']['DB'],
                             charset='utf8')
        cursor = db.cursor()
        cursor.execute('SET NAMES utf8mb4')
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET character_set_connection=utf8mb4")
        result = cursor.execute(query)
        db.commit()
        db.close()
        return result.fetchall()


class KBotAccount:
    @staticmethod
    def register(vkid, nickname, privileges, balance, clan):
        if KBotAccount.get(vkid) == None:
            db = MySQLdb.connect(host=kbotlib.KBot().SETTINGS['PluginsSettings']['kbchatbot']['ChatbotDB']['Host'],
                                 user=kbotlib.KBot().SETTINGS['PluginsSettings']['kbchatbot']['ChatbotDB']['User'],
                                 passwd=kbotlib.KBot().SETTINGS['PluginsSettings']['kbchatbot']['ChatbotDB']['Passwd'],
                                 db=kbotlib.KBot().SETTINGS['PluginsSettings']['kbchatbot']['ChatbotDB']['DB'],
                                 charset='utf8')
            cursor = db.cursor()
            cursor.execute('SET NAMES utf8mb4')
            cursor.execute("SET CHARACTER SET utf8mb4")
            cursor.execute("SET character_set_connection=utf8mb4")
            query = "INSERT INTO users (vkid,nickname,privileges,balance,clan) " \
                    "VALUES('"+str(vkid)+"','"+str(nickname)+"','"+str(privileges)+"','"+str(balance)+"','"+str(clan)+"');"
            cursor.execute(query)
            db.commit()
            db.close()
            return True
        else:
            return False

    @staticmethod
    def get(vkid):
        db = MySQLdb.connect(host=kbotlib.KBot().SETTINGS['PluginsSettings']['kbchatbot']['ChatbotDB']['Host'],
                             user=kbotlib.KBot().SETTINGS['PluginsSettings']['kbchatbot']['ChatbotDB']['User'],
                             passwd=kbotlib.KBot().SETTINGS['PluginsSettings']['kbchatbot']['ChatbotDB']['Passwd'],
                             db=kbotlib.KBot().SETTINGS['PluginsSettings']['kbchatbot']['ChatbotDB']['DB'],
                             charset='utf8')
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SET NAMES utf8mb4')
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET character_set_connection=utf8mb4")
        query = "SELECT * FROM users WHERE vkid = '"+str(vkid)+"';"
        cursor.execute(query)
        db.close()
        return cursor.fetchone()



    @staticmethod
    def setattr(vkid, **kwargs):
        if kwargs is None:
            return False

        data = []
        for key, value in kwargs.items():
            if key in ('nickname', 'privileges', 'balance', 'clan'):
                data.append("`"+str(key)+"` = '"+str(value)+"'")
            else:
                return False

        db = MySQLdb.connect(host=kbotlib.KBot().SETTINGS['PluginsSettings']['kbchatbot']['ChatbotDB']['Host'],
                             user=kbotlib.KBot().SETTINGS['PluginsSettings']['kbchatbot']['ChatbotDB']['User'],
                             passwd=kbotlib.KBot().SETTINGS['PluginsSettings']['kbchatbot']['ChatbotDB']['Passwd'],
                             db=kbotlib.KBot().SETTINGS['PluginsSettings']['kbchatbot']['ChatbotDB']['DB'],
                             charset='utf8')
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SET NAMES utf8mb4')
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET character_set_connection=utf8mb4")
        query = "UPDATE users SET "+','.join(data)+" WHERE vkid = '" + str(vkid) + "';"
        result = cursor.execute(query)
        db.commit()
        db.close()
        if result == 0:
            return True
        else:
            return False