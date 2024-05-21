from collections import namedtuple
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

# Define a named tuple to represent article data
Article = namedtuple('Article', ['name', 'old_price', 'current_price', 'discount', 'ratings'])

def export_to_csv(article_list, csv_file_path):
    """
    Export article data to a CSV file.
    
    Args:
        article_list (list): List of named tuples representing article data.
        csv_file_path (str): File path for the CSV file.

    Returns:
        str: Success message if export is successful.
    """
    data = []
    for article in article_list:
        data.append({
            'Name': article.name,
            'Old Price': article.old_price,
            'Current Price': article.current_price,
            'Discount': article.discount,
            'Ratings': article.ratings
        })

    df = pd.DataFrame(data)
    try:
        if os.path.exists(csv_file_path):
            with open(csv_file_path, 'a', newline='') as existing_file:
                df.to_csv(existing_file, header=False, index=False)
            return 'New information added successfully'
        else:
            df.to_csv(csv_file_path, index=False)
            return 'Information exported successfully'
    except Exception as e:
        return f"An error occurred: {e}"

def find_articles(mercado_articles):
    """
    Find and extract article data from Mercado Libre articles.

    Args:
        mercado_articles (list): List of BeautifulSoup elements representing articles.

    Returns:
        list: List of named tuples containing article data.
    """
    articles_list = []
    for article in mercado_articles:
        try:
            name = article.find('h2', class_='ui-search-item__title').text
            old_price = article.find('span', class_='andes-money-amount__fraction').text.replace('.', '')
            current_price = article.find('span', class_='andes-money-amount__fraction').text.replace('.', '')
            discount = article.find('span', class_='ui-search-price__discount shops__price-discount')
            ratings = article.find('span', class_='ui-search-reviews__amount')

            discount = discount.text if discount else 'No discount'
            ratings = ratings.text if ratings else 'No ratings available'

            article_data = Article(name, old_price, current_price, discount, ratings)
            articles_list.append(article_data)
        except AttributeError as e:
            print(f"Error parsing article: {e}")

    return articles_list

def select_article(art):
    """
    Select the URL for a specific article type or category.

    Args:
        art (str): Article type or category.

    Returns:
        str: URL for the specified article type or category.
    """
    return f'https://listado.mercadolibre.com.co/{art}#D[A:celular]'

def select_page(page):
    """
    Select the URL for a specific page number.

    Args:
        page (str): Page number.

    Returns:
        str: URL for the specified page number.
    """
    return f'https://listado.mercadolibre.com.co/celulares-telefonos/celulares-smartphones/celulares_Desde_{page}_NoIndex_True'

def main():
    article_url = select_article('cell-phones')
    page_url = select_page('51')

    try:
        html_text = requests.get(page_url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        articles = soup.find_all('li', class_='ui-search-layout__item shops__layout-item ui-search-layout__stack')
        mercado_articles = find_articles(articles)

        script_dir = os.path.dirname(os.path.realpath(__file__))
        csv_file_path = os.path.join(script_dir, 'cell_phones.csv')
        result_message = export_to_csv(mercado_articles, csv_file_path)
        print(result_message)
    except requests.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    main()
