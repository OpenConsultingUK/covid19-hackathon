from flask import Flask, request, jsonify
from flask_cors import CORS
from functions import travelinfo as tr
from risk_index import get_risk_index
import sys

app = Flask(__name__)
CORS(app)
# cors = CORS(app, resources={r"/travel_info": {"origins": "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/travel_info')
def covid_travel_info():
    source = request.args.get('source')
    destination = request.args.get('destination')
    from_airlines, to_airlines, from_text, to_text = tr.getTravelInfo(source, destination)

    if not source or not destination:
        return 'Invalid Input'
    response = jsonify({'from_airlines': from_airlines,
                    'to_airlines': to_airlines,
                    'from_text': from_text,
                    'to_text': to_text})
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    # return 'Hello World from Python Flask!'

@app.route('/risk_index')
def covid_risk_index():
    countryname = request.args.get('countryname')
    print(countryname, file=sys.stderr)
    selectiondate = request.args.get('selectiondate')
    print(selectiondate, file=sys.stderr)
    if not countryname or not selectiondate:
        return 'Invalid Input'

    result = get_risk_index(countryname, selectiondate)
    # return result
    return jsonify({'risk_index': str(result)})

app.run(host='0.0.0.0', port=5000)