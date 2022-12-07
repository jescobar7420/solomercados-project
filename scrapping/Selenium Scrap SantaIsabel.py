import pandas as pd
import pandas.io.sql as sqlio
import psycopg2
from os.path import exists
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from time import sleep
from datetime import date


MAIN_PATH = 'E:/Universidad/Asignaturas/Taller Ingeniería de Software/solomercados-project/scrapping'
DIRECTORY_PATH = '/Santa Isabel/'
MAIN_URL = 'https://www.santaisabel.cl'
NAME_SUPERMARKET = 'Santa Isabel'
DB_USER = 'postgres'
DB_HOST = 'localhost'
DB_DATABASE = 'solomercados2'
DB_PASS = 123
DB_PORT = 5432


def find_text_by_class_beautifulsoup(soup, tag, class_name):
    try:
        data = soup.find(tag, class_ = class_name).text
    except:
        data = 'NA'
    return data


def find_by_class_beautifulsoup(soup, tag, class_name):
    try:
        data = soup.find(tag, class_ = class_name)
    except:
        data = 'NA'
    return data


def find_all_by_class_beautifulsoup(soup, tag, class_name):
    try:
        data = soup.find_all(tag, class_ = class_name)
    except:
        data = 'NA'
    return data


def find_firts_text_element_by_class_beautifulsoup(soup, tag, class_name):
    try:
        data = soup.find_all(tag, class_ = class_name)[0].text
    except:
        data = 'NA'
    return data


def find_firts_element_by_class_beautifulsoup(soup, tag, class_name):
    try:
        data = soup.find_all(tag, class_ = class_name)[0]
    except:
        data = 'NA'
    return data


def get_text_selenium(browser, xpath):
    try:
        data = (browser.find_element_by_xpath(xpath).text).upper()
    except:
        data = 'NA'
    return data


def get_element_selenium(browser, xpath):
    try:
        data = (browser.find_element_by_xpath(xpath))
    except:
        data = 'NA'
    return data


def clear_url_image(image):
    # Find start and end of url
    start = image.find('(') + 1
    end = image.find(')')
    
    # Get the url
    image_clean = image[start:end]
    image_clean = image_clean.replace('"', '')
    return image_clean


def clear_price(price):
    price_clean = price.replace('.', '')
    price_clean = price_clean.replace('$', '')
    return price_clean 


def exists_row_dataframe(dataframe, column, element): 
    for i in range(len(dataframe)):
        if dataframe[column][i] == element:
            return True
    return False


def get_data_product_selenium(browser, id_category, id_brand, id_type, id_product):
    # If the product can't load or the product already exists
    error_product = get_element_selenium(browser, '//*[@id="root"]/div/div[2]/main/div/div[2]')
    if error_product != 'NA':
        print('\tError read product - {}'.format(url_product))
        return 'NA'
       
    # Get data of the product
    name_product = get_text_selenium(browser, '//*[@id="root"]/div/div[2]/div/div/main/div[1]/div[2]/div[2]/h1')
    
    # URL of the image is in the style of a div
    image_product = get_element_selenium(browser, '//*[@id="root"]/div/div[2]/div/div/main/div[1]/div[1]/div/div/div[1]/div/div')
    if image_product != 'NA':
        image_product = image_product.get_attribute('style')
        image_product = clear_url_image(image_product)
       
    # Description can has two different xpath
    description1 = get_text_selenium(browser, '//*[@id="root"]/div/div[2]/div/div/main/div[3]/div[1]/div[2]')
    description2 = get_text_selenium(browser, '//*[@id="root"]/div/div[2]/div/div/main/div[3]/div[1]/div[2]/p')
    
    description_product = ''
    if description1 != 'NA' and description1 != '':
        description_product = description1
    
    if description2 != 'NA' and description2 != '':
        description_product += ' ' + description2
    
    ingredients = get_text_selenium(browser, '//*[@id="root"]/div/div[2]/div/div/main/div[3]/div[1]/div[3]/div[2]')
    
    data = [str(id_product),
            str(id_category),
            str(id_brand),
            str(id_type),
            str(name_product),
            str(image_product),
            str(description_product),
            str(ingredients)]
    return data


