
from flask_migrate import Migrate
from apps import create_app
from extends import db


app = create_app()
migrate =Migrate(app =app,db =db)
db.init_app(app)



if __name__ =="__main__":
    app.run()