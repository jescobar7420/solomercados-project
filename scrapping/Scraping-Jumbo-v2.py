""" 
    Libraries
"""
import pandas as pd
import pandas.io.sql as sqlio
import psycopg2
from os.path import exists
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from time import sleep
from datetime import date
from selenium import webdriver
from threading import Thread, Barrier


""" 
    Global variables
"""

MAIN_PATH = 'E:/Universidad/Asignaturas/Taller Ingeniería de Software/solomercados-project/scrapping'
DIRECTORY_PATH = '/Jumbo/'
MAIN_URL = 'https://www.jumbo.cl'
NAME_SUPERMARKET = 'Jumbo'
ID_SUPERMARKET = 2

# XPATHs
XPATH_NAVBAR = '//*[@id="root"]/div/header/div[3]/nav/div/div[2]/div[2]/a'

# CLASS_NAME
CLASS_FEATURES_CONTAINER = 'technical-information-flags-container'
CLASS_FEATURES_CONTAINER_TITLE = 'technical-information-flags-title-container'
CLASS_FEATURES_CONTAINER_VALUE = 'technical-information-flags-value-container'
CLASS_FEATURES_TITLE = 'technical-information-flags-title'
CLASS_FEATURES_VALUE = 'technical-information-flags-value'
CLASS_BRAND = 'product-brand'
CLASS_PRODUCT_INFO = 'product-info-wrapper'
CLASS_PRODUCT_SINGLE_PRICE = 'product-sigle-price-wrapper'
CLASS_PRODUCT_PRICE = 'price-product-value'
CLASS_PRODUCT_BEST_PRICE = 'price-best'
CLASS_PRODUCT_NO_STOCK = 'no-stock-text'
CLASS_PRODUCT_INGREDIENTES = 'product-ingredients-text'
CLASS_PRODUCT_DESCRIPTION = 'product-description-content'
CLASS_PRODUCT_IMAGE = 'zoomed-image'
CLASS_PRODUCT_NAME = 'product-name'
CLASS_PRODUCT_ERROR = 'error-404-empty-message'
CLASS_PRODUCT_CARD = 'shelf-product-island'
CLASS_PRODUCT_CARD_IMAGE = 'shelf-wrap-image'
CLASS_PAGE_NUMBER = 'page-number'
CLASS_NAVBAR_TITLES = 'new-header-supermarket-title'
CLASS_NAVBAR_DROPDOWN = 'new-header-supermarket-dropdown-item-name'

# THREADHS
TOTAL_THREADS = 4

# DATABASE
DB_USER = 'postgres'
DB_HOST = 'localhost'
DB_DATABASE = 'solomercados3'
DB_PASS = 123
DB_PORT = 5432


# COLUMNS
COLUMNS_CATEGORIES = ['id_category', 'category']
COLUMNS_ERROR = ['url_product', 'category', 'id_supermarket']


""" 
    Methods Database
"""

def connect_database():
    connection = psycopg2.connect(user=DB_USER,
                                  password=DB_PASS,
                                  host=DB_HOST,
                                  port=DB_PORT,
                                  database=DB_DATABASE)
    cursor = connection.cursor()
    return connection, cursor


def execute_command_database(connection, cursor, query):
    try:
        cursor.execute(query)
        connection.commit()
        return True
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return False


def insert_into_categorias(connection, cursor, category):
    query = """ INSERT INTO public.categorias(
            	categoria)
            	VALUES ('{}'); """.format(category)
    return execute_command_database(connection, cursor, query)


def get_id_table(cursor, column_id, table_name, column_name, condition):
    query = """ SELECT {} FROM {}
                WHERE {} = '{}'""".format(column_id, table_name, column_name, condition)
    try:
        cursor.execute(query)
        return cursor.fetchall()[0]
    except:
        return None


def exists_row_database(cursor, column_name, table_name, condition):
    query = """ SELECT {} FROM {}
                WHERE {} = '{}'""".format(column_name, table_name, column_name, condition)
    try:
        cursor.execute(query)
        if len(cursor.fetchall()) > 0:
            return True
        else:
            return False
    except:
        return None


def insert_into_productos(connection, cursor, id_category, id_brand, id_type_product, name_product, image_product, description, ingredients):
    query = """ INSERT INTO public.productos(
            	categoria, marca, tipo_producto, nombre, imagen, descripcion, ingredientes)
            	VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}'); """.format(id_category, id_brand, id_type_product, name_product, image_product, description, ingredients)
    return execute_command_database(connection, cursor, query)


