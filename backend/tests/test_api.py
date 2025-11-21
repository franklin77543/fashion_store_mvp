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
