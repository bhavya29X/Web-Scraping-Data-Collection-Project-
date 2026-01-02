import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Download the html page 

# Create directory if it doesn't exist
os.makedirs("htmls", exist_ok=True)
# a = requests.get("https://books.toscrape.com")
for i in range(1, 51):
    response_url = requests.get(f"https://books.toscrape.com/catalogue/page-{i}.html")
    if response_url.status_code == 200:
        with open(f"htmls/page{i}.html", "w", encoding="utf-8") as f:
            f.write(response_url.text)
        print(f"Downloading page {i} successfully")
    else:
        print(f"Failed to download page {i} (Status code: {response_url.status_code})")
        
items = []

# Loop through 50 pages
for page in range(1, 51):
    file_path = f"htmls/page{page}.html"
    
    # Open each HTML file
    with open(file_path, encoding="utf8") as f:
        content = f.read()
    
    soup = BeautifulSoup(content, "html.parser")
    articles = soup.select("article.product_pod")
    
    # Extract title and price from each item
    for article in articles:
        title = article.find("h3").find("a")["title"]
        price = float(article.select_one("p.price_color").text.split("£")[1])
        rating_element = article.select_one("p.star-rating")
        rating = rating_element['class'][1]
        items.append([title, price, rating])

df = pd.DataFrame(items, columns=["Book Title", "Price", "Rating"])
df.index = range(1, len(df) + 1)

df.to_excel("data.xlsx", index=True)
print(df)

