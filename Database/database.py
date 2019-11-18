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
            "db": "ip_reverse",
            "charset": "utf8"
        }
        try:
            self.db = MySQLdb.connect(**mysql_conf)
            self.cursor = self.db.cursor()
            self.cursor.execute("select ip_origin, domain, ip from ip_mapping_relations_real where ip_origin != ip;")
            for i in self.cursor.fetchall():
                if i[2] == '':
                    print i[0], i[1], 'Null'
                else:
                    print i[0], i[1], i[2]
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
