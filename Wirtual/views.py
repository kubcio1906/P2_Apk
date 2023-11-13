from flask import  jsonify,current_app
from extensions import db
from models import CurrencyData, CommodityData, StockData, NewsSource, NewsArticle, NewsTopic, TickerSentiment
from datetime import datetime
import requests





def fetch_and_save_fx_data(symbol,api_key):
    url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={symbol[:3]}&to_symbol={symbol[3:]}&outputsize=full&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        fx_data = response.json()       
        # Sprawdź, czy klucz istnieje w odpowiedzi
        if 'Time Series FX (Daily)' not in fx_data:
            return f"Key 'Time Series FX (Daily)' not found in API response for symbol {symbol}."
        for date_str, daily_data in fx_data['Time Series FX (Daily)'].items():
            print(f"Data for {date_str}: {daily_data}")  # Dodaj tę linię
            open_price = round(float(daily_data['1. open']),2)
            high_price = round(float(daily_data['2. high']),2)
            low_price = round(float(daily_data['3. low']),2)
            close_price = round(float(daily_data['4. close']),2)
            average_price = round((open_price + high_price + low_price + close_price) / 4 ,2)
                
            new_entry = CurrencyData(
                symbol=symbol,
                date=datetime.strptime(date_str, '%Y-%m-%d').date(),
                open_price=open_price,
                high_price=high_price,
                low_price=low_price,
                close_price=close_price,
                average_price=average_price  # obliczona średnia cena
                )
            db.session.add(new_entry)
        db.session.commit()
        return "Data fetched and saved successfully."
    else:
        return "Failed to fetch data from API."

def fetch_and_save_commodity_data(name, api_key):
    
    url = f'https://www.alphavantage.co/query?function={name}&interval=daily&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        commodity_data = response.json()
        print(commodity_data)

        if 'data' in commodity_data:
            for data_point in commodity_data['data']:
                # Sprawdzanie, czy wartość jest stringiem i zamiana przecinka na kropkę
                value_str = data_point['value']
                if isinstance(value_str, str):
                    value_str = value_str.replace(',', '.')
                try:
                    price = float(value_str)
                except ValueError:
                    continue  # Przechodzi do następnego elementu, jeśli konwersja się nie powiedzie

                new_commodity = CommodityData(
                    name=name,
                    date=datetime.strptime(data_point['date'], '%Y-%m-%d').date(),
                    price=price,
                    unit=commodity_data.get('unit', 'not provided')
                )
                db.session.add(new_commodity)
            db.session.commit()
            return "Commodity data fetched and saved successfully."
        else:
            return "Expected key 'data' not found in the JSON response."
    else:
        return f"Failed to fetch data from API. Status code: {response.status_code}"
       

def fetch_and_save_stock_data(symbol,api_key):
   
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        stock_data_json = response.json()

        # Dodaj logowanie, aby zobaczyć strukturę danych
        print("Odpowiedź z API:", stock_data_json)

        if 'Time Series (Daily)' in stock_data_json:
            time_series = stock_data_json['Time Series (Daily)']

            for date_str, daily_data in time_series.items():
                try:
                    open_price = float(daily_data['1. open'])
                    high_price = float(daily_data['2. high'])
                    low_price = float(daily_data['3. low'])
                    close_price = float(daily_data['4. close'])
                    average_price =  round((open_price + high_price + low_price + close_price) / 4,2)
                    volume = int(daily_data['5. volume'])
                    
                    
                    new_entry = StockData(
                        symbol=symbol,
                        date=date_str,
                        average_price=average_price,
                        volume=volume
                    )
                    db.session.add(new_entry)
                except TypeError as e:
                    print(f"Błąd podczas przetwarzania danych: {e}")
                    print(f"Dane: {daily_data}")

            db.session.commit()
            return "Stock data fetched and saved successfully."
        else:
            return "Expected key 'Time Series (Daily)' not found in the JSON response."
    else:
        return f"Failed to fetch data from API. Status code: {response.status_code}"

    



