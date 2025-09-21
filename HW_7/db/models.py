from db.database import get_connection

class Product:
    def __init__(self, name: str, price: str = None, link: str = None, rating: str = None):
        self.name = name
        self.price = price
        self.link = link
        self.rating = rating

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, price, link, rating)
            VALUES (?, ?, ?, ?)
        """, (self.name, self.price, self.link, self.rating))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, price, link, rating FROM products")
        results = cursor.fetchall()
        conn.close()
        return results
