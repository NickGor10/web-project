import requests
from bs4 import BeautifulSoup

class BaseScraper:
    """Базовий універсальний скрапер для e-commerce сайтів."""

    def __init__(self, site_config: dict, pages: int = 1):
        self.site_config = site_config
        self.pages = pages

    def fetch_page(self, page: int) -> str:
        """Завантажує HTML-сторінку."""
        url = self.site_config["url"].format(page=page)
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text  # Важливо, бо це використовують тести

    def parse_page(self, html: str, fields: list[str]) -> list[dict]:
        """Парсить HTML-сторінку, повертаючи список товарів."""
        soup = BeautifulSoup(html, "html.parser")
        products = []

        product_selector = self.site_config.get("selectors", {}).get("product")
        if not product_selector:
            raise ValueError("Не вказаний CSS-селектор для продуктів у site_config")

        product_elements = soup.select(product_selector)

        for product in product_elements:
            product_data = {}
            for field in fields:
                selector = self.site_config["selectors"].get(field)
                if selector:
                    el = product.select_one(selector)
                    product_data[field] = el.get_text(strip=True) if el else None
                else:
                    product_data[field] = None
            products.append(product_data)

        return products

    def parse_products(self, site_config: dict, fields: list[str]) -> list[dict]:
        """Сумісність зі старими тестами — парсить тільки першу сторінку."""
        html = self.fetch_page(1)
        return self.parse_page(html, fields)

    def scrape(self, fields: list[str]) -> None:
        """Повний цикл: fetch -> parse -> save to DB."""
        from db.models import Product  # імпорт тут, щоб уникнути циклічних залежностей

        for page in range(1, self.pages + 1):
            html = self.fetch_page(page)
            products = self.parse_page(html, fields)
            for p in products:
                Product.create(**p)
