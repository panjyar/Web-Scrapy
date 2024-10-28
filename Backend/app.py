from flask import Flask, jsonify, render_template
from pymongo import MongoClient  # type: ignore

app = Flask(__name__)

# Initialize MongoDB Client
client = MongoClient('mongodb://localhost:27017/') 
db = client['cit_scrapy']  

# Route to serve the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch all categorized news items
@app.route('/api/news', methods=['GET'])
def get_all_news():
    # Fetch data from different collections
    cit_news = list(db['citnewsitem'].find({}, {'_id': 0}))
    iitg_news = list(db['iitgnewsitem'].find({}, {'_id': 0}))
    nits_news = list(db['nitsitems'].find({}, {'_id': 0}))

    # Combine all data into a structured format
    all_news = {
        "citNews": cit_news,
        "iitgNews": iitg_news,
        "nitsNews": nits_news
    }

    return jsonify(all_news)

if __name__ == '__main__':
    app.run(debug=True)
