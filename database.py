import pymysql

conn = pymysql.connect(host = "genmotorcycles.com ", user="genmotor_huseinaji", passwd="huseinaji", db = "genmotor_charging")
myCursor = conn.cursor()

myCursor.execute("""CREATE TABLE name
    (
        id int primary key,
        name varchar(20)
    )
    """)
conn.commit()
conn.close()