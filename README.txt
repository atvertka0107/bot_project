run in python console:
con = sqlite3.coonect('bd.bd')
cur = con.cursor()
cur.execute('CREATE TABLE users (id int auto_increment primary key, login varchar(50), password varchar (50))')
con.commit()
cur.close()
con.close()