from flask import Flask, render_template, request

from databases.course import take_product, return_product
from databases.entrance import entrance
from databases.exit import leave_the_store
from databases.get_data import get_stores, get_products_from_store, get_products_from_customer

app = Flask(__name__)
app.config.from_object('config')
global id_store
global id_customer


@app.route('/')
def names():
    data = get_stores()
    print("555", data)
    return render_template("names.html", data=data)


@app.route('/first_purchases', methods=['GET', 'POST'])
def buy_a_product():
    if request.method == 'POST':
        prenom = request.form.get('prenom')
        nom = request.form.get('nom')
        global id_store, id_customer
        id_store = request.form.get('store')
        id_customer = entrance(id_store, nom, prenom)
        data = get_products_from_store(id_store)

    return render_template("first_purchases.html", data=data)


@app.route('/buy_or_return_purchases', methods=['GET', 'POST'])
def buy_or_return_product():
    if request.method == 'POST':

        if request.form.get("Valider") == "Valider achat":

            product = request.form.get("produit")
            print("achat !!")
            take_product(id_store, id_customer, product)


        else:
            request.form.get("Valider retour")
            product = request.form.get("produit")
            print("retour !!!")
            return_product(id_store, id_customer, product)

    return render_template("buy_or_return_purchases.html")


@app.route('/buy_purchases', methods=['GET', 'POST'])
def buy_purchases():
    if request.method == 'POST':
        data = get_products_from_store(id_store)
    return render_template("buy_purchases.html", data=data)


@app.route('/return_purchases', methods=['GET', 'POST'])
def return_products():
    data = get_products_from_customer(id_store, id_customer)
    return render_template("return_purchases.html", data=data)


@app.route('/exit', methods=['GET', 'POST'])
def exit():
    data = leave_the_store(id_store, id_customer)
    return render_template("exit.html", data=data)


if __name__ == "__main__":
    app.run()

if __name__ == "__main__":
    app.run()
