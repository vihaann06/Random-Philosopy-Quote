from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)

def get_philosophy_quotes():
    page = random.randint(1, 100)
    url = f"https://www.goodreads.com/quotes/tag/philosophy?page={page}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        quotes = []
        quote_elements = soup.find_all('div', class_='quoteText')
        
        for element in quote_elements:
            full_text = element.get_text(strip=True)
            parts = full_text.split('―')
            if len(parts) >= 2:
                quote_text = parts[0].strip()
                author = parts[1].strip()
                author = author.split('(')[0].strip()
                
                word_count = len(quote_text.split())
                if quote_text and author and word_count <= 30:
                    quotes.append({
                        'text': quote_text,
                        'author': author
                    })
        
        if not quotes:
            if page != 1:
                return get_philosophy_quotes()
            return [{'text': "No quotes found. Please try again later.", 'author': ''}]
        
        random.shuffle(quotes)
        return quotes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching quotes: {e}")
        return get_philosophy_quotes()

@app.route('/')
def index():
    quotes = get_philosophy_quotes()
    random_quote = random.choice(quotes) if quotes else {'text': "No quotes available", 'author': ''}
    return render_template('index.html', quote=random_quote['text'], author=random_quote['author'])

if __name__ == '__main__':
    app.run(debug=True)
