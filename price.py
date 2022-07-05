def price_scrapper(url):
    import requests
    from bs4 import BeautifulSoup
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_cards = soup.find_all("div", class_="_1YokD2 _3Mn1Gg col-8-12")
    for x in product_cards:
        discounted_price = x.find("div", class_="_30jeq3 _16Jk6d").getText()
    return discounted_price
def mail_alert(mail,name):
    import smtplib
    from_="nitingangwani982000@gmail.com"
    to=mail
    subject="PRICE DROP ALERT For The Product "+name
    body="The price of "+ name +" has been fallen down"
    msg=f"subject:{subject}\n\n{body}"
    pwd="yxcpuwnayuyonswf"

    conn=smtplib.SMTP("smtp.gmail.com",587)
    conn.starttls()
    conn.login(from_,pwd)
    conn.sendmail(from_,to,msg)
    conn.close()


    
import sqlite3
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()
all_product=cursor.execute("select * from PRODUCT").fetchall()
for i in all_product:
    name=i[1]
    old_price=float(i[2].replace('₹',"").replace(',',""))
    url=i[3]
    email=i[4]
    new_price=price_scrapper(url)
    new_price=float(new_price.replace('₹',"").replace(',',""))
    # print(new_price)
    if old_price>new_price:
        mail_alert(email,name)
    else:
        print("same price")
from datetime import datetime
with open("C:/Users/nitin/OneDrive/Desktop/testing.txt", 'a') as file:
    file.write(str(datetime.now()) + "\n")
conn.commit()

conn.close()
