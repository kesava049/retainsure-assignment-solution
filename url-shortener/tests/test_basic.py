# tests/test_basic.py

import pytest
from app.main import app, store

@pytest.fixture(autouse=True)
def client():
    app.config['TESTING'] = True
    # Clear store before each test for isolation
    store.urls.clear()
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_api_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'

def test_shorten_url_success(client):
    response = client.post('/api/shorten', json={"url": "https://openai.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert "short_code" in data
    assert data["short_url"].endswith('/' + data["short_code"])

def test_shorten_url_invalid_missing_param(client):
    response = client.post('/api/shorten', json={})
    assert response.status_code == 400
    assert "Missing 'url' parameter" in response.get_data(as_text=True)

def test_shorten_url_invalid_url(client):
    response = client.post('/api/shorten', json={"url": "foo"})
    assert response.status_code == 400
    assert "Invalid URL" in response.get_data(as_text=True)

def test_redirect_success_and_count(client):
    # Shorten URL first
    response = client.post('/api/shorten', json={"url": "https://example.com"})
    shortcode = response.get_json()['short_code']
    # Redirect
    response2 = client.get(f'/{shortcode}', follow_redirects=False)
    assert response2.status_code == 302
    assert response2.headers['Location'] == "https://example.com"
    # Analytics check: 1 click
    stats = client.get(f'/api/stats/{shortcode}').get_json()
    assert stats['clicks'] == 1

def test_redirect_not_found(client):
    response = client.get('/abcdef')
    assert response.status_code == 404

def test_stats_success(client):
    response = client.post('/api/shorten', json={"url": "https://test.com"})
    shortcode = response.get_json()['short_code']
    stats = client.get(f'/api/stats/{shortcode}')
    assert stats.status_code == 200
    data = stats.get_json()
    assert data["url"] == "https://test.com"
    assert data["clicks"] == 0
    assert "created_at" in data

def test_stats_not_found(client):
    response = client.get('/api/stats/unknown')
    assert response.status_code == 404
    assert "Short code not found" in response.get_data(as_text=True)
