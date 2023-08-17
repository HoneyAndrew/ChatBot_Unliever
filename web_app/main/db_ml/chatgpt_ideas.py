import psycopg2
import openai

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

# Формирование текста для отправки модели
prompt_text = """Here are the top 5 trending products:
Product ID: 266040, Name: Trendy Smartwatch, Sale: 5000 units, Brand: TechGear, Feedbacks: 400 positive, Review Rating: 4.5/5
Product ID: 229144, Name: Organic Face Cream, Sale: 3000 units, Brand: NatureBeauty, Feedbacks: 350 positive, Review Rating: 4.2/5
Product ID: 173981, Name: Vegan Protein Bar, Sale: 4500 units, Brand: HealthBite, Feedbacks: 420 positive, Review Rating: 4.3/5
Product ID: 59673, Name: Eco-friendly Water Bottle, Sale: 6000 units, Brand: GreenLife, Feedbacks: 480 positive, Review Rating: 4.6/5
Product ID: 279535, Name: Wireless Noise-Canceling Headphones, Sale: 4000 units, Brand: SoundWave, Feedbacks: 390 positive, Review Rating: 4.4/5
Based on these trends, what new products can be created? Please provide detailed descriptions.:\n"""
for product in top_5_products_list:
    prompt_text += f"Product ID: {product['product_id']}, Name: {product['name']}, Sale: {product['sale']}, Brand: {product['brand']}, Feedbacks: {product['feedbacks']}, Review Rating: {product['reviewrating']}\n"


# Отправка запроса модели ChatGPT
openai_api_key = "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"
openai.api_key = openai_api_key
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt_text},
    ]
)
# Получение и вывод результата

print(response.choices[0].message['content'])