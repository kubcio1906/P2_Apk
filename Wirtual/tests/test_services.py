import sys
import os
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch
from services import fetch_and_save_fx_data, fetch_and_save_stock_data, fetch_and_save_commodity_data,fetch_and_save_inflation_data,fetch_and_save_interest_rates_data
import requests
from app.__init__ import create_app


class TestCurrencyData(unittest.TestCase):

    def setUp(self):
        self.app = create_app()  # Utwórz instancję aplikacji
        self.app_context = self.app.app_context()  # Utwórz kontekst aplikacji
        self.app_context.push()  # Aktywuj kontekst aplikacji

    def tearDown(self):
        self.app_context.pop()  # Usuń kontekst aplikacji po zakończeniu testu
    @patch('services.requests.get')
    def test_fetch_and_save_fx_data_success(self, mock_get):
        # Przygotowanie danych testowych
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Meta Data": {
                "1. Information": "Forex Daily Prices (open, high, low, close)",
                "2. From Symbol": "EUR",
                "3. To Symbol": "USD",
                "4. Output Size": "Compact",
                "5. Last Refreshed": "2023-11-24 13:35:00",
                "6. Time Zone": "UTC"
            },
            "Time Series FX (Daily)": {
                "2023-11-24": {
                    "1. open": "1.09040",
                    "2. high": "1.09282",
                    "3. low": "1.08947",
                    "4. close": "1.09079"
                },
              
            }
        }

        # Wywołanie funkcji
        result = fetch_and_save_fx_data('EURUSD', 'ALPHA_VANTAGE_API_KEY')

        # Sprawdzenie wyniku
        self.assertIsNone(result)  

    @patch('services.requests.get')
    def test_fetch_and_save_fx_data_failure(self, mock_get):
        # Symulacja błędu sieciowego
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        # Wywołanie funkcji
        result = fetch_and_save_fx_data('EURUSD', 'ALPHA_VANTAGE_API_KEY')

        # Sprawdzenie wyniku
        self.assertIsNotNone(result)
        self.assertIn("Request Exception", result)

class TestStockData(unittest.TestCase):

    def setUp(self):
        self.app = create_app()  # Utwórz instancję aplikacji
        self.app_context = self.app.app_context()  # Utwórz kontekst aplikacji
        self.app_context.push()  # Aktywuj kontekst aplikacji

    def tearDown(self):
        self.app_context.pop()  # Usuń kontekst aplikacji po zakończeniu testu
    @patch('services.requests.get')
    def test_fetch_and_save_sock_data_success(self, mock_get):
        # Przygotowanie danych testowych
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Meta Data": {
                "1. Information": "Intraday (Daily) open, high, low, close prices and volume",
                "2. Symbol": "IBM",
                "3. Last Refreshed": "2023-11-22",
                "4. Interval": "Daily",
                "5. Output Size": "Compact",
                "6. Time Zone": "US/Eastern"
                },
            "Time Series (Daily)": {
                "2023-11-22": {
                    "1. open": "155.0600",
                    "2. high": "155.0600",
                    "3. low": "155.0600",
                    "4. close": "155.0600",
                    "5. volume": "200"
                },
                "2023-11-22": {
                    "1. open": "155.0600",
                    "2. high": "155.0600",
                    "3. low": "155.0600",
                    "4. close": "155.0600",
                    "5. volume": "6"
                },
                
            
            }
        }

        # Wywołanie funkcji
        result = fetch_and_save_stock_data('IBM', 'ALPHA_VANTAGE_API_KEY')

        # Sprawdzenie wyniku
        self.assertIsNone(result)

    @patch('services.requests.get')
    def test_fetch_and_save_stock_data_failure(self, mock_get):
        # Symulacja błędu sieciowego
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        # Wywołanie funkcji
        result = fetch_and_save_stock_data('IBM', 'ALPHA_VANTAGE_API_KEY')

        # Sprawdzenie wyniku
        self.assertIsNotNone(result)
        self.assertIn("Request Exception", result)

