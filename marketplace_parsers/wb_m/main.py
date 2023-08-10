import pandas as pd
import requests


proxies = {
    'htttp': 'СЮДА НУЖНО ВВЕСТИ ПРОКСИ'
}


# Функция по отправке запроса к json файлу, i - индекс страницы от 1 и пока не вылетит ошибка
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

    # Отправляем request запрос на ссылку выше
    response = requests.get(url=url, headers=headers, proxies=proxies)

    # Возвращаем request в формате JSON
    return response.json()


# Функция по работе с JSON файлом
def items(response):
    products = []
    products_data = response.get('data', {}).get('products')

    # Проверка на полноту файла
    if products_data is not None and len(products_data) > 0:

        # Проходимся циклом по файлу с получением нужных параметров,
        for product in products_data:
            products.append({
                'brand': product.get('brand', None),
                'name': product.get('name', None),
                'sale': product.get('sale', None),
                'priceU': float(product.get('priceU', None)) / 100 if product.get('priceU', None) is not None else None,
                'salePriceU': float(product.get('salePriceU', None)) / 100 if product.get('salePriceU',
                                                                                          None) is not None else None,
                'reviewRating': product.get('reviewRating', None),
                'feedbacks': product.get('feedbacks', None),

            })

    # возвращаем массив с товарами
    return products


def main():
    response_array = []
    table_of_products = []

    # Начинаем цикл от 1 до N > 100 для перехода по страницам
    for i in range(1, 1000):

        # Пытаемся выполнить функцию по i странице
        try:
            response_array.append(get_category(i))

        #Если страницы не существует
        except Exception:
            break

        #Если такая существует, то выполняем заполнение массива
        table_of_products.append(items(response_array[i - 1]))


    #Создаем пандас фрейм
    frame = pd.DataFrame([table_of_products[i] for i in range(len(table_of_products))])
    frame.to_csv('products.csv', index=False)


if __name__ == '__main__':
    main()
