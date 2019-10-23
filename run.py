from sqlalchemy import and_

from databases import crud
from databases.crud import s
from databases.models import Customer
from databases.entrance import create_customer, customer_in_the_store, entrance

if __name__ == "__main__":
    #app.run(debug=True)
    crud.pipeline_create_databases()
    entrance(2, "Gimenez", "Victorien")
    entrance(1, "Pierre", "QuiRoule")

  