def clear_text(text):
    text_clear = text.replace("'", "`")
    return text_clear


def get_data_product_beautifulsoup(soup):
    # If the product can't load or the product already exists
    error_product = find_text_by_class_beautifulsoup(soup, 'div', 'error-404-empty-message')
    if error_product != 'NA' or error_product == '':
        print('\tError read product - {}'.format(url_product))
        return 'NA'
    
    # Get data of the product
    name_product = (find_firts_text_element_by_class_beautifulsoup(soup, 'h1', 'product-name')).upper()
    if name_product == 'NA' or name_product == '':
        name_product = (find_text_by_class_beautifulsoup(soup, 'h1', 'product-name')).upper()
        if name_product == 'NA' or name_product == '':
            print('\tError read product - {}'.format(url_product))
            return 'Error read'
    
    # URL of the image is in the style of a div
    image_product = find_by_class_beautifulsoup(soup, 'div', 'zoomed-image')
    if image_product != 'NA' and image_product != '' and type(image_product) != 'NoneType':
        try:
            image_product = image_product.get('style')
            image_product = clear_url_image(image_product)
        except:
            image_product = 'NA'
       
    # Description can has two different xpath
    description1 = find_text_by_class_beautifulsoup(soup, 'p', '')
    description2 = find_text_by_class_beautifulsoup(soup, 'div', 'product-description-content')
    
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
    
    ingredients = find_text_by_class_beautifulsoup(soup, 'div', 'product-ingredients-text')
    if ingredients == '':
        ingredients == 'NA'
    
    data = [str(clear_text(name_product)),
            str(image_product),
            str(clear_text(description_product)),
            str(clear_text(ingredients))]
    return data


def get_data_categories(connection, cursor, df_categories, categories_element):   
    # Remove categories are void and get data of all categories
    for item in categories_element:
        if item.get('href') != '/' and exists_row_database(cursor, 'categoria', 'categorias', (item.text).upper()) == False:
            # Insert into database
            if insert_into_categorias(connection, cursor, (item.text).upper()) == True:
                # Insert into dataframe
                id_category = get_id_table(cursor, 'id_categoria', 'categorias', 'categoria', (item.text).upper())
                data = [id_category, (item.text).upper()]
                df_row = pd.DataFrame(data=[data], columns=columns_category)
                df_categories = pd.concat([df_categories, df_row], ignore_index=True)
    return df_categories


def get_data_categories_supermarket(connection, df_categories, categories_element):   
    # Remove categories are void and get data of all categories
    for item in categories_element:
        if item.get('href') != '/' and exists_row_database(cursor, 'categoria', 'categorias', (item.text).upper()) == True:
            df_row = sqlio.read_sql_query("SELECT id_categoria AS id_category, categoria AS category FROM categorias WHERE categoria = '{}'".format((item.text).upper()), connection)
            df_categories = pd.concat([df_categories, df_row], ignore_index=True)
    return df_categories


def get_all_url_from_elements(list_elements):
    list_url = []
    for item in list_elements:
        if item.get('href') != '/':
            url = MAIN_URL + item.get('href')
            list_url.append(url)
    return list_url


def get_all_pages_category(soup, url_category):
    list_pages_categories = []
    # Count total pages, if it has
    total_pages = soup.find_all('button', class_ = 'page-number')
    if len(total_pages) > 0:
        for i in range(1, int(total_pages[-1].text) + 1):
            # Get link from all pages
            list_pages_categories.append(url_category + '?page={}'.format(i))
    else:
        list_pages_categories.append(url_category)
    return list_pages_categories


def get_item_dataframe(dataframe, column_search, column_get, item):
    for i in range(len(dataframe)):
        if dataframe[column_search][i] == item:
            return dataframe[column_get][i]
    return None


