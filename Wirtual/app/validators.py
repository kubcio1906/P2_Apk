
def validate_stock_data_structure(data):
   
    # Walidacja Meta Data
    meta_keys = ["1. Information", "2. Symbol", "3. Last Refreshed", "4. Interval", "5. Output Size", "6. Time Zone"]
    for key in meta_keys:
        if key not in data.get("Meta Data", {}):
            return False, f"Missing key in Meta Data: {key}"

    # Walidacja Time Series
    if "Time Series (Daily)" not in data:
        return False, "Missing Time Series data"

    for timestamp, values in data.get("Time Series (Daily)", {}).items():
        expected_keys = ["1. open", "2. high", "3. low", "4. close", "5. volume"]
        for key in expected_keys:
            if key not in values:
                return False, f"Missing key in Time Series data: {key} at {timestamp}"

    return True, "Data structure is valid"

def validate_currency_data_structure(data):
   

    # Walidacja Meta Data
    meta_keys = ["1. Information", "2. From Symbol", "3. To Symbol", "4. Output Size", "5. Last Refreshed", "6. Time Zone"]
    for key in meta_keys:
        if key not in data.get("Meta Data", {}):
            return False, f"Missing key in Meta Data: {key}"

    # Walidacja Time Series
    if "Time Series FX (Daily)" not in data:
        return False, "Missing Time Series data"

    for timestamp, values in data.get("Time Series FX (Daily)", {}).items():
        expected_keys = ["1. open", "2. high", "3. low", "4. close"]
        for key in expected_keys:
            if key not in values:
                return False, f"Missing key in Time Series data: {key} at {timestamp}"

    return True, "Data structure is valid"

def validate_commodity_data_structure(data):
   

    # Walidacja Meta Data
    meta_keys = ["name", "interval", "unit"]
    for key in meta_keys:
        if key not in data:
            return False, f"Missing key in Meta Data: {key}"

    # Walidacja Time Series
    if "data" not in data:
        return False, "Missing data section"

    for item in data["data"]:
        expected_keys = ["date", "value"]
        for key in expected_keys:
            if key not in item:
                return False, f"Missing key '{key}' in data item"

    return True, "Data structure is valid"

def validate_cpi_data_structure(data):
    

    # Walidacja Meta Data
    meta_keys = ["name", "interval", "unit"]
    for key in meta_keys:
        if key not in data:
            return False, f"Missing key in data: {key}"

    # Walidacja Time Series
    if "data" not in data:
        return False, "Missing Time Series data"

    for item in data['data']:
        expected_keys = ["date","value"]
        for key in expected_keys:
            if key not in item:
                return False, f"Missing key '{key}' in data"

    return True, "Data structure is valid"

def validate_interest_rates_data_structure(data):
   
    meta_keys = ["name", "interval", "unit"]
    for key in meta_keys:
        if key not in data:
            return False, f"Missing key in Meta Data: {key}"

    # Walidacja danych
    if "data" not in data:
        return False, "Missing 'data' section"

    for item in data["data"]:
        expected_keys = ["date", "value"]
        for key in expected_keys:
            if key not in item:
                return False, f"Missing key '{key}' in data item"

    return True, "Data structure is valid"