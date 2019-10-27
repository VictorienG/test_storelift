from datetime import datetime

from flask import Flask, render_template, request

from databases.crud import s
from databases.purchases import take_product, return_product
from databases.entrance import entrance
from databases.exit import leave_the_store
from databases.get_data_for_api import get_stores, get_products_in_store, get_products_in_buying_for_customer, \
    get_purchases_id_from_customer, get_purchases_names_from_customer, get_available_product_for_customer

app = Flask(__name__)
app.config.from_object('config')
global id_store
global id_customer


@app.route('/')
def names():
    data = get_stores(s)
    return render_template("names.html", data=data)


@app.route('/first_purchases', methods=['GET', 'POST'])
def buy_a_product():
    if request.method == 'POST':
        prenom = request.form.get('prenom')
        nom = request.form.get('nom')
        global id_store, id_customer
        id_store = request.form.get('store')
        id_customer = entrance(s, id_store, nom, prenom)
        data = get_products_in_store(s, id_store)

    return render_template("first_purchases.html", data=data)


@app.route('/buy_or_return_purchases', methods=['GET', 'POST'])
def buy_or_return_product():
    if request.method == 'POST':

        if request.form.get("Valider") == "Valider achat":

            product = request.form.get("produit")
            print("achat !!")
            take_product(s, id_store, id_customer, product)


        else:
            request.form.get("Valider retour")
            product = request.form.get("produit")
            print("retour !!!")
            return_product(s, id_store, id_customer, product)
    data = get_products_in_buying_for_customer(s, id_store, id_customer)
    return render_template("buy_or_return_purchases.html", data = data)


@app.route('/buy_purchases', methods=['GET', 'POST'])
def buy_purchases():
    if request.method == 'POST':
        data = get_available_product_for_customer(s, id_store, id_customer)
    return render_template("buy_purchases.html", data=data)


@app.route('/return_purchases', methods=['GET', 'POST'])
def return_products():
    data = get_products_in_buying_for_customer(s, id_store, id_customer)
    return render_template("return_purchases.html", data=data)


@app.route('/exit', methods=['GET', 'POST'])
def exit():
    now = datetime.now()
    now = now.strftime("%d/%m/%Y %H:%M")
    data = leave_the_store(s, id_store, id_customer)
    history = get_purchases_names_from_customer(s, id_customer, id_store, now)
    print(history)
    return render_template("exit.html", data=data, history=history)


if __name__ == "__main__":
    app.run()