def insert_into_marcas(connection, cursor, brand):
    query = """ INSERT INTO public.marcas(
            	marca)
            	VALUES ('{}'); """.format(brand)
    return execute_command_database(connection, cursor, query)


def insert_into_tipos(connection, cursor, type_product):
    query = """ INSERT INTO public.tipos(
            	tipo)
            	VALUES ('{}'); """.format(type_product)
    return execute_command_database(connection, cursor, query)


def insert_into_categorias(connection, cursor, category):
    query = """ INSERT INTO public.categorias(
            	categoria)
            	VALUES ('{}'); """.format(category)
    return execute_command_database(connection, cursor, query)
    

def insert_into_supermercados(connection, cursor, logo):
    query = """ INSERT INTO public.supermercados(
            	supermercado, logo)
            	VALUES ('{}', '{}'); """.format(NAME_SUPERMARKET, logo)
    return execute_command_database(connection, cursor, query)


def insert_into_supermercados_productos(connection, cursor, id_supermarket, id_product, sale_price, normal_price, url_product, scrap_date, stock):
    query = """ INSERT INTO public.supermercados_productos(
            	id_supermercado, id_producto, precio_oferta, precio_normal, url_product, fecha, disponibilidad)
            	VALUES ({}, {}, '{}', '{}', '{}', '{}', '{}'); """.format(id_supermarket, id_product, sale_price, normal_price, url_product, scrap_date, stock)
    return execute_command_database(connection, cursor, query)


def exists_row_database_two_conditions(cursor, column_name1, column_name2, table_name, condition1, condition2):
    query = """ SELECT {} FROM {}
                WHERE {} = '{}' AND {} = '{}'""".format(column_name1, table_name, column_name1, condition1, column_name2, condition2)
    try:
        cursor.execute(query)
        if len(cursor.fetchall()) > 0:
            return True
        else:
            return False
    except:
        return None


def update_table(connection, cursor, table_name, column_condition_name, column_set_name, condition, value):
    query = """ UPDATE {} SET {} = '{}' WHERE {} = '{}'""".format(table_name, column_set_name, value, column_condition_name, condition)
    return execute_command_database(connection, cursor, query)


""" 
    Categories Functions
"""

def get_all_url_from_elements(list_elements):
    list_url = []
    for item in list_elements:
        if item.text != 'Exclusivo en Jumbo' and item.get('href') != '/':
            url = MAIN_URL + item.get('href')
            list_url.append(url)
    return list_url


def get_categories(connection, cursor, df_categories):
    # Try to open Chrome
    while True:
        try:
            driver = webdriver.Chrome(MAIN_PATH + '/chromedriver2.exe')
            driver.set_window_size(1280, 720)
            driver.get(MAIN_URL)
            sleep(1)
            break
        except:
            print('Error open Chrome, wait 10 seconds...')
            sleep(10)
            pass
    
    # Hover Navbar
    navbar_element = driver.find_element_by_xpath(XPATH_NAVBAR)
    hover = ActionChains(driver).move_to_element(navbar_element)
    hover.perform()
    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    categories_supermarket = soup.find_all('a', class_ = CLASS_NAVBAR_DROPDOWN)
    categories_navbar = soup.find_all('a', class_ = CLASS_NAVBAR_TITLES)
    categories = categories_supermarket + categories_navbar
      
    # Remove categories are void and get data of all categories
    for item in categories:
        if item.text != 'Exclusivo en Jumbo' and item.get('href') != '/' and exists_row_database(cursor, 'categoria', 'categorias', (item.text).upper()) == False:
            # Insert into DataFrame
            if insert_into_categorias(connection, cursor, (item.text).upper()) == True:
                # Insert into DataFrame
                id_category = get_id_table(cursor, 'id_categoria', 'categorias', 'categoria', (item.text).upper())
                data = [id_category, (item.text).upper()]
                df_row = pd.DataFrame(data=[data], columns=COLUMNS_CATEGORIES)
                df_categories = pd.concat([df_categories, df_row], ignore_index=True)
    
    # Create a DataFrame for this supermarket
    df_categories_supermarket = get_data_categories_supermarket(connection, cursor, df_categories, categories)
    
    # Get all URLs from categories
    list_url = get_all_url_from_elements(categories)
    
    # Close driver
    driver.quit()
    
    return df_categories, df_categories_supermarket, list_url


