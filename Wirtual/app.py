from flask import Flask
from flask_restful import Api
from extensions import db,migrate
from services import(
    auto_fetch_currency_data, auto_fetch_commodity_data, auto_fetch_stock_data, auto_fetch_inflation_data,
    auto_fetch_save_interest_rates_data,calculate_inflation_from_cpi,auto_fetch_ema_data,auto_fetch_rsi_data
    
    )
from apscheduler.schedulers.background import BackgroundScheduler
from views import data_exists_in_database,populate_time_dimension,calculate_and_save_correlations
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
    today_str = datetime.today().strftime('%Y-%m-%d')
    scheduler.add_job(
        func=lambda: auto_fetch_currency_data(app.config['ALPHA_VANTAGE_API_KEY']) if not data_exists_in_database('currency_pairs', today_str) else None,
        trigger="cron",
        day_of_week='mon',
        hour=1
    )


    scheduler.add_job(
        func=lambda: auto_fetch_commodity_data(app.config['ALPHA_VANTAGE_API_KEY']) if not data_exists_in_database('commodity_data', today_str) else None,
        trigger="cron",
        day_of_week='tue',
        hour=1
    )

    
    scheduler.add_job(
        func=lambda: auto_fetch_stock_data(app.config['ALPHA_VANTAGE_API_KEY']) if not data_exists_in_database('stock_data',today_str) else None,
        trigger="cron",
        day_of_week='wed',
        hour=1
    )

 
    scheduler.add_job(
        func=lambda: auto_fetch_inflation_data(app.config['ALPHA_VANTAGE_API_KEY']) if not data_exists_in_database('inflation_data',today_str) else None,
        trigger="cron",
        day=14,  
        hour=1
    )
    
  
    scheduler.add_job(
        func=lambda: auto_fetch_save_interest_rates_data(app.config['ALPHA_VANTAGE_API_KEY']) if not data_exists_in_database('interest_rates_data', today_str) else None,
        
        day=19,  
        hour=1
    )
    
    scheduler.start()
if __name__ == '__main__':
    
    with app.app_context():
        today = datetime.today().strftime('%Y-%m-%d')
        symbols = ['IBM','MSFT']  # Lista symboli akcji
        if not data_exists_in_database('currency_pairs', today):
            auto_fetch_currency_data(app.config['ALPHA_VANTAGE_API_KEY'])
        if not data_exists_in_database('commodity_data', today):
            auto_fetch_commodity_data(app.config['ALPHA_VANTAGE_API_KEY'])
        if not data_exists_in_database('stock_data', today):
            auto_fetch_stock_data(app.config['ALPHA_VANTAGE_API_KEY'])
        if not data_exists_in_database('inflation_data', today):
            auto_fetch_inflation_data(app.config['ALPHA_VANTAGE_API_KEY'],db.session)
        if not data_exists_in_database('interest_rates_data', today):
            auto_fetch_save_interest_rates_data(app.config['ALPHA_VANTAGE_API_KEY'])
        intervals = ['daily']  # Lista interwałów czasowych
        time_periods = [50, 100]  # Lista okresów czasowych dla EMA
        series_types = ['close']  # Lista typów serii danych
        auto_fetch_ema_data(app.config['ALPHA_VANTAGE_API_KEY'], symbols, intervals, time_periods, series_types)
        intervals = ['daily']  # Lista interwałów czasowych
        time_periods = [14]  # Lista okresów czasowych dla RSI
        series_types = ['close']  # Typ serii danych, np. cena zamknięcia
        if not data_exists_in_database('rsi_data', today):
            
            auto_fetch_rsi_data(app.config['ALPHA_VANTAGE_API_KEY'], symbols, intervals, time_periods, series_types)
    
        calculate_and_save_correlations()
        populate_time_dimension()
        
    


