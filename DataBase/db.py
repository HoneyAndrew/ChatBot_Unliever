import requests
import psycopg2

def connect_to_db():
    return psycopg2.connect(
        dbname="Vestrum_db",
        user="Vestrum",
        password="VestrumTeam4",
        host="rc1b-1qbg8ffrhy01sqpo.mdb.yandexcloud.net",
        port="6432"
    )

def get_marketplace_and_category_ids(cursor, marketplace_name, category_name):
    cursor.execute("SELECT marketplace_id FROM Marketplaces WHERE name = %s", (marketplace_name,))
    result = cursor.fetchone()
    if result is None:
        raise Exception(f"Marketplace with name '{marketplace_name}' not found in the database.")
    marketplace_id = result[0]

    cursor.execute("SELECT category_id FROM Categories WHERE name = %s", (category_name,))
    result = cursor.fetchone()
    if result is None:
        raise Exception(f"Category with name '{category_name}' not found in the database.")
    category_id = result[0]

    return marketplace_id, category_id


def add_product_to_db(cursor, product, marketplace_id, category_id):
    product_data = (
        marketplace_id,
        category_id,
        product.get('brand'),
        product.get('name'),
        product.get('sale'),
        product.get('priceU'),
        product.get('salePriceU'),
        product.get('reviewRating'),
        product.get('feedbacks')
    )
    cursor.execute("INSERT INTO Products (marketplace_id, category_id, brand, name, sale, priceU, salePriceU, reviewRating, feedbacks) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", product_data)

def get_category(i):
    url = f'https://catalog.wb.ru/catalog/beauty22/catalog?appType=1&cat=8976&curr=rub&dest=-1257786&page={i}&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&xsubject=1526'
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        "Connection": "keep - alive",
        'Origin': 'https://www.wildberries.ru',
        'Referer': 'https://www.wildberries.ru/catalog/krasota/uhod-za-kozhey/uhod-za-litsom?sort=popular&page=1&xsubject=1526&bid=81041e6b-2367-459d-acb4-4d688d2e650c',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    response = requests.get(url=url, headers=headers)
    return response.json()

def items(response):
    products = []
    products_data = response.get('data', {}).get('products')

    if products_data is not None and len(products_data) > 0:
        for product in products_data:
            products.append({
                'brand': product.get('brand', None),
                'name': product.get('name', None),
                'sale': product.get('sale', None),
                'priceU': float(product.get('priceU', None)) / 100 if product.get('priceU', None) is not None else None,
                'salePriceU': float(product.get('salePriceU', None)) / 100 if product.get('salePriceU', None) is not None else None,
                'reviewRating': product.get('reviewRating', None),
                'feedbacks': product.get('feedbacks', None),
            })
    return products

def main():
    conn = connect_to_db()

    with conn.cursor() as cursor:
        # Предположим, что для данного запроса маркетплейс и категория известны
        marketplace_name = 'Wildberries'
        category_name = 'Beauty'
        marketplace_id, category_id = get_marketplace_and_category_ids(cursor, marketplace_name, category_name)

        i = 1
        while True:
            try:
                response = get_category(i)
                products = items(response)

                # Если массив продуктов пуст, прервать цикл
                if not products:
                    break

                for product in products:
                    add_product_to_db(cursor, product, marketplace_id, category_id)

                conn.commit()

                i += 1  # Переход на следующую страницу

            except Exception:
                break

    conn.close()
    print("Data inserted successfully!")

if __name__ == '__main__':
    main()
