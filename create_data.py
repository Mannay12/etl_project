import random
import requests
import pandas as pd

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru,en;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://madetolove.ru',
    'Referer': 'https://madetolove.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.0.2534 Yowser/2.5 Safari/537.36',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "YaBrowser";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

categories = [
    {'name': 'Хиты продаж', 'params': {'city': '1', 'category': 'khity_prodazh', 'per_page': '24', 'page': '1'}},
    {'name': 'Монобукеты', 'params': {'city': '1', 'category': 'monobukety', 'per_page': '24', 'page': '1'}},
    {'name': 'Миксовые букеты', 'params': {'city': '1', 'category': 'miksovye_bukety', 'per_page': '24', 'page': '1'}},
    {'name': 'Для нее', 'params': {'city': '1', 'category': 'dlya_nee', 'per_page': '24', 'page': '1'}},
    {'name': 'Букеты невесты', 'params': {'city': '1', 'category': 'bukety_nevesty', 'per_page': '24', 'page': '1'}},
    {'name': '101 роза', 'params': {'city': '1', 'category': '101_roza', 'per_page': '24', 'page': '1'}},
]

catalog_description = {
    'Хиты продаж': 'Наиболее популярные и востребованные букеты и цветы.',
    'Монобукеты': 'Букеты, состоящие из одного вида цветов, что создает элегантный и минималистичный образ.',
    'Миксовые букеты': 'Букеты, состоящие из нескольких видов цветов, что создает яркий и разнообразный образ.',
    'Для нее': 'Букеты и цветы, подходящие для женщин, например, розы, лилии, пионы и т.д.',
    'Букеты невесты': 'Специальные букеты для невесты, которые могут быть выполнены в различных стилях и из разных видов цветов.',
    '101 роза': 'Особый вид букета, который состоит из 101 розы и часто дарят в особенные дни или события.'
}

composition_flower = [
    'Разноцветные розы', 'Тюльпаны разных оттенков', 'Герберы различных цветов', 'Белые лилии', 'Красные розы',
    'Розовые гвоздики', 'Лаванда и сирень', 'Ромашки и эустомы', 'Гиацинты и анемоны', 'Красные розы', 'Белые пионы',
    'Розовые лилии', 'Белые орхидеи', 'Ароматные розы и фрезии', 'Пастельные пионы и ранункулюсы', 'Красные розы',
    'Розовые розы', 'Белые розы'
]

data = {
    'Category': [],
    'Name': [],
    'Price': [],
    'Size': [],
    'Composition': [random.choice(composition_flower) for _ in range(129)],
    'Description': [],
    'Short_Description': []
}

for category in categories:
    response = requests.get('https://api.madetolove.ru/api/v2/category.php/', params=category['params'], headers=headers)
    for item in response.json()['items']:
        category_flower = category['name']
        name = item['name']
        price = item['price']
        size = item['offers_list'][0]['size']
        data['Category'].append(category_flower)
        data['Name'].append(name)
        data['Price'].append(price)
        data['Size'].append(size)

# создаем описание, которое соответствует категории и цветам
for category, name in zip(data['Category'], data['Name']):
    data['Description'].append(catalog_description[category])

# создаем краткое описание на основе описания
for i, description in enumerate(data['Description']):
    short_description = description[:30]
    if len(description) > 30:
        # Находим последнее полное слово перед 50 символами
        last_space_index = short_description.rfind(' ')
        if last_space_index != -1:
            short_description = short_description[:last_space_index]

    data['Short_Description'].append(short_description)

# конвертируем в pandas DataFrame
df = pd.DataFrame(data)

# сохраняем в файл csv
df.to_csv('flowers_data.csv', index=False)

print(df.head())
