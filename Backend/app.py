from flask import Flask, jsonify, render_template
from pymongo import MongoClient # type: ignore

app = Flask(__name__)

# Initialize MongoDB Client
client = MongoClient('mongodb://localhost:27017/')  # Update the URI if needed
db = client['cit_scrapy']  # Replace with your database name

# Route to serve the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch CIT news items
@app.route('/api/citnews', methods=['GET'])
def get_cit_news():
    collection = db['citnewsitem']
    data = list(collection.find({}, {'_id': 0}))  # Exclude MongoDB _id field
    return jsonify(data)

# Route to fetch IITG news items
@app.route('/api/iitgnews', methods=['GET'])
def get_iitg_news():
    collection = db['iitgnewsitem']
    data = list(collection.find({}, {'_id': 0}))
    return jsonify(data)

# Route to fetch NITS news items
@app.route('/api/nitsnews', methods=['GET'])
def get_nits_news():
    collection = db['nitsitems']
    data = list(collection.find({}, {'_id': 0}))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
