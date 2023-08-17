import psycopg2
import pandas as pd
import sklearn
import psycopg2
import ast
import datetime
import psycopg2
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostRegressor



# 1. Подключение к базе данных и загрузка данных
def connect_to_db():
    return psycopg2.connect(
        dbname="Vestrum_db",
        user="Vestrum",
        password="VestrumTeam4",
        host="rc1b-1qbg8ffrhy01sqpo.mdb.yandexcloud.net",
        port="6432"
    )

# Подключение к базе данных
conn = connect_to_db()

# Запрос к базе данных
query = "SELECT * FROM products"
data = pd.read_sql(query, conn)
data['collection_timestamp'] = (data['collection_timestamp'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1D')


# Закрытие соединения
conn.close()

## 2. Подготовка данных


from sklearn.model_selection import train_test_split

# Выделение признаков и целевой переменной
X = data[['product_id', 'collection_timestamp', 'subcategory_id', 'category_id', 'priceu', 'sale', 'feedbacks', 'reviewrating']]
y = data['synthetic_sales']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


## 3. Обучение моделей

import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostRegressor

# XGBoost
xgb_model = xgb.XGBRegressor(objective='reg:squarederror')
xgb_model.fit(X_train, y_train)

# LightGBM
lgb_model = lgb.LGBMRegressor()
lgb_model.fit(X_train, y_train)

# CatBoost
cat_model = CatBoostRegressor()
cat_model.fit(X_train, y_train)

# 4. Ансамблирование моделей

# Прогнозы отдельных моделей
xgb_pred = xgb_model.predict(X_test)
lgb_pred = lgb_model.predict(X_test)
cat_pred = cat_model.predict(X_test)

# Простое усреднение
final_pred = (xgb_pred + lgb_pred + cat_pred) / 3

# 5. Оценка и интерпретация


# Вычисление ошибок (лосса) для каждого продукта
individual_mse = [mean_squared_error([true], [pred]) for true, pred in zip(y_test, final_pred)]

# Сопоставление ошибок с продуктами
product_errors = list(zip(X_test.index, individual_mse))

# Отсортировать продукты по ошибке и выбрать топ 5
top_5_products = sorted(product_errors, key=lambda x: x[1])[:5]

# Вывести результат
print("Top 5 products with the lowest loss:")
for product_index, error in top_5_products:
    product_info = data.loc[product_index]
    print(f"Product ID: {product_info['product_id']}, Error: {error}")

# Оценка производительности
mse = mean_squared_error(y_test, final_pred)
print(f'Mean Squared Error: {mse}')



# 6. Применение к новым данным
# Новые данные (можно загрузить аналогичным образом из базы данных)
# new_data = pd.read_csv('new_data.csv')
# X_new = new_data[['feature1', 'feature2', 'feature3']]

# Прогнозы
# xgb_new_pred = xgb_model.predict(X_new)
# lgb_new_pred = lgb_model.predict(X_new)
# cat_new_pred = cat_model.predict(X_new)
# final_new_pred = (xgb_new_pred + lgb_new_pred + cat_new_pred) / 3
