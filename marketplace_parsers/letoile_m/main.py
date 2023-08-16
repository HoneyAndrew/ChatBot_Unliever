import pandas as pd
import requests


LETOILE_URLS = {
            'ПАРФЮМЕРИЯ': {
                        'ЖЕНСКАЯ ПАРФЮМЕРИЯ': 'https://www.letu.ru/s/api/product/listing/v1/products?N=1qwrtks&Nrpp=36&No=0&innerPath=mainContent%5B3%5D&resultListPath=%2Fcontent%2FWeb%2FCategories%2FBrowse%20Pages%2FDefault%20Browse%20Page%20-%20General%20Rule&pushSite=storeMobileRU',
                        'МУЖСКАЯ ПАРФЮМЕРИЯ': 'https://www.letu.ru/s/api/product/listing/v1/products?N=mcx86j&Nrpp=36&No=0&innerPath=mainContent%5B3%5D&resultListPath=%2Fcontent%2FWeb%2FCategories%2FBrowse%20Pages%2FDefault%20Browse%20Page%20Men%20-%20General%20Rule&pushSite=storeMobileRU',
                        'УНИСЕКС': 'https://www.letu.ru/s/api/product/listing/v1/products?N=17a6r03&Nrpp=36&No=0&innerPath=mainContent%5B3%5D&resultListPath=%2Fcontent%2FWeb%2FCategories%2FBrowse%20Pages%2FDefault%20Browse%20Page%20-%20General%20Rule&pushSite=storeMobileRU',
                        'НИШЕВАЯ ПАРФЮМЕРИЯ': {
                                                'Женская парфюмерия': 'https://www.letu.ru/s/api/product/listing/v1/products?N=2rig66&Nrpp=36&No=0&innerPath=mainContent%5B3%5D&resultListPath=%2Fcontent%2FWeb%2FCategories%2FBrowse%20Pages%2FDefault%20Browse%20Page%20-%20General%20Rule&pushSite=storeMobileRU',
                                                'Мужская парфюмерия': 'https://www.letu.ru/s/api/product/listing/v1/products?N=1l8mrio&Nrpp=36&No=0&innerPath=mainContent%5B3%5D&resultListPath=%2Fcontent%2FWeb%2FCategories%2FBrowse%20Pages%2FDefault%20Browse%20Page%20-%20General%20Rule&pushSite=storeMobileRU',
                                                'Унисекс': 'https://www.letu.ru/s/api/product/listing/v1/products?N=1w94bzs&Nrpp=36&No=0&innerPath=mainContent%5B3%5D&resultListPath=%2Fcontent%2FWeb%2FCategories%2FBrowse%20Pages%2FDefault%20Browse%20Page%20-%20General%20Rule&pushSite=storeMobileRU',
                                                'Scent bibliotheque': 'https://www.letu.ru/s/api/product/listing/v1/products?N=11n51yp&Nrpp=36&No=0&innerPath=mainContent%5B3%5D&resultListPath=%2Fcontent%2FWeb%2FCategories%2FBrowse%20Pages%2FDefault%20Browse%20Page%20-%20Unlimited%20Multifacets%20-%20Quiz1&pushSite=storeMobileRU'
                                                },
                        'ДЕТСКАЯ ПАРФЮМЕРИЯ': 'https://www.letu.ru/s/api/product/listing/v1/products?N=oqbcy1&Nrpp=36&No=0&innerPath=mainContent%5B3%5D&resultListPath=%2Fcontent%2FWeb%2FCategories%2FBrowse%20Pages%2FDefault%20Browse%20Page%20-%20General%20Rule&pushSite=storeMobileRU',
                            },

            'КРАСОТА': {
                        'МАКИЯЖ': 'https://www.letu.ru/s/api/product/listing/v1/products?N=164j8nn&Nrpp=36&No=0&innerPath=mainContent%5B3%5D&resultListPath=%2Fcontent%2FWeb%2FCategories%2FBrowse%20Pages%2FDefault%20Browse%20Page%20Make%20up%20Commerc%20-%20General%20Rule&pushSite=storeMobileRU',
                        'УХОД ЗА КОЖЕЙ': 'https://www.letu.ru/s/api/product/listing/v1/products?N=1v26ro5&Nrpp=36&No=0&innerPath=mainContent%5B3%5D&resultListPath=%2Fcontent%2FWeb%2FCategories%2FBrowse%20Pages%2FDefault%20Browse%20Page%20SkinCare%20-%20General%20Rule5&pushSite=storeMobileRU',
                        'ДЛЯ ВОЛОС': 'https://www.letu.ru/s/api/product/listing/v1/products?N=1to7koq&Nrpp=36&No=0&innerPath=mainContent%5B3%5D&resultListPath=%2Fcontent%2FWeb%2FCategories%2FBrowse%20Pages%2FDefault%20Browse%20For%20Hair&pushSite=storeMobileRU',
                        'АПТЕЧНАЯ КОСМЕТИКА': 'https://www.letu.ru/s/api/product/listing/v1/products?N=r7pp80&Nrpp=36&No=0&innerPath=mainContent%5B3%5D&resultListPath=%2Fcontent%2FWeb%2FCategories%2FBrowse%20Pages%2FDefault%20Browse%20Page%20-%20General%20Rule&pushSite=storeMobileRU',
                        'УХОД ЗА ПОЛОСТЬЮ РТА': 'https://www.letu.ru/s/api/product/listing/v1/products?N=xreng3&Nrpp=36&No=0&innerPath=mainContent%5B3%5D&resultListPath=%2Fcontent%2FWeb%2FCategories%2FBrowse%20Pages%2FDefault%20Browse%20Polost%20rta%20-%20Marketplace&pushSite=storeMobileRU'
                        }

            }


headers = {
    'authority': 'www.letu.ru',
    'accept': 'application/json, text/plain',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6,fr;q=0.5',
    'baggage': 'sentry-environment=prod-ru,sentry-public_key=dd1d902e97bb41b2a74f1b3085ae7b90,sentry-trace_id=1d9f1670c195477584e887fa4b853ca0,sentry-sample_rate=0.3',
    'cookie': 'anonymous_user_cart=; anonymous_user_last_viewed=; anonymous_user_wishlist=; anonymous_user_city=; COOKIE-BEARER=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ1MTYyNzQ5NjQwNjkiLCJhdXRob3JpdGllcyI6IlJPTEVfQU5PTllNT1VTIiwic2l0ZUlkIjoic3RvcmVNb2JpbGVSVSIsImlhdCI6MTY5MjIxMDQxMiwiZXhwIjoxNjkyMjk2ODEyfQ.ls8HiSFEiB_stqMbF9rR3fhN3ZM_yFbzizR6mOBeNPiPPqLN9qSq-5Whf7Jp6807781qarbnv8KmNij14NHpnw; JSESSIONID=2CdGfXi2uovTw3V2Eza1JyiqvJE_.letu-wru-03; language=ru-RU; cityDetected=true; cityGuessed=true',
    'referer': 'https://www.letu.ru/browse/parfyumeriya/zhenskaya-parfyumeriya',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '1d9f1670c195477584e887fa4b853ca0-b7c7d44ccb7f9f60-1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
    'x-promo-msg': '8CDHp8P8LUWUlktA6uNgTw'
              }