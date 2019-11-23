"""
Mysql

"""
import MySQLdb


class DB:
    def __init__(self):
        mysql_conf = {
            "host": "10.245.146.37",
            "user": "root",
            "passwd": "platform",
            "db": "ip_domains",
            "charset": "utf8"
        }
        try:
            self.db = MySQLdb.connect(**mysql_conf)
            self.cursor = self.db.cursor()
        except Exception as e:
            print e

    def insert(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print e


if __name__ == '__main__':
    DB()
    pass
