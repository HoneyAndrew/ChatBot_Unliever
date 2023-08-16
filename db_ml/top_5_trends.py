import psycopg2

# ID продуктов, которые были выведены в топ-5
top_5_product_ids = [266040, 229144, 173981, 59673, 279535]

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="Vestrum_db",
    user="Vestrum",
    password="VestrumTeam4",
    host="rc1b-1qbg8ffrhy01sqpo.mdb.yandexcloud.net",
    port="6432"
)

# Создание курсора
cursor = conn.cursor()

# Запрос к базе данных для получения деталей о продуктах
query = f"SELECT * FROM products WHERE product_id IN {tuple(top_5_product_ids)}"
cursor.execute(query)

# Получение результатов
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]

# Преобразование результатов в список словарей
top_5_products_list = [dict(zip(columns, row)) for row in rows]

# Закрытие соединения
conn.close()

# Вывод результата
for product in top_5_products_list:
    print(product)
