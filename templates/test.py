import sqlite3


# connect with db
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()
cursor.execute("""
                   create table if not exists PRODUCT
                   (id integer primary key autoincrement,
                   Product_name text,
                   Product_price integer,  
                   Product_url text,
                   email varchar(20))
                   """)
def update_product():
    cursor.execute("""
        update PRODUCT set Product_price ='₹7,000'
        where id = 2
                   """)
    print("data updated.")

update_product()
conn.commit()

conn.close()
