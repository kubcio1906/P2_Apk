from flask import Flask
from flask_restful import Api
from extensions import db, migrate
from views import(
    auto_fetch_currency_data, auto_fetch_commodity_data, auto_fetch_stock_data, auto_fetch_inflation_data,auto_fetch_save_interest_rates_data,data_exists_in_database
    )
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://aa'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ALPHA_VANTAGE_API_KEY'] = 'LA5MNPY8I21T1PEJ'
    app.config['API_KEY_INFLU']= 'rSDuwDyiKwglyDEJ+RFGAw==GCyHG2Tk9GR6ZbwE'

    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

# Inicjalizacja i start harmonogramu w kontekście aplikacji
def schedule_tasks():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: auto_fetch_currency_data(app.config['ALPHA_VANTAGE_API_KEY']) if not print(data_exists_in_database('currency_pairs', datetime.today().strftime('%Y-%m-%d'))) else None,
        trigger="cron",
        day_of_week='mon-fri',
        hour=1
    )

    # Harmonogram dla commodity_data
    scheduler.add_job(
        func=lambda: auto_fetch_commodity_data(app.config['ALPHA_VANTAGE_API_KEY']) if not data_exists_in_database('commodity_data', datetime.today().strftime('%Y-%m-%d')) else None,
        trigger="cron",
        day_of_week='mon-fri',
        hour=1
    )

    # Harmonogram dla stock_data
    scheduler.add_job(
        func=lambda: auto_fetch_stock_data(app.config['ALPHA_VANTAGE_API_KEY']) if not data_exists_in_database('stock_data',datetime.today().strftime('%Y-%m-%d')) else None,
        trigger="cron",
        day_of_week='mon-fri',
        hour=1
    )

    # Harmonogram dla inflation_data
    scheduler.add_job(
        func=lambda: auto_fetch_inflation_data(app.config['ALPHA_VANTAGE_API_KEY']) if not data_exists_in_database('inflation_data',datetime.today().strftime('%Y-%m-%d')) else None,
        trigger="cron",
        day=14,  # Pierwszy dzień każdego miesiąca
        hour=1
    )
    
    # Harmonogram dla retail_sales_data
    scheduler.add_job(
        func=lambda: auto_fetch_save_interest_rates_data(app.config['ALPHA_VANTAGE_API_KEY']) if not data_exists_in_database('interest_rates_data', datetime.today().strftime('%Y-%m-%d')) else None,
        
        trigger="cron",
        day=19,  # Pierwszy dzień każdego miesiąca
        hour=1
    )
    scheduler.start()
if __name__ == '__main__':
    
    with app.app_context():
        today = datetime.today().strftime('%Y-%m-%d')
      
        if not data_exists_in_database('currency_pairs', today):
            auto_fetch_currency_data(app.config['ALPHA_VANTAGE_API_KEY'])
        if not data_exists_in_database('commodity_data', today):
            auto_fetch_commodity_data(app.config['ALPHA_VANTAGE_API_KEY'])
        if not data_exists_in_database('stock_data', today):
            auto_fetch_stock_data(app.config['ALPHA_VANTAGE_API_KEY'])
        if not data_exists_in_database('inflation_data', today):
            auto_fetch_inflation_data(app.config['ALPHA_VANTAGE_API_KEY'])
        if not data_exists_in_database('interest_rates_data', today):
            auto_fetch_save_interest_rates_data(app.config['ALPHA_VANTAGE_API_KEY'])
        
       


#rSDuwDyiKwglyDEJ+RFGAw==GCyHG2Tk9GR6ZbwE

