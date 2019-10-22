from databases.models import Store, Customer, Product, Stock, IsInStore

fill_store = [
    Store(
        address="15 rue de la paix 75015",
        name_store="magasin de la paix",
    ),
    Store(
        address="1 rue de la guerre 75015",
        name_store="magasin de la guerre"
    )
]

fill_customer = [
    Customer(
        mail="victorien@gmail.com",
        last_name="Gimenez",
        first_name="Victorien"
    ),
    Customer(
        mail="macron@gmail.com",
        last_name="Macron",
        first_name="Emmanuel"
    )
]

fill_product = [
    Product(
        name="Evian 50 cL",
        brand="Evian"
    ),
    Product(
        name="Evian 1L",
        brand="Evian"
    ),
    Product(
        name="Lait 50 cL",
        brand="Lactel"
    ),
    Product(
        name="KitKat paquet de 6",
        brand="Nestlé"
    ),
]

fill_stock = [
    Stock(
        id_store=1,
        id_prod=1,
        unit_price=0.56,
        quantity=8
    ),
    Stock(
        id_store=1,
        id_prod=2,
        unit_price=1,
        quantity=8)
    ,
    Stock(
        id_store=1,
        id_prod=3,
        unit_price=0.59,
        quantity=12
    ),
    Stock(
        id_store=2,
        id_prod=2,
        unit_price=1,
        quantity=6
    ),
    Stock(
        id_store=2,
        id_prod=4,
        unit_price=1.50,
        quantity=2000
    ),
    Stock(
        id_store=2,
        id_prod=3,
        unit_price=0.59,
        quantity=1
    ),
]

fill_is_in_store = [
    IsInStore(
        id_store=1,
        id_customer=1,
    ),
    IsInStore(
        id_store=1,
        id_customer=2,
    ),
    IsInStore(
        id_store=2,
        id_customer=1,
    ),
    IsInStore(
        id_store=2,
        id_customer=2,
    ),
]