def get_data_categories_supermarket(connection, cursor, df_categories, categories_element):   
    # Remove categories are void and get data of all categories
    for item in categories_element:
        if item.text != 'Exclusivo en Jumbo' and item.get('href') != '/' and exists_row_database(cursor, 'categoria', 'categorias', (item.text).upper()) == True:
            df_row = sqlio.read_sql_query("SELECT id_categoria AS id_category, categoria AS category FROM categorias WHERE categoria = '{}'".format((item.text).upper()), connection)
            df_categories = pd.concat([df_categories, df_row], ignore_index=True)
    return df_categories
    

def get_all_pages_category(soup, url_category):
    list_pages_categories = []
    # Count total pages, if it has
    total_pages = soup.find_all('button', class_ = CLASS_PAGE_NUMBER)
    if len(total_pages) > 0:
        for i in range(1, int(total_pages[-1].text) + 1):
            # Get link from all pages
            list_pages_categories.append(url_category + '?page={}'.format(i))
    else:
        list_pages_categories.append(url_category)
    return list_pages_categories


def get_all_products_category(browser, pages_categories):
    list_url_products = []
    # Get url of all categories
    for page in pages_categories:
        # Connect to page category
        while True:
            try:
                browser.get(page)
                sleep(5)
                break
            except:
                pass
        
        # Get url of all products from page category
        soup = BeautifulSoup(browser.page_source, 'lxml')
        for i in soup.find_all('div', class_ = CLASS_PRODUCT_CARD):
            url_product = MAIN_URL + i.find('a', CLASS_PRODUCT_CARD_IMAGE).get('href')
            list_url_products.append(url_product)
    return list_url_products


""" 
    Tools Functions
"""

def clear_text(text):
    text_clear = text.replace("'", "`")
    return text_clear


def create_row_error_product(url_product, category, id_supermarket, columns):
    data = [str(url_product), str(category), str(id_supermarket)]
    dataframe = pd.DataFrame(data=[data], columns=columns)
    return dataframe


def clear_price(price):
    price_clean = price.replace('.', '')
    price_clean = price_clean.replace('$', '')
    return price_clean 


def clear_url_image(image):
    # Find start and end of url
    start = image.find('(') + 1
    end = image.find(')')
    
    # Get the url
    image_clean = image[start:end]
    image_clean = image_clean.replace('"', '')
    return image_clean


""" 
    BeautifulSoup Functions
"""

def find_text_by_class_beautifulsoup(soup, tag, class_name):
    try:
        data = soup.find(tag, class_ = class_name).text
    except:
        data = 'NA'
    return data


def find_all_by_class_beautifulsoup(soup, tag, class_name):
    try:
        data = soup.find_all(tag, class_ = class_name)
    except:
        data = 'NA'
    return data


def get_data_product_beautifulsoup(soup, url_product):
    # If the product can't load or the product already exists
    error_product = find_text_by_class_beautifulsoup(soup, 'div', CLASS_PRODUCT_ERROR)
    if error_product != 'NA' or error_product == '':
        print('\tError read product - {}'.format(url_product))
        return 'NA'
    
    # Get data of the product
    name_product = (find_firts_text_element_by_class_beautifulsoup(soup, 'h1', CLASS_PRODUCT_NAME)).upper()
    if name_product == 'NA' or name_product == '':
        name_product = (find_text_by_class_beautifulsoup(soup, 'h1', CLASS_PRODUCT_NAME)).upper()
        if name_product == 'NA' or name_product == '':
            print('\tError read product - {}'.format(url_product))
            return 'Error read'
    name_product = clear_text(name_product)
    
    # URL of the image is in the style of a div
    image_product = find_by_class_beautifulsoup(soup, 'div', CLASS_PRODUCT_IMAGE)
    if image_product != 'NA' and image_product != '' and type(image_product) != 'NoneType':
        try:
            image_product = image_product.get('style')
            image_product = clear_url_image(image_product)
        except:
            image_product = 'NA'
       
    # Description can has two different xpath
    description1 = find_text_by_class_beautifulsoup(soup, 'p', '')
    description2 = find_text_by_class_beautifulsoup(soup, 'div', CLASS_PRODUCT_DESCRIPTION)
    
    description_product = 'NA'
    if description1 != 'NA' and description1 != '':
        if description_product == 'NA':
            description_product = description1
        else:
            description_product += description1
    
    if description2 != 'NA' and description2 != '':
        if description_product == 'NA':
            description_product = description2
        else:
            description_product += ' ' + description1
    
    ingredients = find_text_by_class_beautifulsoup(soup, 'div', CLASS_PRODUCT_INGREDIENTES)
    if ingredients == '':
        ingredients == 'NA'
    
    data = [str(clear_text(name_product)),
            str(image_product),
            str(clear_text(description_product)),
            str(clear_text(ingredients))]
    return data


