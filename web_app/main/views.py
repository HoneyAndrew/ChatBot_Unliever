from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'main/index.html')


def generate_items(request):
    return render(request, 'main/generator.html')


def profile(request):
    return render(request, 'main/profile.html')


def register(request):
    return render(request, 'main/register.html')


def login(request):
    return render(request, 'main/login.html')


def error_404(request):
    return render(request, 'main/404.html')


def beauty(request):
    data = {
        "name_1": 'FRESHLAND Влажные детские салфетки ДПантенол Зайка 6х120 шт с клапаном',
        "name_2": 'Vivienne Sabo Тушь для ресниц черная Cabaret Premiere тон 01',
        "name_3": 'EpilProfi Крем воск от трещин для сухой кожи',
        "name_4": 'LA ROCHE-POSAY Effaclar Гель для умывания проблемной кожи лица 400 мл',
        "name_5": 'Ollin Professional Спрей для волос 15 в 1 профессиональный с кератином, 250 мл',
        "date_1": '15.08.2023',
        "date_2": '15.08.2023',
        "date_3": '15.08.2023',
        "date_4": '15.08.2023',
        "date_5": '15.08.2023',
        "last_price_1": '350',
        "last_price_2": '540',
        "last_price_3": '420',
        "last_price_4": '1200',
        "last_price_5": '720',
        "high_price_1": '480',
        "high_price_2": '760',
        "high_price_3": '549',
        "high_price_4": '1480',
        "high_price_5": '980',
        "rate_1": '4.9',
        "rate_2": '4.9',
        "rate_3": '4.8',
        "rate_4": '4.7',
        "rate_5": '4.9',
        "count_1": '112000',
        "count_2": '980000',
        "count_3": '145000',
        "count_4": '87000',
        "count_5": '132000',
    }
    return render(request, 'main/trends/index_beauty.html', context=data)


def products(request):
    data = {
        "name_1": 'ProteinRex Протеиновые батончики Брауни без сахара Ассорти, 12 шт',
        "name_2": 'KDV Батончик Миндаль и карамель Nut and Go, 18шт по 34г',
        "name_3": 'МирФрут Чурчхела с грецким орехом ассорти, виноград, гранат абрикос',
        "name_4": 'Таёжный Бор Кедровые орехи очищенные 500 гр ',
        "name_5": 'Donat Mg Минеральная вода Donat от производителя',
        "date_1": '15.08.2023',
        "date_2": '15.08.2023',
        "date_3": '15.08.2023',
        "date_4": '15.08.2023',
        "date_5": '15.08.2023',
        "last_price_1": '1 149',
        "last_price_2": '579',
        "last_price_3": '770',
        "last_price_4": '759',
        "last_price_5": '1624',
        "high_price_1": '2016',
        "high_price_2": '2759',
        "high_price_3": '1540',
        "high_price_4": '1460',
        "high_price_5": '2499',
        "rate_1": '4.8',
        "rate_2": '4.9',
        "rate_3": '4.8',
        "rate_4": '4.7',
        "rate_5": '4.7',
        "count_1": '108000',
        "count_2": '63900',
        "count_3": '12900',
        "count_4": '128000',
        "count_5": '98900',
    }
    return render(request, 'main/trends/index_products.html', context=data)


