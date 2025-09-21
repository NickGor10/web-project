import time
import random
import logging
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
from db.models import Product

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

BASE_URL = "https://rozetka.com.ua/ua/apple-phones/c80003/"

# Набір user-agent для ротації
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)"
    " Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/116.0.0.0 Safari/537.36",
]

class RozetkaScraper:
    def __init__(self, pages: int = 1, delay: float = 1.0, max_retries: int = 3, timeout: float = 10.0):
        self.pages = max(1, int(pages))
        self.delay = delay
        self.max_retries = max_retries
        self.timeout = timeout
        self.session = requests.Session()
        # початкові заголовки (будуть мінятися при повторних спробах)
        self.session.headers.update({
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": "uk-UA,uk;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "https://google.com/",
        })

    def fetch_page(self, page_number: int) -> str:
        url = f"{BASE_URL}?page={page_number}"
        last_exc: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(f"Fetching page {page_number} (attempt {attempt}) with UA: {self.session.headers.get('User-Agent')}")
                resp = self.session.get(url, timeout=self.timeout)
                # Якщо статус 200 — повертаємо HTML
                if resp.status_code == 200:
                    return resp.text
                # Для 403/429/5xx — пробуємо повторно з іншим UA і паузою
                logger.warning(f"Got status {resp.status_code} for {url}")
                last_exc = requests.HTTPError(f"{resp.status_code} for {url}")
            except requests.RequestException as e:
                logger.warning(f"RequestException on attempt {attempt} for {url}: {e}")
                last_exc = e

            # підготовка до повтору: інша фасада UA, довша пауза
            time.sleep(self.delay + random.random())
            # змінюємо user-agent перед наступною спробою
            self.session.headers.update({"User-Agent": random.choice(USER_AGENTS)})

        # якщо всі спроби неуспішні — викидаємо помилку
        raise last_exc or Exception("Unknown error fetching page")

    def parse_products(self, html: str, fields: List[str]) -> List[Product]:
        soup = BeautifulSoup(html, "html.parser")

        # основний селектор — fallback на інші варіанти якщо розмітка інша
        items = soup.select("div.goods-tile__inner")
        if not items:
            items = soup.select("[data-goods-id]")  # інший варіант
        products: List[Product] = []
        for item in items:
            try:
                name = None
                price = None
                link = None
                rating = None

                if "name" in fields:
                    el = item.select_one("a.goods-tile__heading") or item.select_one(".goods-tile__title")
                    if el:
                        name = el.get_text(strip=True)

                if "price" in fields:
                    p_el = item.select_one("span.goods-tile__price-value")
                    if p_el:
                        price = p_el.get_text(strip=True)

                if "link" in fields:
                    a = item.select_one("a.goods-tile__heading")
                    if a and a.has_attr("href"):
                        link = a["href"].strip()

                if "rating" in fields:
                    r_el = item.select_one("span.goods-tile__rating")
                    if r_el:
                        rating = r_el.get_text(strip=True)

                # лише якщо хоча б одне поле має значення або name існує
                if name or price or link or rating:
                    products.append(Product(name, price, link, rating))
            except Exception as e:
                logger.exception("Error parsing a product item: %s", e)
                continue
        return products

    def scrape(self, fields: List[str]):
        saved_count = 0
        for page in range(1, self.pages + 1):
            try:
                html = self.fetch_page(page)
            except Exception as e:
                logger.error(f"Skipping page {page} due to fetch error: {e}")
                continue

            products = self.parse_products(html, fields)
            logger.info(f"Parsed {len(products)} products from page {page}")
            for p in products:
                try:
                    p.save()
                    saved_count += 1
                except Exception as e:
                    logger.exception("Error saving product: %s", e)
            # пауза між сторінками
            time.sleep(self.delay + random.random())
        logger.info(f"Scraping finished, saved {saved_count} products")
        return saved_count
