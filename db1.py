import pymysql


def db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        database="users_test"
    )
def closeconn(conn):
    conn.close()   
