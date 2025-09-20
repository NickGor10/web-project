import sys
import os

# додаємо корінь проекту в sys.path, щоб імпорти типу from db.database працювали
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
