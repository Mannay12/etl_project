from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def read_from_mongodb(dbname='clean_flower_data', collname='flowers'):
    # Создаем подключение к MongoDB
    client = MongoClient('mongodb://localhost:27017/')

    db = client[dbname]
    collection = db[collname]

    cursor = collection.find()

    data = []
    for doc in cursor:
        category = doc['Category']
        for flower in doc['Flowers']:
            flower['Category'] = category
            data.append(flower)

    df = pd.DataFrame(data)

    # Выводим DataFrame
    print(df)
    return df # Возвращаем DataFrame


def filter_and_sort_flowers(df, price_form, price_to):
    # Фильтрация по цене
    df_filtered = df[(df['Price'] >= price_form) & (df['Price'] <= price_to)]

    # Выбор нужных столбцов
    df_filtered = df_filtered[['Name', 'Price']]

    # Сортировка по названию букета цветов и цене
    df_sorted = df_filtered.sort_values(['Name', 'Price'])

    return df_sorted


def filter_premium_composition_flowers(df):
    # Фильтрация по классу стоимости и по составу букета цветов
    df_filtered = df[(df['Cost_Class'] == 'премиум') & (df['Composition'] == 'Розовые розы')]

    # Выбор нужных столбцов
    df_filtered = df_filtered[['Name', 'Composition', 'Price']]

    return df_filtered


def plot_price_vs_size(df, price_from, price_to):
    # Создаем новый DataFrame, отфильтрованный по цене
    df_plot = df[(df['Price'] >= price_from) & (df['Price'] <= price_to)]

    # Получаем список уникальных категорий
    categories = df_plot['Category'].unique()

    # Создаем словарь цветов для каждого букета цветов
    cmap = plt.get_cmap('rainbow')
    colors = cmap(np.linspace(0, 1, len(categories)))
    color_dict = dict(zip(categories, colors))

    # Рисуем диаграмму
    plt.figure(figsize=(10, 6))
    for category in categories:
        df_brand = df[df['Category'] == category]
        plt.scatter(df_brand['Price'], df_brand['Size'], alpha=0.5, color=color_dict[category], label=category)

    # Добавляем название осей и заголовок
    plt.xlabel('Price')
    plt.ylabel('Size')
    plt.title('Price vs Size')

    # Добовляем легенду
    plt.legend()

    # Показывем диаграмму
    plt.show()


read_from_mongodb()
df = read_from_mongodb()
filtered_df = filter_and_sort_flowers(df, 2000, 5000)
print(filtered_df)

filtered_premium_df = filter_premium_composition_flowers(df)
print(filtered_premium_df)

plot_price_vs_size(df, 2000, 30000)