# Funkcja do pobierania i zapisywania danych z API Alpha Vantage
def fetch_and_save_news_data(ticker):
    api_key = current_app.config['ALPHA_VANTAGE_API_KEY']
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json()
        for item in news_data['feed']:
            # Konwersja czasu publikacji na obiekt datetime
            time_published = datetime.strptime(item['time_published'], '%Y%m%dT%H%M%S')
            
            # Utwórz i dodaj artykuł wiadomości
            article = NewsArticle(
                title=item['title'],
                url=item['url'],
                time_published=time_published,
                summary=item['summary'],
                # ... inne pola ...
            )
            db.session.add(article)
            db.session.flush()  # To pozwala na odzyskanie ID dla obiektu przed zapisem

            # Dodaj informacje o tematach
            for topic in item.get('topics', []):
                new_topic = NewsTopic(
                    topic=topic['topic'],
                    relevance_score=float(topic['relevance_score']),
                    article_id=article.id  # Użyj ID nowo utworzonego artykułu
                )
                db.session.add(new_topic)

            # Dodaj informacje o sentymentach tickerów
            for ticker_sentiment in item.get('ticker_sentiment', []):
                new_ticker_sentiment = TickerSentiment(
                    ticker=ticker_sentiment['ticker'],
                    relevance_score=float(ticker_sentiment['relevance_score']),
                    ticker_sentiment_score=float(ticker_sentiment['ticker_sentiment_score']),
                    ticker_sentiment_label=ticker_sentiment['ticker_sentiment_label'],
                    article_id=article.id  # Użyj ID nowo utworzonego artykułu
                )
                db.session.add(new_ticker_sentiment)
                
        db.session.commit()
        return "News data fetched and saved successfully."
    else:
        return "Failed to fetch data from API."
def setup_routes(app):

  #  @app.route('/fetch_fx_data/<string:symbol>', methods=['GET'])
   # def fetch_fx_data_view(symbol):
    #    result = fetch_and_save_fx_data(symbol)
    #   if result == "Data fetched and saved successfully.":
    #        response = {"status": "success", "message": result}
    #    else:
    #        response = {"status": "error", "message": result}
    #    return jsonify(response)
    
    # Endpoint do pobierania danych o towarach
    
    @app.route('/fetch_commodity_data/<string:name>', methods=['GET'])
    def fetch_commodity_data_view(name):
        result = fetch_and_save_commodity_data(name)
        if result == "Commodity data fetched and saved successfully.":
            return jsonify({'status': 'success', 'message': result}), 200
        else:
            return jsonify({'status': 'error', 'message': result}), 500

    @app.route('/fetch_stock_data/<string:symbol>', methods=['GET'])
    def fetch_stock_data(symbol):
      
        result = fetch_and_save_stock_data(symbol)
        if result == "Stock data fetched and saved successfully.":
           response = {"status": "success", "message": result}
        else:
            response = {"status": "error", "message": result}
        return jsonify(response)
    
    @app.route('/fetch_news_data/<string:ticker>', methods=['GET'])
    def fetch_news_data(ticker):
      
        result = fetch_and_save_news_data(ticker)
        if result == "News data fetched and saved successfully.":
            return jsonify({'status': 'success', 'message': result}), 200
        else:
            return jsonify({'status': 'error', 'message': result}), 500
def auto_fetch_currency_pairs(api_key):
   
    base_currencies = ["PLN", "USD", "EUR", "CHF", "GBP"]
    target_currencies = ["PLN", "USD", "EUR", "CHF", "GBP"]

    for base_currency in base_currencies:
        for target_currency in target_currencies:
            if base_currency != target_currency:
                symbol = base_currency + target_currency
                fetch_and_save_fx_data(symbol, api_key)
def auto_fetch_commodity_data(api_key):
    
    commodities = ["BRENT", "NATURAL_GAS", "COPPER", "ALUMINUM", "COFFEE",]

    for commodity in commodities:
        fetch_and_save_commodity_data(commodity,api_key)
def auto_fetch_stock_data(api_key):
 
    # Lista symboli 10 najpopularniejszych spółek
    stock_symbols = ["AAPL", "MSFT", "AMZN", "GOOGL", "FB", "TSLA", "BRK.A", "V", "JNJ", "WMT"]

    for symbol in stock_symbols:
        fetch_and_save_stock_data(symbol,api_key)