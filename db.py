# -*- coding:utf-8 -*-

import MySQLdb


class MyDB(object):
    """
    封装管理数据库的上下文
    """

    def __init__(self, db_info):
        assert isinstance(db_info, dict)
        self.conn = MySQLdb.connect(**db_info)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            return True

        if exc_val:
            self.conn.rollback()
            self.cursor.close()
            self.conn.close()
            print(exc_tb)
            print(exc_type)

        return True
