from databases import crud
from databases.course import take_product, return_product
from databases.entrance import entrance

if __name__ == "__main__":
    # app.run(debug=True)
    crud.pipeline_create_databases()
    entrance(2, "Gimenez", "Victorien")
    entrance(1, "Pierre", "QuiRoule")
    take_product(1, 2, "evian 50 cl", "evian")
    take_product(1, 2, "evian 50 cl", "evian")
    take_product(1, 2, "evian 50 cl", "evian")
    return_product(1, 2, "evian 50 cl", "evian")