def find_firts_element_by_class_beautifulsoup(soup, tag, class_name):
    try:
        data = soup.find_all(tag, class_ = class_name)[0]
    except:
        data = 'NA'
    return data


def find_all_by_class_beautifulsoup(soup, tag, class_name):
    try:
        data = soup.find_all(tag, class_ = class_name)
    except:
        data = 'NA'
    return data


def find_by_class_beautifulsoup(soup, tag, class_name):
    try:
        data = soup.find(tag, class_ = class_name)
    except:
        data = 'NA'
    return data


def find_firts_text_element_by_class_beautifulsoup(soup, tag, class_name):
    try:
        data = soup.find_all(tag, class_ = class_name)[0].text
    except:
        data = 'NA'
    return data
    

def get_data_superproduct_beautifulsoup(soup):
    box_data = find_firts_element_by_class_beautifulsoup(soup, 'div', CLASS_PRODUCT_INFO)
    if box_data == 'NA':
        box_data = find_by_class_beautifulsoup(soup, 'div', CLASS_PRODUCT_INFO)
    
    # Get prices
    sale_price = find_firts_text_element_by_class_beautifulsoup(box_data, 'span', CLASS_PRODUCT_BEST_PRICE)  
    sale_price = clear_price(sale_price)
    if sale_price == '':
        sale_price == 'NA'
    
    normal_price = find_text_by_class_beautifulsoup(box_data, 'span', CLASS_PRODUCT_SINGLE_PRICE)
    if normal_price == 'NA':
        normal_price = find_text_by_class_beautifulsoup(box_data, 'span', CLASS_PRODUCT_PRICE)
    normal_price = clear_price(normal_price)
    if normal_price == '':
        normal_price == 'NA'
    
    # If the tag exists, the product is out of stock
    available = find_text_by_class_beautifulsoup(soup, 'span', CLASS_PRODUCT_NO_STOCK)
    if available == 'NA' or available == '':
        stock = 'Yes'
    else:
        stock = 'No'
    
    data = [str(sale_price),
            str(normal_price),
            str(stock)]
    return data


""" 
    Main Scrap Data
"""