def get_all_products_category(browser, soup, url_category):
    list_url_products = []
    # Get url of all categories
    pages_categories = get_all_pages_category(soup, url_category)
    for page in pages_categories:
        # Connect to page category
        browser.get(page)
        sleep(3)
        
        # Get url of all products from page category
        soup = BeautifulSoup(browser.page_source, 'lxml')
        for i in soup.find_all('div', class_ = 'shelf-product-island'):
            url_product = MAIN_URL + i.find('a', 'shelf-wrap-image').get('href')
            list_url_products.append(url_product)
    return list_url_products
    

def save_data_csv(dataframe, name_file, columns):
    attemps = 0
    path = MAIN_PATH
    if not exists(path + name_file):
        while attemps < 10:
            try:
                dataframe.to_csv('{}/{}.csv'.format(MAIN_PATH, name_file), encoding='utf-8', index=False, columns=columns)
                print('Saved .CSV - {}.csv !^^'.format(name_file))
                break
            except:
                attemps += 1
                print('Error trying to save files... ({}/10)'.format(attemps))
    else:
        print('File already exists.')


def get_id_dataframe(dataframe, column, column_id, element):
    for i in range(len(dataframe)):
        if dataframe[column][i] == element:
            return dataframe[column_id][i]
    return None


def exists_superproduct(df, id_supermarket, id_product, date_scrap):
    for i in range(len(df)):
        if df['id_supermarket'][i] == id_supermarket and df['id_product'][i] == id_product and df['date'][i] == date_scrap:
            return True
    return False
    
    
def get_data_superproduct_selenium(browser, id_supermarket, id_product, url, date):
    sale_price = clear_price(get_text_selenium(browser, '//*[@id="root"]/div/div[2]/div/div/main/div[1]/div[2]/div[5]/div[1]/div/div[1]/span[1]'))    
    
    # If the tag exists, the product is out of stock
    available = get_text_selenium(browser, '//*[@id="root"]/div/div[2]/div/div/main/div[1]/div[2]/div[1]/span')
    if available == 'NA':
        stock = 'Yes'
    else:
        stock = 'No'
    
    # The normal price can has two different xpath
    if stock == 'Yes':
        normal_price = get_text_selenium(browser, '//*[@id="root"]/div/div[2]/div/div/main/div[1]/div[2]/div[5]/div[2]/div/div/div/span/span/span')
        if normal_price == 'NA':
            normal_price = get_text_selenium(browser, '//*[@id="root"]/div/div[2]/div/div/main/div[1]/div[2]/div[5]/div/span')
        normal_price = clear_price(normal_price)
    else:
        normal_price = 'NA'
    
    data = [str(id_supermarket),
            str(id_product),
            str(sale_price),
            str(normal_price),
            str(url),
            str(date),
            str(stock)]
    return data


def get_data_superproduct_beautifulsoup(soup):
    box_data = find_firts_element_by_class_beautifulsoup(soup, 'div', 'product-info-wrapper')
    if box_data == 'NA':
        box_data = find_by_class_beautifulsoup(soup, 'div', 'product-info-wrapper')
    
    # Get prices
    sale_price = find_firts_text_element_by_class_beautifulsoup(box_data, 'span', 'price-best')  
    sale_price = clear_price(sale_price)
    if sale_price == '':
        sale_price == 'NA'
    
    normal_price = find_text_by_class_beautifulsoup(box_data, 'span', 'product-sigle-price-wrapper')
    if normal_price == 'NA':
        normal_price = find_text_by_class_beautifulsoup(box_data, 'span', 'price-product-value')
    normal_price = clear_price(normal_price)
    if normal_price == '':
        normal_price == 'NA'
    
    # If the tag exists, the product is out of stock
    available = find_text_by_class_beautifulsoup(soup, 'span', 'no-stock-text')
    if available == 'NA' or available == '':
        stock = 'Yes'
    else:
        stock = 'No'
    
    data = [str(sale_price),
            str(normal_price),
            str(stock)]
    return data


