# final_fixed_bot.py
# Сгенерировано: 2025-05-23 18:54

import random

def get_my_ads():
    return [
        {"id": 1, "title": "Дом в Соузге", "price": 19500000},
        {"id": 2, "title": "Участок 5 га в Курае", "price": 15000000},
        {"id": 3, "title": "Коттедж в Элекмонаре", "price": 89000000},
    ]

def get_market_stats(region: str):
    return {
        "region": region,
        "avg_price_per_sqm": round(random.uniform(30000, 120000)),
        "min_price": round(random.uniform(1000000, 3000000)),
        "max_price": round(random.uniform(10000000, 90000000)),
        "sample_size": random.randint(20, 100)
    }

def get_region_ads(region: str):
    return [
        {"title": f"Участок в {region}", "price": 4500000},
        {"title": f"Дом с видом на горы в {region}", "price": 18500000},
        {"title": f"База отдыха у реки в {region}", "price": 60000000},
    ]