def scraping_data(connection, cursor, url_category, category, id_category, df_error_products, barrier):
    # Try to open Chrome
    while True:
        try:
            driver = webdriver.Chrome(MAIN_PATH + '/chromedriver2.exe')
            driver.set_window_size(1280, 720)
            driver.get(url_category)
            sleep(3)
            break
        except:
            print('Error open Chrome, wait 10 seconds...')
            sleep(10)
            pass
    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    pages_categories = get_all_pages_category(soup, url_category)
    
    print('Wait for others...')
    barrier.wait()
    
    list_url_products = get_all_products_category(driver, pages_categories)
    
    for url_product in list_url_products:
        # Try to connect to product details
        while True:
            try:
                driver.get(url_product)
                sleep(1)
                break
            except:
                print('Error connect {}'.format(url_product))
                sleep(10)
                pass
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        # Try to get data from product
        attemps = 0
        while attemps < 3:
            # Add to database if doesn't exists and get its id
            brand_product = clear_text((find_text_by_class_beautifulsoup(soup, 'a', CLASS_BRAND)).upper())
            if brand_product != '' and exists_row_database(cursor, 'marca', 'marcas', brand_product) == False:
                if insert_into_marcas(connection, cursor, brand_product) == True:
                    flag_brand = True
            else:
                flag_brand = False
            id_brand = get_id_table(cursor, 'id_marca', 'marcas', 'marca', brand_product)[0]
            
            # Search type of product if exists
            type_product = 'NA'
            list_features = find_all_by_class_beautifulsoup(soup, 'div', CLASS_FEATURES_CONTAINER)
            for item in list_features:
                try:
                    if item.find('span', class_ = CLASS_FEATURES_CONTAINER_TITLE).text == 'Tipo de Producto':
                        type_product = clear_text((item.find('span', class_ = CLASS_FEATURES_CONTAINER_VALUE).text).upper())
                except:
                    try:
                        if item.find('span', class_ = CLASS_FEATURES_TITLE).text == 'Tipo de Producto':
                            type_product = clear_text((item.find('span', CLASS_FEATURES_VALUE).text).upper())
                    except:
                        type_product = 'NA'

            # Add to database if doesn't exists and get its id
            if type_product != '' and exists_row_database(cursor, 'tipo', 'tipos', type_product) == False:
                if insert_into_tipos(connection, cursor, type_product) == True:
                    flag_type = True
            else:
                flag_type = False
            id_type = get_id_table(cursor, 'id_tipo', 'tipos', 'tipo', type_product)[0]
            
            data_product = get_data_product_beautifulsoup(soup, url_product)
            if data_product == 'Error read':
                attemps += 1
                # Reload page
                while True:
                    try:
                        driver.get(url_product)
                        sleep(3)
                        soup = BeautifulSoup(driver.page_source, 'lxml')
                        break
                    except:
                        sleep(10)
                        pass
            elif data_product == 'NA':
                break
            else:
                break
        
        # Get product details
        if data_product == 'NA':
            tmp_df = create_row_error_product(url_product, category, ID_SUPERMARKET, COLUMNS_ERROR)
            df_error_products = pd.concat([df_error_products, tmp_df], ignore_index=True)
            continue
        
        # Add product if doesn't exists in database
        if exists_row_database(cursor, 'nombre', 'productos', data_product[0]) == False:
            if insert_into_productos(connection, cursor, id_category, id_brand, id_type, data_product[0], data_product[1], data_product[2], data_product[3]) == True:
                flag_product = True
        else:
            id_product = get_id_table(cursor, 'id_producto', 'productos', 'nombre', data_product[0])[0]
            update_table(connection, cursor, 'productos', 'id_producto', 'imagen', id_product, data_product[1])
            flag_product = False
        
        # Add supermarket_product if doesn't exists in database
        id_product = get_id_table(cursor, 'id_producto', 'productos', 'nombre', data_product[0])[0]
        data_superproduct = get_data_superproduct_beautifulsoup(soup)
        if exists_row_database_two_conditions(cursor, 'id_producto', 'id_supermercado', 'supermercados_productos', id_product, ID_SUPERMARKET) == False:
            scrap_date = date.today()
            
            if insert_into_supermercados_productos(connection, cursor, ID_SUPERMARKET, id_product, data_superproduct[0], data_superproduct[1], url_product, scrap_date, data_superproduct[2]) == True:
                flag_superproduct = True
            else:
                flag_superproduct = False
        print('> {} - {} - ${} > ${}'.format(data_product[0], brand_product, data_superproduct[1], data_superproduct[0]))
    
    # Close Chrome
    driver.quit()



def main():
    # Connect database
    connection, cursor = connect_database()
    
    # Read data and insert into to DataFrame
    df_categories = sqlio.read_sql_query('SELECT * FROM categorias', connection)
    
    if exists(MAIN_PATH + '/Data/error_products.csv'):
        df_error_products = pd.read_csv(MAIN_PATH + '/Data/error_products.csv')
    
    # Get all data categories and return a URLs list from them
    df_categories, df_categories_supermarket, list_url_categories = get_categories(connection, cursor, df_categories)

    # Threads
    threads = []
    
    # Barrier
    barrier = Barrier(TOTAL_THREADS)
    
    total_categories = len(list_url_categories)
    indice = 0
    
    while indice < total_categories:
        for _ in range(TOTAL_THREADS):
            if (indice < total_categories):
                url_category = list_url_categories[indice]
                id_category = str(df_categories_supermarket['id_categoria'][indice]).replace(".0", "")
                category = str(df_categories_supermarket['category'][indice])
        
                t = Thread(target=scraping_data, args=(connection, cursor, url_category, category, id_category, df_error_products, barrier)) 
                t.start()
                threads.append(t)
                
                indice += 1
            else:
                break
    
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
