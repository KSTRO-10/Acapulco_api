from app.database import get_connection

def registrar_uso(endpoint, formato, ip, username="Anonimo"):

    conn=get_connection()
    cursor=conn.cursor()

    sql="""
    INSERT INTO api_stats(endpoint,formato,ip,username)
    VALUES(%s,%s,%s,%s)
    """

    cursor.execute(sql,(endpoint,formato,ip,username))

    conn.commit()

    cursor.close()
    conn.close()