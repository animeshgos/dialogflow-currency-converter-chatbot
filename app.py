from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']

    cf = fetch_conversion_factor(source_currency, target_currency)
    final_amount = amount*cf
    final_amount = round(final_amount, 2)

    response = {
        'fulfillmentText': "{} {} is {} {}".format(amount, source_currency, final_amount, target_currency)
    }

    return jsonify(response)


def fetch_conversion_factor(source, target):
    url = "https://api.freecurrencyapi.com/v1/latest?apikey=jWjy435GaVzEDAIuXoNfiNEm5e3m89s5wcaOAbVA"
    response = requests.get(url)
    response = response.json()
    s = response['data'][source]
    print(s)
    t = response['data'][target]
    print(t)
    return s/t


if __name__ == "__main__":
    app.run(debug=True)
