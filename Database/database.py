# encoding:utf-8

"""
Mysql Database 模块
===================
Author @ Junxiong Wang
data @ 2019/11/X
"""
import MySQLdb


class DB:
    def __init__(self):
        mysql_conf = {
            "host": "10.xx.xx.xx",
            "user": "xxx",
            "passwd": "xxx",
            "db": "xxx",
            "charset": "utf8"
        }
        try:
            self.db = MySQLdb.connect(**mysql_conf)
            self.cursor = self.db.cursor()
        except Exception as e:
            print e

    def select(self, sql):
        """
        :param sql:
        :return: 从数据库中 fetchall 的数据
        """
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            print e
            return e

    def insert(self, sql):
        """
        :param sql:
        :return: Null
        insert方式主要是处理插入数据的动作，该方法插入后数据会直接commit持久化数据
        """
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print e

    def update(self, sql):
        """
        :param sql:
        :return: Null
        update方式主要是处理更新数据的动作，该方法插入后数据会直接commit持久化数据
        """
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print e


if __name__ == '__main__':
    DB()
    pass
