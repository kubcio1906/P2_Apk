from flask import Flask
from flask_restful import Api
from extensions import db, migrate
from views import setup_routes  # Import funkcji ustawiającej routy,



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://aa'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ALPHA_VANTAGE_API_KEY'] = 'LA5MNPY8I21T1PEJ'

    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)

    setup_routes(app)

    with app.app_context():
        db.create_all()

    return app
    

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        from views import auto_fetch_currency_pairs
        auto_fetch_currency_pairs()
    app.run(debug=True)












   
   






