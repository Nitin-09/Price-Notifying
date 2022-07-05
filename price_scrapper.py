from flask import Flask,render_template, request,redirect, url_for
import sqlite3

app = Flask(__name__)

def insert_product(name,price,url,email):
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
    cursor.execute("insert into PRODUCT (Product_name,Product_price,Product_url,email) values(?,?,?,?)",[name,price,url,email])
    conn.commit()
    conn.close()


def get_product():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    all_products = cursor.execute("select * from PRODUCT").fetchall()
    conn.commit()
    conn.close()
    return all_products

def price_scrapper(url):
    import requests
    from bs4 import BeautifulSoup
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    product_cards = soup.find_all("div", class_="_1YokD2 _3Mn1Gg col-8-12")
    for x in product_cards:
        product_name = x.find("span", class_="B_NuCI").getText()
        discounted_price = x.find("div", class_="_30jeq3 _16Jk6d").getText()
        # actual_pice = x.find("div", class_="_3I9_wc _2p6lqe").getText()
        print("Product Name:", product_name)
        # print("Actual price:", actual_pice)
        print("Discounted price:", discounted_price)
    return product_name,discounted_price


@app.route("/")
def home_page():
    all_product=get_product()
    return render_template("front_page.html",data=all_product)

@app.route("/add_product",methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        product_url = request.form.get("product_url")
        email = request.form.get("email")
        product_details=price_scrapper(product_url)
        insert_product(product_details[0],product_details[1],product_url,email)
        return redirect(url_for("home_page"))
    return render_template("form_page.html")
app.run(debug=True)