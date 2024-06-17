from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/', methods=["POST"])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']

    print(f"Amount: {amount}")
    print(f"Target Currency: {target_currency}")
    print(f"Source Currency: {source_currency}")

    conversion_rate = convert_currency_fetch(source_currency, target_currency)

    if conversion_rate is not None:
        converted_amount = amount * conversion_rate
        response_text = f"{amount} {source_currency} is equal to {converted_amount:.2f} {target_currency}."
    else:
        response_text = "Sorry, I couldn't fetch the conversion rate at the moment."

    return jsonify({'fulfillmentText': response_text})


def convert_currency_fetch(source, target):
    api_key = "fca_live_mxtXHEm1KMuTDNb1udrI1kjrEirWKFZ8xB6OZcd2"
    url = f"https://api.freecurrencyapi.com/v1/latest?apikey={api_key}&base_currency={source}&currencies={target}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and target in data['data']:
            return data['data'][target]
        else:
            print(f"Conversion rate for {source} to {target} not found in the response.")
            return None
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


if __name__ == "__main__":
    app.run(debug=True)
