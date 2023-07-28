from pymongo import MongoClient
import pandas as pd


def load_and_display_data(file_path):
    '''
    Загружает данные из CSV-файла и выводит их на экран
    :param file_path: путь к файлу
    '''
    df = pd.read_csv(file_path)
    print(df.head()) # выводим первые несколько строк для проверки


def add_cost_class(df):
    '''
    Добавляет новое поле name 'Cost_Class' в DataFrame
    :param df: pandas DataFrame
    :return: DataFrame с новым полем 'Cost_Class'
    '''
    cost_median = df['Price'].median()
    cost_25_percentile = cost_median * 0.75
    cost_75_percentile = cost_median * 1.25

    df['Cost_Class'] = 'средний'
    df.loc[df['Price'] < cost_25_percentile, 'Cost_Class'] = 'эконом'
    df.loc[df['Price'] > cost_75_percentile, 'Cost_Class'] = 'премиум'

    return df


def add_flowers_for_administration(df):
    '''
    Позволяет новое name 'Suitable_for_Administration' в DataFrame
    :param df: pandas DataFrame
    :return: DataFrame с новым полем 'Suitable_for_Administration
    '''
    df['Suitable_for_Administration'] = False
    df.loc[(df['Cost_Class'] == 'эконом') & (df['Category'] == 'Монобукеты') & (
        df['Size'] == 'XS'), 'Suitable_for_Administration'] = True
    return df


def add_composition_of_roses(df):
    '''
    Добавляет новое поле 'Composition_of_roses' в DataFrame
    :param df: pandas DataFrame
    :return: DataFrame с новым полем 'Composition_of_roses'
    '''
    df['Composition_of_roses'] = False
    df.loc[(df['Composition'] == 'Розовые розы') & (df['Composition'] == 'Розовые лилии'), 'Composition_of_roses'] = True

    return df


def write_to_mongodb(df, dbname='clean_flower_data', collname='flowers'):
    # Создаем подключение к MongoDB
    client = MongoClient('mongodb://localhost:27017/')

    db = client[dbname]
    collection = db[collname]

    grouped = df.groupby('Category')

    for name, group in grouped:
        brand_data = {'Category': name, 'Flowers': group.drop('Category', axis=1).to_dict('records')}

        collection.insert_one(brand_data)


file_path = 'flowers_data.csv'  # путь к файлу
df = pd.read_csv(file_path)  # загрузка данных

load_and_display_data(file_path)  # отображение данных

df_with_cost_class = add_cost_class(df)
print(df_with_cost_class)

df_with_flowers_for_administration = add_flowers_for_administration(df)
print(df_with_flowers_for_administration)

df_with_composition_of_roses = add_composition_of_roses(df_with_flowers_for_administration)
print(df_with_composition_of_roses)

write_to_mongodb(df_with_composition_of_roses)