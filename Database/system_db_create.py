# encoding: utf-8
"""
- System DataBase Design & init
! Warning: Don't run this programme without being agreed by system manager
! 警告：未经管理员同意，不得运行此代码！
- Author@Wangjunxiong
"""
from database import DB


class Create:
    def __init__(self):
        self.__DB = DB().db
        self.cursor = self.__DB.cursor()

    def creat_ipsegment_table(self):
        """
        创建系统需要的255张基础IP表
        :return: None
        """
        for i in range(1, 255):
            if i == 127:
                pass
            else:
                table_structure = 'IPsegment_%s' % str(i)
                sql = """CREATE TABLE IF NOT EXISTS `ip_domains`.`{table_name}`  (
                    `id` int(32) NOT NULL AUTO_INCREMENT,
                    `origin_ip` varchar(255),
                    `domain` varchar(255),
                    `time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
                    PRIMARY KEY (`id`)
                    );""".format(table_name=table_structure)
                print sql
                try:
                    self.cursor.execute(sql)
                    print table_structure
                except Exception as e:
                    print e
                    return e

    def commit(self):
        self.__DB.commit()
        return None


if __name__ == '__main__':
    Create().creat_ipsegment_table()
    # Create().commit()