def create_row_error_product(url_product, category, id_supermarket, columns):
    data = [str(url_product), str(category), str(id_supermarket)]
    dataframe = pd.DataFrame(data=[data], columns=columns)
    return dataframe


def execute_command_database(connection, cursor, query):
    try:
        cursor.execute(query)
        connection.commit()
        return True
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return False


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


def insert_into_supermercados_productos(connection, cursor, id_supermarket, id_product, sale_price, normal_price, url_product, date_scrap, stock):
    query = """ INSERT INTO public.supermercados_productos(
            	id_supermercado, id_producto, precio_oferta, precio_normal, url_product, fecha, disponibilidad)
            	VALUES ({}, {}, '{}', '{}', '{}', '{}', '{}'); """.format(id_supermarket, id_product, sale_price, normal_price, url_product, date_scrap, stock)
    return execute_command_database(connection, cursor, query)


def get_id_table(cursor, column_id, table_name, column_name, condition):
    query = """ SELECT {} FROM {}
                WHERE {} = '{}'""".format(column_id, table_name, column_name, condition)
    try:
        cursor.execute(query)
        return cursor.fetchall()[0]
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
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


# Connect database
connection = psycopg2.connect(user=DB_USER,
                              password=DB_PASS,
                              host=DB_HOST,
                              port=DB_PORT,
                              database=DB_DATABASE)
cursor = connection.cursor()

# MAIN
total_products = 0

# -- DataFrames --
columns_category = ['id_category', 'category']
columns_error = ['url_product', 'category', 'id_supermarket']
df_error_products = pd.DataFrame(columns=columns_error)

# Read data and insert into to dataframe
df_products = sqlio.read_sql_query('SELECT * FROM productos', connection)
df_type = sqlio.read_sql_query('SELECT * FROM tipos', connection)
df_brand = sqlio.read_sql_query('SELECT * FROM marcas', connection)
df_categories = sqlio.read_sql_query('SELECT * FROM categorias', connection)
df_super_product = sqlio.read_sql_query('SELECT * FROM supermercados_productos', connection)
df_supermarket = sqlio.read_sql_query('SELECT * FROM supermercados', connection)
if exists(MAIN_PATH + '/Data/error_products.csv'):
    df_error_products = pd.read_csv(MAIN_PATH + '/Data/error_products.csv')

# Try to connect to main website
while True:
    try:
        driver = webdriver.Chrome(MAIN_PATH + '/chromedriver2.exe')
        driver.set_window_size(1280, 720)
        driver.get(MAIN_URL)
        sleep(1)
        break
    except:
        sleep(10)
        pass

# Hover mouse in the Navbar
element_path = driver.find_element_by_xpath('//*[@id="root"]/div/header/div[3]/nav/div/div[2]/div[2]/a')
hover = ActionChains(driver).move_to_element(element_path)
hover.perform()

# Imports the HTML of the current page into python
soup = BeautifulSoup(driver.page_source, 'lxml')

# Data supermarket
if exists_row_database(cursor, 'supermercado', 'supermercados', NAME_SUPERMARKET) == False:
    # Insert database
    url_logo = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Logo_Santa_Isabel_Cencosud_transparente.svg/1200px-Logo_Santa_Isabel_Cencosud_transparente.svg.png'
    if insert_into_supermercados(connection, cursor, url_logo):
        flag_supermarket = True
    else:
        flag_supermarket = False
id_supermarket = get_id_table(cursor, 'id_supermercado', 'supermercados', 'supermercado', NAME_SUPERMARKET)[0]

# Get all categories data
categories_supermarket = soup.find_all('a', class_ = 'new-header-supermarket-dropdown-item-name')
categories_navbar = soup.find_all('a', class_ = 'new-header-supermarket-title')
categories = categories_supermarket + categories_navbar
df_categories = get_data_categories(connection, cursor, df_categories, categories)

