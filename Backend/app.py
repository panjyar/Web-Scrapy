from flask import Flask, jsonify, render_template
from pymongo import MongoClient  # type: ignore
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

mongo_uri= os.getenv('MONGO_URL')
client = MongoClient(mongo_uri)
db = client['All_college']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/all', methods=['GET'])
def get_all_news():
    try:
        # Fetch data from different collections
        news = list(db['news'].find({}, {'_id': 0}))
        upcoming_events = list(db['upcoming_events'].find({}, {'_id': 0}))  
        notices = list(db['notices'].find({}, {'_id': 0}))  
        tenders = list(db['tenders'].find({}, {'_id': 0}))  

        # Combine all data into a structured format
        all_news = {
            "News": news,
            "UpcomingEvents": upcoming_events,
            "Notices": notices,
            "Tenders": tenders
        }

        return jsonify(all_news)

    except Exception as e:
        app.logger.error(f"Error fetching data: {e}")
        return jsonify({"error": "An error occurred while fetching data"}), 500

if __name__ == '__main__':
    app.run()
