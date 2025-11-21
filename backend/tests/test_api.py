import pytest
import httpx
BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    response = httpx.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_list_products():
    response = httpx.get(f"{BASE_URL}/products?page=1&limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_product_detail():
    # 這裡假設 id=1 存在，否則可根據實際資料調整
    response = httpx.get(f"{BASE_URL}/products/1163")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert "id" in response.json()

def test_search_products():
    response = httpx.get(f"{BASE_URL}/products/search?q=shirt&page=1&limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_filter_products():
    response = httpx.get(f"{BASE_URL}/products/filter?gender=Men&page=1&limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_master_categories():
    response = httpx.get(f"{BASE_URL}/master-categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # 可選: 檢查回傳資料結構
    if response.json():
        assert "name" in response.json()[0]
        assert "display_name" in response.json()[0]

def test_recommend_exact():
    payload = {"query": "白色襯衫", "limit": 5}
    response = httpx.post(f"{BASE_URL}/recommend", json=payload, timeout=30.0)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5
    if data:
        assert "product_id" in data[0]
        assert "matchScore" in data[0]
        assert "reason" in data[0]

def test_recommend_style():
    payload = {"query": "正式商務風格", "limit": 10}
    response = httpx.post(f"{BASE_URL}/recommend", json=payload, timeout=30.0)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10
    if data:
        assert "product_id" in data[0]
        assert "reason" in data[0]

def test_recommend_occasion():
    payload = {"query": "約會穿搭推薦", "limit": 10}
    response = httpx.post(f"{BASE_URL}/recommend", json=payload, timeout=30.0)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10
    if data:
        assert "product_id" in data[0]
        assert "reason" in data[0]

def test_recommend_semantic():
    payload = {"query": "適合夏天海邊的服飾", "limit": 10}
    response = httpx.post(f"{BASE_URL}/recommend", json=payload, timeout=30.0)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10
    if data:
        assert "product_id" in data[0]
        assert "reason" in data[0]
