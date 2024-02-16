### saxo-get-uic.py v1.0 ###

### imports section ###  
import requests
import json
### end # imports section ### 

### Application configuration ###
def load_config(filename='config.json'):  # Load application configuration from a JSON file
    """Load application configuration from a JSON file."""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None

config = load_config()
if config is None:
    exit("Failed to load configuration, terminating program.")

app_data = {
    "AppName": "saxo-get-uic",
    "AppKey": config.get("AppKey", ""),
    "OpenApiBaseUrl": "https://gateway.saxobank.com/sim/openapi/"
}
### end # Application configuration ###

### Function to resolve symbol to UIC ###
def resolve_symbol_to_uic(access_token, symbol):
    """Resolve a trading symbol to its UIC using Saxo Bank's OpenAPI."""
    url = f"{app_data['OpenApiBaseUrl']}ref/v1/instruments"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"Keywords": symbol, "AssetTypes": "Stock"}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raises an HTTPError if the response was an error
        data = response.json()
        if 'Data' in data and data['Data']:
            return data['Data'][0]['Identifier']
    except requests.RequestException as e:
        print(f"Error resolving UIC for symbol: {symbol}. Error: {e}")
    return None
### end # Function to resolve symbol to UIC ###

### Main program ###
if __name__ == "__main__":
    symbol = "AAPL"  # STOCK SYMBOL TO GET UIC FOR 
    access_token = config.get("AccessToken", "")
    if not access_token:
        print("Access token is missing in the configuration.")
        exit()
        
    uic = resolve_symbol_to_uic(access_token, symbol)
    if uic:
        print(f"Resolved UIC for {symbol}: {uic}")
    else:
        print(f"Failed to resolve UIC for symbol: {symbol}")
### end # Main program ###

### end # saxo-get-uic.py v1.0 ###
### support@sugra.systems ###