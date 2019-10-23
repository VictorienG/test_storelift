
def change_stock(id_store, id_product, give_back=False):
    change_quantity_stock = s.query(Stock).filter(
        and_(
            Stock.id_store==id_store,
            Stock.id_prod==id_product
        )
    )
    if give_back:
        change_quantity_stock.quantity = change_quantity_stock.quantity - 1
    else :
        change_quantity_stock.quantity = change_quantity_stock.quantity + 1