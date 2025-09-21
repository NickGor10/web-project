SITES_CONFIG = {
    "rozetka": {
        "base_url": "https://rozetka.com.ua/ua/apple-phones/c80003/",
        "selectors": {
            "item": "div.goods-tile__inner",
            "name": "a.goods-tile__heading",
            "price": "span.goods-tile__price-value",
            "link_attr": "href",
            "rating": "span.goods-tile__rating"
        }
    },
    "comfy": {
        "base_url": "https://comfy.ua/ua/smartfon/brand__apple/",
        "selectors": {
            "item": "div.product-item",
            "name": ".product-name a",
            "price": ".price-value",
            "link_attr": "href",
            "rating": ".rating"
        }
    },
    "allo": {
        "base_url": "https://allo.ua/ua/products/mobile/proizvoditel-apple/",
        "selectors": {
            "item": ".product-card",
            "name": ".product-card__title",
            "price": ".sum",
            "link_attr": "href",
            "rating": ".rating"
        }
    }
}
