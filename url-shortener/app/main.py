# app/main.py

from flask import Flask, jsonify, request, redirect, abort, url_for
from .models import URLStore        
from .utils import generate_short_code, is_valid_url


app = Flask(__name__)

store = URLStore()

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' parameter"}), 400
    long_url = data["url"].strip()
    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400
    # Generate a unique short code
    short_code = generate_short_code(store.urls)
    store.create_short_url(short_code, long_url)
    host = request.host_url.rstrip('/')
    return jsonify({
        "short_code": short_code,
        "short_url": f"{host}/{short_code}"
    }), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_short_url(short_code):
    record = store.get_url(short_code)
    if not record:
        abort(404, description="Short code not found")
    store.increment_click(short_code)
    return redirect(record["url"], code=302)

@app.route('/api/stats/<short_code>', methods=['GET'])
def url_stats(short_code):
    record = store.get_url(short_code)
    if not record:
        return jsonify({"error": "Short code not found"}), 404
    return jsonify({
        "url": record["url"],
        "clicks": record["clicks"],
        "created_at": record["created_at"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
