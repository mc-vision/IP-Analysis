"""
Scripts
"""

from Database.database import DB


def get_info():
    DB().db.cursor().execute()
    info = DB().db.cursor().fetchall()
    for i in info:
        print i


if __name__ == '__main__':
    get_info()
