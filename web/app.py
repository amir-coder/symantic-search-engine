from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
from src.engine import SearchEngine


app = Flask(__name__)

print("Starting Flask server...")
engine = SearchEngine(
    datapath='data/preprocessed/clean_dataset.csv', 
    embdedings_path='data/preprocessed/plot_embeddings.npy'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/api/search", methods=['POST'])
def search_api():
    try:
        data = request.json
        start_time = time.time()
        results =   engine.search(filters=data)
        query_time = time.time() - start_time

        return jsonify({   
            "status": "success", 
            "results": results, 
            "count": len(results),
            "query_time": round(query_time, 4)
        })
    except Exception as e:
        print(f"Error during search: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)