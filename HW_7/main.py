from db.database import init_db
from scraper.base_scraper import BaseScraper
from scraper.sites import SITES_CONFIG
from db.models import Product

def main():
    init_db()
    print("=== Універсальний скрапер ===")
    print("Доступні сайти:", ", ".join(SITES_CONFIG.keys()))
    site = input("Виберіть сайт: ").strip()
    if site not in SITES_CONFIG:
        print("Сайт не підтримується!")
        return

    try:
        pages = int(input("Кількість сторінок: ").strip())
    except ValueError:
        pages = 1

    fields_input = input("Які дані збираємо? (name, price, link, rating) - через кому, або Enter для всіх: ").strip()
    fields = [f.strip() for f in fields_input.split(",")] if fields_input else ["name", "price", "link", "rating"]

    scraper = BaseScraper(SITES_CONFIG[site], pages=pages)
    try:
        saved = scraper.scrape(fields)
        print(f"✅ Збережено {saved} товарів.")
    except Exception as e:
        print(f"❌ Помилка під час скрапінгу: {e}")

    products = Product.get_all()
    print(f"У базі {len(products)} товарів.")
    for p in products:
        print(p)

if __name__ == "__main__":
    main()
