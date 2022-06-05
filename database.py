import mysql.connector


def open_connection():
    cnx = mysql.connector.connect(user='root', password='#5O<##l7n-1R_IO<', host='34.132.141.97', 
                              database='waralobby_db')

    return cnx

