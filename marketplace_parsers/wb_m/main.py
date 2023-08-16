import pandas as pd
import requests

WB_URLS = {
    'КРАСОТА': {
        'КРАСОТА С ARAVIA': 'https://search.wb.ru/promo/bucket_24/catalog?appType=1&curr=rub&dest=-1257786&page=1&preset=163046&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'КАТАЛОГ ROYAL SAMPLES': 'https://catalog.wb.ru/brands/r/catalog?appType=1&brand=76460&curr=rub&dest=-1257786&fcolor=15631086;16776960&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'КОРЕЙСКАЯ КОСМЕТИКА': 'https://catalog.wb.ru/catalog/beauty11/catalog?appType=1&cat=58217&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'АКСЕССУАРЫ ДЛЯ КОСМЕТИКИ': 'https://catalog.wb.ru/catalog/beauty7/catalog?appType=1&cat=4872&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'АПТЕЧНАЯ КОСМЕТИКА': {
            'Коррекция признаков старения': 'https://catalog.wb.ru/catalog/beauty8/catalog?appType=1&cat=8727&curr=rub&dest=-1257786&f10829=18997;19003;31733;61603;61605;61612;67734;96105;461647;511840&fbrand=5949;7774;7776;7780;7785;7787;7789;7797;7798;10394;19492;28537;28539;41244;67782;84682;86963;88671;114969;404073&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'Жирная и проблемная кожа': 'https://catalog.wb.ru/catalog/beauty8/catalog?appType=1&cat=8727&curr=rub&dest=-1257786&f10829=20415;31732;65517;96106;96110;115706;421625;463466;466833;472193;472963;503474;629634&fbrand=5949;7774;7776;7780;7785;7787;7789;7797;7798;10394;19492;28537;28539;41244;67782;84682;86963;88671;114969;404073&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'Увлажнение и питание': 'https://catalog.wb.ru/catalog/beauty8/catalog?appType=1&cat=8727&curr=rub&dest=-1257786&f10829=19001;496044;496047&fbrand=5949;7774;7776;7780;7785;7787;7789;7797;7798;10394;19492;28537;28539;41244;67782;84682;86963;88671;114969;404073&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'Бережное очищение': 'https://catalog.wb.ru/catalog/beauty8/catalog?appType=1&cat=8727&curr=rub&dest=-1257786&fbrand=5949;7774;7776;7780;7785;7787;7789;7797;7798;10394;19492;28537;28539;41244;67782;84682;86963;88671;114969;404073&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&xsubject=359;361;362;363;366;367;370;382;950;959;1570;1929;5976',
            'Сухая и склонная к атопии кожа': 'https://catalog.wb.ru/catalog/beauty8/catalog?appType=1&cat=8727&curr=rub&dest=-1257786&fbrand=5949;7774;7776;7780;7785;7787;7789;7797;7798;10394;19492;28537;28539;41244;67782;84682;86963;88671;114969;404073&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&xsubject=362;365;377;2410',
            'Чувствительная и аллергичная кожа': 'https://catalog.wb.ru/catalog/beauty8/catalog?appType=1&cat=8727&curr=rub&dest=-1257786&f10829=31734;222869&fbrand=5949;7774;7776;7780;7785;7787;7789;7797;7798;10394;19492;28537;28539;41244;67782;84682;86963;88671;114969;404073&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&xsubject=357;359;360;362;363;364;365;366;367;370;372;377;403;436;959;1566;1923;1929;2410',
            'Восстановление и заживление': 'https://catalog.wb.ru/catalog/beauty8/catalog?appType=1&cat=8727&curr=rub&dest=-1257786&f10829=18982;31735&f56267=63524;63528;63529;63530;63621;63622;63808;65912;409395;479893&fbrand=5949;7774;7776;7780;7785;7787;7789;7797;7798;10394;19492;28537;28539;41244;67782;84682;86963;88671;114969;404073&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&xsubject=357;372;377;1921',
            'Защита от солнца': 'https://catalog.wb.ru/catalog/beauty8/catalog?appType=1&cat=8727&curr=rub&dest=-1257786&f10829=24974&fbrand=5949;7774;7776;7780;7785;7787;7789;7797;7798;10394;19492;28537;28539;41244;67782;84682;86963;88671;114969;404073&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'Уход за лицом': 'https://catalog.wb.ru/catalog/beauty8/catalog?appType=1&cat=8727&curr=rub&dest=-1257786&f56267=63524;63525;411969;438661;460791;495871&fbrand=5949;7774;7776;7780;7785;7787;7789;7797;7798;10394;19492;28537;28539;41244;67782;84682;86963;88671;114969;404073&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'Уход за телом': 'https://catalog.wb.ru/catalog/beauty8/catalog?appType=1&cat=8727&curr=rub&dest=-1257786&f56267=63528;63529;63530;65912;567272&fbrand=5949;7774;7776;7780;7785;7787;7789;7797;7798;10394;19492;28537;28539;41244;67782;84682;86963;88671;114969;404073&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'Уход за волосами': 'https://catalog.wb.ru/catalog/beauty8/catalog?appType=1&cat=8727&curr=rub&dest=-1257786&f56267=63526&fbrand=5949;7774;7776;7780;7785;7787;7789;7797;7798;10394;19492;28537;28539;41244;67782;84682;86963;88671;114969;404073&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'Уход для мам и малышей': 'https://catalog.wb.ru/catalog/beauty8/catalog?appType=1&cat=8727&curr=rub&dest=-1257786&f56267=65912;489738&fbrand=5949;7774;7776;7780;7785;7787;7789;7797;7798;10394;19492;28537;28539;41244;67782;84682;86963;88671;114969;404073&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'Уход для мужчин': 'https://catalog.wb.ru/catalog/beauty8/catalog?appType=1&cat=8727&curr=rub&dest=-1257786&f56267=63526;63530;63619;63808;65913;79544;455646;481874;567272&fbrand=5949;7774;7776;7780;7785;7787;7789;7797;7798;10394;19492;28537;28539;41244;67782;84682;86963;88671;114969;404073&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'Сыворотки': 'https://catalog.wb.ru/catalog/beauty8/catalog?appType=1&cat=8727&curr=rub&dest=-1257786&fbrand=5949;7774;7776;7780;7785;7787;7789;7797;7798;10394;19492;28537;28539;41244;67782;84682;86963;88671;114969;404073&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&xsubject=372'
        },

        'ПАРФЮМЕРИЯ': {
            'Детская парфюмерия': 'https://catalog.wb.ru/catalog/beauty3/catalog?appType=1&cat=9232&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'Женская парфюмерия': 'https://catalog.wb.ru/catalog/beauty4/catalog?appType=1&cat=9000&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'Мужская парфюмерия': 'https://catalog.wb.ru/catalog/beauty3/catalog?appType=1&cat=9001&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0'
        },
        'КОСМЕТИКА ПО УХОДУ ЗА ЛИЦОМ': 'https://catalog.wb.ru/catalog/beauty22/catalog?appType=1&cat=8976&curr=rub&dest=-1257786&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&xsubject=1526',
        'КОСМЕТИКА ДЛЯ ГУБ': 'https://catalog.wb.ru/catalog/beauty12/catalog?appType=1&cat=8944&curr=rub&dest=-1257786&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&xsubject=349',
        'НАБОРЫ ДЛЯ УХОДА': 'https://catalog.wb.ru/catalog/beauty2/catalog?appType=1&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&subject=403',
        'КОСМЕТИКА ДЛЯ ЛИЦА (BB КРЕМА)': 'https://catalog.wb.ru/catalog/beauty12/catalog?appType=1&cat=8925&curr=rub&dest=-1257786&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&xsubject=1928',
        'ЗДОРОВАЯ УЛЫБКА': 'https://search.wb.ru/promo/bucket_3/catalog?appType=1&curr=rub&dest=-1257786&preset=159711&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'МУЖСКАЯ КОСМЕТИКА': 'https://catalog.wb.ru/catalog/beauty14/catalog?appType=1&cat=8999&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'ПРОФЕССИОНАЛЬНАЯ КОСМЕТИКА': 'https://catalog.wb.ru/catalog/beauty2/catalog?appType=1&cat=7036&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'СРЕДСТВА ЗАЩИТЫ ОТ СОЛНЦА И ЗАГАРА': 'https://catalog.wb.ru/catalog/beauty9/catalog?appType=1&cat=8988&curr=rub&dest=-1257786&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&xsubject=521',
        'КОСМЕТИКА ПО УХОДУ ЗА ЛИЦОМ': 'https://catalog.wb.ru/catalog/beauty22/catalog?appType=1&cat=8976&curr=rub&dest=-1257786&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&xsubject=1526',
        'КОСМЕТИКА ДЛЯ ЛИЦА': 'https://catalog.wb.ru/catalog/beauty12/catalog?appType=1&cat=8925&curr=rub&dest=-1257786&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&xsubject=1250'
    },

    'ПРОДУКТЫ': {
        'ВКУСНЫЕ ПОДАРКИ': 'https://catalog.wb.ru/catalog/product3/catalog?appType=1&cat=58757&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'ЗЕФИР, МАРМЕЛАД, ПАСТИЛА': 'https://catalog.wb.ru/catalog/product1/catalog?appType=1&cat=62320&curr=rub&dest=-1257786&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&xsubject=2879',
        'ЧАЙ И КОФЕ': 'https://catalog.wb.ru/catalog/product1/catalog?appType=1&cat=9510&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'СЛАДОСТИ И ХЛЕБОБУЛОЧНЫЕ ИЗДЕЛИЯ': 'https://catalog.wb.ru/catalog/product1/catalog?appType=1&cat=10558&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'БАКАЛЕЯ': 'https://catalog.wb.ru/catalog/product2/catalog?appType=1&cat=10411&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'ДЕТСКОЕ ПИТАНИЕ': 'https://catalog.wb.ru/catalog/product3/catalog?appType=1&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&subject=2638',
        'ПИЩЕВЫЕ ДОБАВКИ': 'https://catalog.wb.ru/catalog/product3/catalog?appType=1&cat=60125&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'ПРОДУКТЫ ЗДОРОВОГО ПИТАНИЯ': 'https://catalog.wb.ru/catalog/product3/catalog?appType=1&cat=10299&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'МЯСНАЯ ПРОДУКЦИЯ': 'https://catalog.wb.ru/catalog/product3/catalog?appType=1&cat=62466&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'МОЛОКО И СЛИВКИ': 'https://catalog.wb.ru/catalog/product3/catalog?appType=1&cat=10305&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'НАПИТКИ': 'https://catalog.wb.ru/catalog/product3/catalog?appType=1&cat=10557&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'СНЕКИ': 'https://catalog.wb.ru/catalog/product3/catalog?appType=1&cat=10297&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'ЗАМОРОЖЕННАЯ ПРОДУКЦИЯ': 'https://catalog.wb.ru/catalog/product3/catalog?appType=1&cat=128326&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'ФРУКТЫ И ЯГОДЫ': 'https://catalog.wb.ru/catalog/product3/catalog?appType=1&cat=128327&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'ОВОЩИ': 'https://catalog.wb.ru/catalog/product3/catalog?appType=1&cat=128328&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0'
    },

    'ЭЛЕКТРОНИКА': {
        'АВТОЭЛЕКТРОНИКА': 'https://catalog.wb.ru/catalog/electronic14/catalog?appType=1&cat=9835&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'ГАРНИТУРЫ И НАУШНИКИ': 'https://catalog.wb.ru/catalog/electronic14/catalog?appType=1&cat=9468&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'ДЕТСКАЯ ЭЛЕКТРОНИКА': 'https://catalog.wb.ru/catalog/electronic19/catalog?appType=1&cat=58513&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'ИГРОВЫЕ КОНСОЛИ И ИГРЫ': {
            'ИГРОВЫЕ КОНСОЛИ': 'https://catalog.wb.ru/catalog/electronic19/catalog?appType=1&cat=130772&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'АКСЕССУАРЫ ДЛЯ ГЕЙМПАДОВ': 'https://catalog.wb.ru/catalog/electronic19/catalog?appType=1&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&subject=4030',
            'АКСЕССУАРЫ ДЛЯ КОНСОЛЕЙ': 'https://catalog.wb.ru/catalog/electronic19/catalog?appType=1&cat=9509&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'ГЕЙМПАДЫ': 'https://catalog.wb.ru/catalog/electronic19/catalog?appType=1&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&subject=524',
            'ИГРЫ': 'https://catalog.wb.ru/catalog/electronic19/catalog?appType=1&cat=10491&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0'
        },
        'КАБЕЛИ И ЗАРЯДНЫЕ УСТРОЙСТВА': 'https://catalog.wb.ru/catalog/electronic14/catalog?appType=1&cat=59132&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'МУЗЫКА И ВИДЕО': 'https://catalog.wb.ru/catalog/books3/catalog?appType=1&cat=128516&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'НОУТБУКИ И КОМПЬЮТЕРЫ': 'https://catalog.wb.ru/catalog/electronic18/catalog?appType=1&cat=9491&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'ОФИСНАЯ ТЕХНИКА': 'https://catalog.wb.ru/catalog/electronic15/catalog?appType=1&cat=58331&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'РАЗВЛЕЧЕНИЯ И ГАДЖЕТЫ': 'https://catalog.wb.ru/catalog/electronic15/catalog?appType=1&cat=9497&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'СЕТЕВОЕ ОБОРУДОВАНИЕ': 'https://catalog.wb.ru/catalog/electronic14/catalog?appType=1&cat=9846&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'ТОВАРЫ ДЛЯ БЕЗОПАСНОСТИ ДОМА': 'https://catalog.wb.ru/catalog/electronic17/catalog?appType=1&cat=9746&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'СМАРТФОНЫ И ТЕЛЕФОНЫ': {
            'SIM-КАРТЫ': 'https://catalog.wb.ru/catalog/electronic20/catalog?appType=1&curr=rub&dest=-1257786&page=2&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&subject=1258',
            'АКСЕССУАРЫ ДЛЯ СМАРТФОНОВ': 'https://catalog.wb.ru/catalog/electronic20/catalog?appType=1&cat=128550&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'АКСЕССУАРЫ ДЛЯ СЪЕМКИ': 'https://catalog.wb.ru/catalog/electronic20/catalog?appType=1&cat=9473&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'ГАРНИТУРЫ И НАУШНИКИ': 'https://catalog.wb.ru/catalog/electronic14/catalog?appType=1&cat=9468&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'ДЕРЖАТЕЛИ': 'https://catalog.wb.ru/catalog/electronic20/catalog?appType=1&cat=9476&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'ЗАПЧАСТИ ДЛЯ УСТРОЙСТВ': 'https://catalog.wb.ru/catalog/electronic20/catalog?appType=1&cat=128487&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'КАРТЫ ПАМЯТИ': 'https://catalog.wb.ru/catalog/electronic20/catalog?appType=1&cat=9467&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'МОБИЛЬНЫЕ ТЕЛЕФОНЫ': 'https://catalog.wb.ru/catalog/electronic20/catalog?appType=1&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&subject=516',
            'ПЛАНШЕТЫ': 'https://catalog.wb.ru/catalog/electronic22/catalog?appType=1&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&subject=517',
            'СМАРТФОНЫ': 'https://catalog.wb.ru/catalog/electronic22/catalog?appType=1&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&subject=515',
            'СТАЦИОНАРНЫЕ ТЕЛЕФОНЫ': 'https://catalog.wb.ru/catalog/electronic22/catalog?appType=1&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&subject=2376',
            'СТЕКЛА ЗАЩИТНЫЕ': 'https://catalog.wb.ru/catalog/electronic22/catalog?appType=1&cat=9465&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'ПЛЕНКИ ЗАЩИТНЫЕ': 'https://catalog.wb.ru/catalog/electronic21/catalog?appType=1&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&subject=453',
            'СТИЛУСЫ': 'https://catalog.wb.ru/catalog/electronic22/catalog?appType=1&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&subject=2833',
            'ШНУРКИ И КОЛЬЦА': 'https://catalog.wb.ru/catalog/electronic21/catalog?appType=1&cat=130693&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
            'FLASH-НАКОПИТЕЛИ': 'https://catalog.wb.ru/catalog/electronic22/catalog?appType=1&cat=59065&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0'
        },
        'СМАРТ ЧАСЫ И АКСЕССУАРЫ': 'https://catalog.wb.ru/catalog/electronic17/catalog?appType=1&cat=9845&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'СОЛНЕЧНЫЕ ЭЛЕКТРОСТАНЦИИ И КОМПЛЕКТУЮЩИЕ': 'https://catalog.wb.ru/catalog/electronic17/catalog?appType=1&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&subject=8395',
        'ТВ АУДИО ФОТО И ВИДЕО ТЕХНИКА': 'https://catalog.wb.ru/catalog/electronic13/catalog?appType=1&cat=9834&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'ТОРГОВОЕ ОБОРУДОВАНИЕ': 'https://catalog.wb.ru/catalog/electronic14/catalog?appType=1&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&subject=2479',
        'ТОВАРЫ ДЛЯ УМНОГО ДОМА': 'https://catalog.wb.ru/catalog/electronic14/catalog?appType=1&cat=7588&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0',
        'ЭЛЕКТРОСАМОКАТЫ И АКСЕССУАРЫ': 'https://catalog.wb.ru/catalog/electronic14/catalog?appType=1&cat=9240&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0'
    }
}

proxies = {
    'htttp': 'СЮДА НУЖНО ВВЕСТИ ПРОКСИ'
}


# Функция по отправке запроса к json файлу, i - индекс страницы от 1 и пока не вылетит ошибка
def get_category(i):
    url = f'https://catalog.wb.ru/catalog/beauty/catalog?appType=1&cat=8976&curr=rub&dest=-1257786&page={i}&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&xsubject=1526'

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

        # Если страницы не существует
        except Exception:
            break

        # Если такая существует, то выполняем заполнение массива
        table_of_products.append(items(response_array[i - 1]))

    # Создаем пандас фрейм
    frame = pd.DataFrame([table_of_products[i] for i in range(len(table_of_products))])
    frame.to_csv('products.csv', index=False)


if __name__ == '__main__':
    main()
