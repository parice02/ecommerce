from pathlib import Path
import json

from webapp.settings import BASE_DIR

basket = []

product_url = "http://127.0.0.1:8001/products/"
order_url = "http://127.0.0.1:8002/orders/"
account_url = "http://127.0.0.1:8003/users/"
login_url = "http://127.0.0.1:8003/login/"


def load_user():
    CONFIG_FILE = BASE_DIR / "app/config/user.json"

    config_file = Path(CONFIG_FILE)
    if config_file.exists() and config_file.is_file():
        with open(file=CONFIG_FILE, mode="r", encoding="utf8") as file:
            return json.load(file)
    raise FileNotFoundError


def save_user(user):
    CONFIG_FILE = BASE_DIR / "app/config/user.json"

    config_file = Path(CONFIG_FILE)
    if config_file.exists() and config_file.is_file():
        with open(file=CONFIG_FILE, mode="w", encoding="utf8") as file:
            return json.dump(user, file)
    raise FileNotFoundError


user = load_user()