def activity(request):
    data = {
        "name_1": '4DRC Квадрокоптер с камерой 4DRC V4 / Коптер / Дрон для детей ',
        "name_2": 'BAOFENG Радиостанция Baofeng BF-888s',
        "name_3": 'TECNO Смартфон Spark 10 Pro 4+128 Гб',
        "name_4": 'Samsung Galaxy S23+ 5G 256GB',
        "name_5": 'Microsoft Игровая консоль Xbox Series S',
        "date_1": '15.08.2023',
        "date_2": '15.08.2023',
        "date_3": '15.08.2023',
        "date_4": '15.08.2023',
        "date_5": '15.08.2023',
        "last_price_1": '4439',
        "last_price_2": '1980',
        "last_price_3": '10632',
        "last_price_4": '77992',
        "last_price_5": '26691',
        "high_price_1": '11990',
        "high_price_2": '3000',
        "high_price_3": '13990',
        "high_price_4": '99990',
        "high_price_5": '29990',
        "rate_1": '4.6',
        "rate_2": '4.8',
        "rate_3": '4.8',
        "rate_4": '5.0',
        "rate_5": '4.6',
        "count_1": '19700',
        "count_2": '24000',
        "count_3": '13800',
        "count_4": '78000',
        "count_5": '235000',
    }
    return render(request, 'main/trends/index_activity.html', context=data)


def parfum(request):
    data = {
        "name_1": 'Christine Lavoisier Parfums Туалетная воды Clutch Collection Strawberry, 14 мл',
        "name_2": 'NUX NIKA Духи по мотивам Escentric 02, 10 мл',
        "name_3": 'Extrait de Parfum Набор пробников духи женские ',
        "name_4": 'NUX NIKA Духи по мотивам Escentric 02, 10 мл',
        "name_5": 'Armoule Духи Black Opium Черный Опиум 10 мл',
        "date_1": '15.08.2023',
        "date_2": '15.08.2023',
        "date_3": '15.08.2023',
        "date_4": '15.08.2023',
        "date_5": '15.08.2023',
        "last_price_1": '352',
        "last_price_2": '468',
        "last_price_3": '690',
        "last_price_4": '468',
        "last_price_5": '475',
        "high_price_1": '480',
        "high_price_2": '900',
        "high_price_3": '2300',
        "high_price_4": '900',
        "high_price_5": '3170',
        "rate_1": '4.7',
        "rate_2": '4.8',
        "rate_3": '4.7',
        "rate_4": '4.8',
        "rate_5": '4.8',
        "count_1": '108000',
        "count_2": '828',
        "count_3": '50400',
        "count_4": '800',
        "count_5": '720',
    }
    return render(request, 'main/trends/index_parfum.html', context=data)


def it(request):
    data = {
        "name_1": 'Acer Ноутбук Acer Nitro 5 AN515-57 I785SGN (NH.QELER.005)',
        "name_2": 'MagicPro Камера видеонаблюдения уличная Wi-Fi 3MP',
        "name_3": 'ETTA High Tech Наушники беспроводные Air 2 для iPhone и Android ',
        "name_4": 'Smartx Power Bank / 30000 mah/Повер банк/Портативное зарядное',
        "name_5": 'A-Watch Смарт часы 8 / Smart Watch 8',
        "date_1": '15.08.2023',
        "date_2": '15.08.2023',
        "date_3": '1256',
        "date_4": '15.08.2023',
        "date_5": '15.08.2023',
        "last_price_1": '69300',
        "last_price_2": '2535',
        "last_price_3": '6615',
        "last_price_4": '2499',
        "last_price_5": '2033',
        "high_price_1": '99000',
        "high_price_2": '50700',
        "high_price_3": '549',
        "high_price_4": '4999',
        "high_price_5": '4066',
        "rate_1": '4.4',
        "rate_2": '4.7',
        "rate_3": '4.7',
        "rate_4": '4.7',
        "rate_5": '4.8',
        "count_1": '420',
        "count_2": '29500',
        "count_3": '92300',
        "count_4": '20100',
        "count_5": '79800',
    }
    return render(request, 'main/trends/index_it.html', context=data)


def gen_b(request):

    return render(request, 'main/generators/generator_beauty.html')


def gen_p(request):
    url = ''
    return render(request, 'main/generators/generator_beauty.html')


def gen_parf(request):
    url = ''
    return render(request, 'main/generators/generator_beauty.html')


def gen_act(request):
    url = ''
    return render(request, 'main/generators/generator_beauty.html')


def gen_it(request):
    url = ''
    return render(request, 'main/generators/generator_beauty.html')