# Get all urls from categories
list_url_categories = get_all_url_from_elements(categories)

# Create a dataframe for this supermarket
df_categories_supermarket = pd.DataFrame(columns=columns_category)
df_categories_supermarket = get_data_categories_supermarket(connection, df_categories_supermarket, categories)

# Browse all categories
for i in range(len(list_url_categories)):
    # Try to connect in category page
    while True:
        try:
            driver.get(list_url_categories[i])
            sleep(5)
            break
        except:
            sleep(10)
            pass
    soup = BeautifulSoup(driver.page_source, 'lxml')
    print('{} - {}:'.format(df_categories_supermarket['category'][i], list_url_categories[i]))
    
    # Get all urls products from category
    list_url_products = get_all_products_category(driver, soup, list_url_categories[i])
    
    cont_products_category = 0
    total_products_category = len(list_url_products)
    id_category = get_id_table(cursor, 'id_categoria', 'categorias', 'categoria', df_categories_supermarket['category'][i])[0]
    
    # Get data for all products from category
    for url_product in list_url_products:
        # Try to connect to product details
        while True:
            try:
                driver.get(url_product)
                sleep(1)
                break
            except:
                sleep(10)
                pass
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        # Try to get data from product
        attemps = 0
        while attemps < 3:
            # Add to database if doesn't exists and get its id
            brand_product = clear_text((find_text_by_class_beautifulsoup(soup, 'a', 'product-brand')).upper())
            if brand_product != '' and exists_row_database(cursor, 'marca', 'marcas', brand_product) == False:
                if insert_into_marcas(connection, cursor, brand_product) == True:
                    flag_brand = True
            else:
                flag_brand = False
            id_brand = get_id_table(cursor, 'id_marca', 'marcas', 'marca', brand_product)[0]
            
            # Search type of product if exists
            type_product = 'NA'
            list_features = find_all_by_class_beautifulsoup(soup, 'div', 'technical-information-flags-container')
            for item in list_features:
                try:
                    if item.find('span', class_ = 'technical-information-flags-title-container').text == 'Tipo de Producto':
                        type_product = clear_text((item.find('span', class_ = 'technical-information-flags-value-container').text).upper())
                except:
                    try:
                        if item.find('span', class_ = 'technical-information-flags-title').text == 'Tipo de Producto':
                            type_product = clear_text((item.find('span', 'technical-information-flags-value').text).upper())
                    except:
                        type_product = 'NA'

            # Add to database if doesn't exists and get its id
            if type_product != '' and exists_row_database(cursor, 'tipo', 'tipos', type_product) == False:
                if insert_into_tipos(connection, cursor, type_product) == True:
                    flag_type = True
            else:
                flag_type = False
            id_type = get_id_table(cursor, 'id_tipo', 'tipos', 'tipo', type_product)[0]
            
            data_product = get_data_product_beautifulsoup(soup)
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
            tmp_df = create_row_error_product(url_product, df_categories_supermarket['category'][i], id_supermarket, columns_error)
            df_error_products = pd.concat([df_error_products, tmp_df], ignore_index=True)
            cont_products_category += 1
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
        if exists_row_database_two_conditions(cursor, 'id_producto', 'id_supermercado', 'supermercados_productos', id_product, id_supermarket) == False:
            date_scrap = date.today()
            if insert_into_supermercados_productos(connection, cursor, id_supermarket, id_product, data_superproduct[0], data_superproduct[1], url_product, date_scrap, data_superproduct[2]) == True:
                flag_superproduct = True
            else:
                flag_superproduct = False
        
        total_products += 1
        cont_products_category += 1
        print('[{}/{}] > {} - ${} > ${}'.format(cont_products_category, total_products_category, data_product[0], data_superproduct[1], data_superproduct[0]))          
print('Total products from {}: {}'.format(NAME_SUPERMARKET, total_products))
