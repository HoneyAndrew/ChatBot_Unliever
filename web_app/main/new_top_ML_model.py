import psycopg2
import pandas as pd
from sklearn.linear_model import QuantileRegressor
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import numpy as np


# ... (Функции для вычисления метрик остаются без изменений) ...
# Функции для вычисления метрик
def wQL(y_true, y_pred, quantile):
    return ((y_true - y_pred) * (quantile - (y_true < y_pred).astype(int))).sum() / y_true.shape[0]

def WAPE(y_true, y_pred):
    return 100 * (abs(y_true - y_pred).sum() / y_true.sum())

def RMSE(y_true, y_pred):
    return mean_squared_error(y_true, y_pred, squared=False)

def MAPE(y_true, y_pred):
    return 100 * (abs((y_true - y_pred) / y_true)).mean()

def MASE(y_true, y_pred, y_train):
    n = y_train.shape[0]
    d = abs(y_train[1:] - y_train[:-1]).sum() / (n - 1)
    errors = abs(y_pred - y_true)
    return errors.mean() / d

from sqlalchemy import create_engine

def connect_to_db():
    conn = psycopg2.connect(
        dbname="Vestrum_db",
        user="Vestrum",
        password="VestrumTeam4",
        host="rc1b-1qbg8ffrhy01sqpo.mdb.yandexcloud.net",
        port="6432"
    )
    return conn

conn = connect_to_db()
query = "SELECT * FROM products"
data = pd.read_sql(query, conn)
conn.close()

# Взять подвыборку данных (например, 10%)
data = data.sample(frac=0.1)


# Объединение столбцов 'name' и 'brand' в один текстовый столбец
data['name_brand'] = data['name'] + " " + data['brand']

# Преобразование нового столбца 'name_brand' с использованием TF-IDF
vectorizer = TfidfVectorizer()
name_features = vectorizer.fit_transform(data['name_brand'])

# Уменьшение размерности с использованием TruncatedSVD
n_components = 5
svd = TruncatedSVD(n_components=n_components)
name_features_reduced = svd.fit_transform(name_features)

# Добавление TF-IDF признаков к данным
data = pd.concat([data, pd.DataFrame(name_features_reduced)], axis=1)

# Удаление столбцов 'name', 'brand', и 'name_brand', если они больше не нужны
data = data.drop(columns=['name', 'brand', 'name_brand'])

from sklearn.impute import SimpleImputer
data = data.dropna()


# Функция для обучения квантильных моделей
def train_quantile_models(X, y, quantiles=[0.1, 0.3, 0.5, 0.7, 0.9]):
    models = []
    for quant in quantiles:
        model = QuantileRegressor(quantile=quant)
        model.fit(X, y)
        models.append(model)
    return models

# Функция для получения прогнозов от квантильных моделей
def get_quantile_predictions(models, X):
    predictions = []
    for index, row in X.iterrows():
        quantile_preds = [model.predict([row]) for model in models]
        predictions.append(quantile_preds)
    return predictions

# Разделение данных на обучающую и тестовую выборки
X = data.drop(columns=['synthetic_sales'])
y = data['synthetic_sales']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Преобразование столбца с датой в количество дней с определенной даты
reference_date = pd.Timestamp('2000-01-01')
X_train['collection_timestamp'] = (X_train['collection_timestamp'] - reference_date).dt.days

X_train.columns = X_train.columns.astype(str)

# Обучение квантильных моделей и получение прогнозов
quantile_models = train_quantile_models(X_train, y_train)
quantile_predictions = get_quantile_predictions(quantile_models, X_train)

# Объединение прогнозов с оригинальными признаками
X_train_with_quantiles = pd.concat([X_train.reset_index(drop=True), pd.DataFrame(quantile_predictions)], axis=1)

# Функция для обучения LGB модели
def train_lgbm(X_train_with_quantiles, y_train):
    params = {
        'objective': 'regression',
        'metric': 'rmse',
        'boosting_type': 'gbdt',
        'num_leaves': 31
    }
    train_data = lgb.Dataset(X_train_with_quantiles, label=y_train)
    lgb_model = lgb.train(params, train_data, num_boost_round=100)
    return lgb_model


# Обучение LightGBM модели
lgb_model = train_lgbm(X_train_with_quantiles, y_train)

# Прогнозирование на тестовой выборке с использованием квантильных моделей
quantile_predictions_test = get_quantile_predictions(quantile_models, X_test)
X_test_with_quantiles = pd.concat([X_test.reset_index(drop=True), pd.DataFrame(quantile_predictions_test)], axis=1)

# Прогнозирование и вычисление метрик
y_pred = lgb_model.predict(X_test_with_quantiles)
print("wQL:", wQL(y_test, y_pred, 0.5))
print("WAPE:", WAPE(y_test, y_pred))
print("RMSE:", RMSE(y_test, y_pred))
print("MAPE:", MAPE(y_test, y_pred))
print("MASE:", MASE(y_test, y_pred, y_train))

# Прогнозирование на тестовой выборке
quantile_predictions_test = get_quantile_predictions(quantile_models, X_test)
X_test_with_quantiles = pd.concat([X_test.reset_index(drop=True), pd.DataFrame(quantile_predictions_test)], axis=1)
y_pred = lgb_model.predict(X_test_with_quantiles)

# Добавление прогнозов и реальных значений в исходный набор данных
results = X_test.copy()
results['predicted_sales'] = y_pred
results['actual_sales'] = y_test

# Определение категорий
categories = ['beauty', 'electronics', 'products'] # Добавьте здесь свои категории

# Вывод топ-5 продуктов для каждой категории
for category in categories:
    print(f"Top 5 products for category {category}:")
    category_data = results[results['category'] == category] # Предполагается, что у вас есть столбец 'category'
    top_5_products = category_data.nlargest(5, 'predicted_sales')
    print(top_5_products[['product_id', 'predicted_sales', 'actual_sales']]) # Предполагается, что у вас есть столбец 'product_id'

from sqlalchemy import create_engine

# Создание подключения к базе данных
engine = create_engine('postgresql://Vestrum:VestrumTeam4@rc1b-1qbg8ffrhy01sqpo.mdb.yandexcloud.net:6432/Vestrum_db')

# Отправка результатов в новую таблицу
results.to_sql('results_table', engine, if_exists='replace')

