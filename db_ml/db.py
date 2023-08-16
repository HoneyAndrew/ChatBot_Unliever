import requests
import psycopg2
import ast
import datetime


def read_and_transform_WB_urls(filename):

    transformed_data = {}
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read().replace("WB_URLS = ", "")
        WB_URLS = ast.literal_eval(content)


    for category_name, subcategories in WB_URLS.items():
        transformed_data[category_name] = {}
        for subcategory_name, value in subcategories.items():
            if isinstance(value, dict):
                transformed_data[category_name][subcategory_name] = list(value.values())
            else:
                transformed_data[category_name][subcategory_name] = value
    print(f"Transformed data: {transformed_data}")
    return transformed_data

def connect_to_db():
    print("Connecting to the database...")
    return psycopg2.connect(
        dbname="Vestrum_db",
        user="Vestrum",
        password="VestrumTeam4",
        host="rc1b-1qbg8ffrhy01sqpo.mdb.yandexcloud.net",
        port="6432"
    )
print("Connected to the database.")

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


def add_product_to_db(cursor, product, marketplace_id, category_id, subcategory_id, subsubcategory_id):
    print(f"Adding product to DB: {product}")
    product_data = (
        datetime.datetime.now(), # Временная метка коллекции
                marketplace_id,
                subsubcategory_id,
                subcategory_id,
                category_id,
                product.get('name'),
                product.get('priceU'),
                product.get('sale'),
                product.get('brand'),
                product.get('feedbacks'),
                product.get('salepriceu'),
                product.get('reviewrating')
    )

    cursor.execute("""
    INSERT INTO Products (collection_timestamp, marketplace_id, subsubcategory_id, subcategory_id, category_id, name, priceU, sale, brand, feedbacks, salepriceu, reviewrating)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING product_id
    """, product_data)

    product_id = cursor.fetchone()[0]
    print(f"Added product: {product['name']} with ID {product_id}")







def get_category(url, page_number):
    print(f"Getting category data from URL: {url}")
    url = f'{url}&page={page_number}' # добавление номера страницы к URL
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
    print(f"Processing response: {response}")
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

def add_category_to_db(cursor, category_name):
    cursor.execute("INSERT INTO Categories (name) VALUES (%s) RETURNING category_id;", (category_name,))
    result = cursor.fetchone()
    return result[0]

def add_subcategory_to_db(cursor, subcategory_name, category_id):
    cursor.execute("INSERT INTO Subcategories (name, category_id) VALUES (%s, %s) RETURNING subcategory_id;", (subcategory_name, category_id))
    return cursor.fetchone()[0]

def add_category(cursor, category_name):
    print(f"Adding category: {category_name}")
    cursor.execute("SELECT category_id FROM Categories WHERE name = %s", (category_name,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO Categories (name) VALUES (%s) RETURNING category_id;", (category_name,))
        category_id = cursor.fetchone()[0]
    else:
        category_id = result[0]
    return category_id

def add_subcategory(cursor, subcategory_name, category_id):
    print(f"Adding subcategory: {subcategory_name}")
    cursor.execute("SELECT subcategory_id FROM Subcategories WHERE name = %s", (subcategory_name,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO Subcategories (name, category_id) VALUES (%s, %s) RETURNING subcategory_id;", (subcategory_name, category_id))
        subcategory_id = cursor.fetchone()[0]
    else:
        subcategory_id = result[0]
    return subcategory_id


def add_subsubcategory(cursor, subsubcategory_name, subcategory_id):
    print(f"Adding subsubcategory: {subsubcategory_name}")
    cursor.execute("SELECT subsubcategory_id FROM Subsubcategories WHERE name = %s", (subsubcategory_name,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO Subsubcategories (name, subcategory_id) VALUES (%s, %s) RETURNING subsubcategory_id;", (subsubcategory_name, subcategory_id))
        subsubcategory_id = cursor.fetchone()[0]
    else:
        subsubcategory_id = result[0]
    return subsubcategory_id




def add_categories_and_subcategories_to_db(conn, WB_URLS):
    cursor = conn.cursor()

    # Добавляем категории
    for category_name, subcategories in WB_URLS.items():
        category_id = add_category(cursor, category_name)

        # Добавляем подкатегории для текущей категории
        # Добавляем подкатегории для текущей категории
        # Добавляем подкатегории для текущей категории
        for subcategory_name, subsubcategories_or_url in subcategories.items():
            subcategory_id = add_subcategory(cursor, subcategory_name, category_id)
            if isinstance(subsubcategories_or_url, dict):
                # Добавляем подподкатегории для текущей подкатегории
                for subsubcategory_name, subsubcategory_url in subsubcategories_or_url.items():
                    subsubcategory_id = add_subsubcategory(cursor, subsubcategory_name, subcategory_id)



        conn.commit()
    cursor.close()

def process_products(conn, cursor, url, marketplace_id, category_id, subcategory_id, subsubcategory_id = None):
    i = 1
    while True:
        try:
            with conn:  # Здесь начинается транзакция
                response = get_category(url, i)
                products = items(response)
                if not products:
                    break
                for product in products:
                    product_id = add_product_to_db(cursor, product, marketplace_id, category_id, subcategory_id, subsubcategory_id)
                    print(f"Added product with ID {product_id}")
                i += 1
        except Exception as e:
            conn.rollback()  # Откат транзакции в случае ошибки
            print(f"Error processing products: {e}")
            break







def main():
    conn = connect_to_db()
    WB_URLS = read_and_transform_WB_urls('WBurls.txt')
    add_categories_and_subcategories_to_db(conn, WB_URLS)

    if conn is None:
        raise Exception("Failed to connect to the database.")

    with conn.cursor() as cursor:
        marketplace_name = 'Wildberries'
        cursor.execute("SELECT marketplace_id FROM Marketplaces WHERE name = %s", (marketplace_name,))
        result = cursor.fetchone()
        conn.commit()
        if result is None:
            raise Exception(f"Marketplace with name '{marketplace_name}' not found in the database.")
        marketplace_id = result[0]

        # Перебор категорий
        for category_name, subcategories in WB_URLS.items():
            cursor.execute("SELECT category_id FROM Categories WHERE name = %s", (category_name,))
            result = cursor.fetchone()
            conn.commit()
            category_id = result[0] if result else None

            # Перебор подкатегорий
            for subcategory_name, subsubcategories_or_url in subcategories.items():
                subcategory_id = add_subcategory(cursor, subcategory_name, category_id)

                if isinstance(subsubcategories_or_url, dict):
                    # Обработка подподкатегорий
                    for subsubcategory_name, subsubcategory_url in subsubcategories_or_url.items():
                        process_products(conn, cursor, subsubcategory_url, marketplace_id, category_id, subcategory_id)
                else:
                    # Обработка продуктов, если подкатегория является строкой (URL)
                    process_products(conn, cursor, subsubcategories_or_url, marketplace_id, category_id, subcategory_id)

        conn.commit()
    conn.close()
    print("Data inserted successfully!")


if __name__ == '__main__':
    main()