class TestCommodityData(unittest.TestCase):

    def setUp(self):
        self.app = create_app()  # Utwórz instancję aplikacji
        self.app_context = self.app.app_context()  # Utwórz kontekst aplikacji
        self.app_context.push()  # Aktywuj kontekst aplikacji

    def tearDown(self):
        self.app_context.pop()  # Usuń kontekst aplikacji po zakończeniu testu
    @patch('services.requests.get')
    def test_fetch_and_save_commodity_data_success(self, mock_get):
        # Przygotowanie danych testowych
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Copper",
            "interval": "monthly",
            "unit": "dollars per barrel",
            "data": [
                {
                    "date": "2023-10-01",
                    "value": "85.64"
                },
                {
                    "date": "2023-09-01",
                 "value": "89.43"
                },
                
            ]
            
        }

        # Wywołanie funkcji
        result = fetch_and_save_commodity_data('COPPER', 'ALPHA_VANTAGE_API_KEY')

        # Sprawdzenie wyniku
        self.assertIsNone(result) 

    @patch('services.requests.get')
    def test_fetch_and_save_commodity_data_failure(self, mock_get):
        # Symulacja błędu sieciowego
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        # Wywołanie funkcji
        result = fetch_and_save_commodity_data('COPPER', 'ALPHA_VANTAGE_API_KEY')

        # Sprawdzenie wyniku
        self.assertIsNotNone(result)
        self.assertIn("Request Exception", result)

class TestCpiData(unittest.TestCase):

    def setUp(self):
        self.app = create_app()  # Utwórz instancję aplikacji
        self.app_context = self.app.app_context()  # Utwórz kontekst aplikacji
        self.app_context.push()  # Aktywuj kontekst aplikacji

    def tearDown(self):
        self.app_context.pop()  # Usuń kontekst aplikacji po zakończeniu testu
    @patch('services.requests.get')
    def test_fetch_and_save_inflation_data_success(self, mock_get):
        # Przygotowanie danych testowych
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Consumer Price Index for all Urban Consumers",
            "interval": "monthly",
            "unit": "index 1982-1984=100",
            "data": [
                {
                    "date": "2023-10-01",
                    "value": "307.671"
                },
                {
                    "date": "2023-09-01",
                    "value": "307.789"
                },
                    ]
            }

        # Wywołanie funkcji
        result = fetch_and_save_inflation_data('ALPHA_VANTAGE_API_KEY')

        # Sprawdzenie wyniku
        self.assertEqual(result, 'CPI data fetched and saved successfully.') 
        

    @patch('services.requests.get')
    def test_fetch_and_save_inflation_data_failure(self, mock_get):
        # Symulacja błędu sieciowego
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        # Wywołanie funkcji
        result = fetch_and_save_inflation_data('ALPHA_VANTAGE_API_KEY')

        # Sprawdzenie wyniku
        self.assertIsNotNone(result)
        self.assertIn("Request Exception", result)

class TestInterestRatesData(unittest.TestCase):

    def setUp(self):
        self.app = create_app()  # Utwórz instancję aplikacji
        self.app_context = self.app.app_context()  # Utwórz kontekst aplikacji
        self.app_context.push()  # Aktywuj kontekst aplikacji

    def tearDown(self):
        self.app_context.pop()  # Usuń kontekst aplikacji po zakończeniu testu
    @patch('services.requests.get')
    def test_fetch_and_save_interest_rate_data_success(self, mock_get):
        # Przygotowanie danych testowych
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Effective Federal Funds Rate",
            "interval": "monthly",
            "unit": "percent",
            "data": [
                {
                    "date": "2023-10-01",
                    "value": "5.33"
                },
                {
                    "date": "2023-09-01",
                    "value": "5.33"
                },
            ]
        }

        # Wywołanie funkcji
        result = fetch_and_save_interest_rates_data('ALPHA_VANTAGE_API_KEY')

        # Sprawdzenie wyniku
        self.assertEqual(result, 'Interest rates data fetched and saved successfully.') 
        

    @patch('services.requests.get')
    def test_fetch_and_save_interest_rates_data_failure(self, mock_get):
        # Symulacja błędu sieciowego
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        # Wywołanie funkcji
        result = fetch_and_save_interest_rates_data('ALPHA_VANTAGE_API_KEY')

        # Sprawdzenie wyniku
        self.assertIsNotNone(result)
        self.assertIn("Request Exception", result)

if __name__ == '__main__':
    unittest.main()