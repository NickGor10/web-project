import pytest
from scraper.base_scraper import BaseScraper
from db.database import init_db
from db.models import Product

# Конфіг сайту
SITES_CONFIG = {
    "allo": {
        "url": "https://fake-all-site.com/page={page}",
        "selectors": {
            "product": ".product-card",
            "name": ".product-title",
            "price": ".product-price",
            "link": ".product-title",  # отримаємо href
            "rating": ".product-rating"
        }
    }
}

MOCK_HTML = """
<html>
<body>
<div class="product-card">
  <a class="product-title" href="/product1">Product 1</a>
  <span class="product-price">1000 грн</span>
  <span class="product-rating">4.5</span>
</div>
<div class="product-card">
  <a class="product-title" href="/product2">Product 2</a>
  <span class="product-price">2000 грн</span>
  <span class="product-rating">4.7</span>
</div>
</body>
</html>
"""

@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    """Ініціалізуємо тестову SQLite-базу перед кожним тестом."""
    test_db = tmp_path / "test_products.db"
    monkeypatch.setattr("db.database", "DB_NAME", str(test_db))
    init_db()
    yield


def test_parse_products_all_fields(monkeypatch):
    """Перевірка парсингу всіх полів."""
    scraper = BaseScraper(SITES_CONFIG["allo"], pages=1)
    monkeypatch.setattr(scraper, "fetch_page", lambda page: MOCK_HTML)

    products = scraper.parse_products(SITES_CONFIG["allo"], ["name", "price", "link", "rating"])

    assert len(products) == 2
    assert products[0]["name"] == "Product 1"
    assert products[1]["price"] == "2000 грн"


def test_parse_products_partial_fields(monkeypatch):
    """Перевірка парсингу тільки частини полів."""
    scraper = BaseScraper(SITES_CONFIG["allo"], pages=1)
    monkeypatch.setattr(scraper, "fetch_page", lambda page: MOCK_HTML)

    products = scraper.parse_products(SITES_CONFIG["allo"], ["name", "link"])

    assert len(products) == 2
    assert "price" not in products[0]  # бо не запитували


def test_fetch_page(monkeypatch):
    """Перевірка що fetch_page повертає HTML."""
    scraper = BaseScraper(SITES_CONFIG["allo"], pages=1)
    monkeypatch.setattr(scraper, "fetch_page", lambda page: "<html>Test</html>")

    html = scraper.fetch_page(1)
    assert html == "<html>Test</html>"


def test_scrape_and_save(monkeypatch):
    """Повний цикл scrape -> save -> get_all."""
    scraper = BaseScraper(SITES_CONFIG["allo"], pages=1)
    monkeypatch.setattr(scraper, "fetch_page", lambda page: MOCK_HTML)

    scraper.scrape(["name", "price", "link", "rating"])
    products = Product.get_all()

    assert len(products) == 2
    assert products[0][1] == "Product 1"  # name
    assert products[1][2] == "2000 грн"  # price
