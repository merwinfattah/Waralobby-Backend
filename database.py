import mysql.connector



def open_connection():
    cnx = mysql.connector.connect(user='root', password='\H5:fYy&%k"y)bX[', host='34.101.157.254', 
                              database='waralobby_db')

    return cnx

