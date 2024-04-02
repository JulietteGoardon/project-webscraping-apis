from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_books(api_key, genre, max_pages, published_year):
    base_url = "https://www.googleapis.com/books/v1/volumes"

    # Set up the parameters for the API request
    params = {
        'q': f'subject:{genre}',
        'maxResults': 3,
        'key': api_key,
    }

    # Make the API request
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Filter books based on the maximum number of pages and published year
        filtered_books = []
        for item in data.get('items', []):
            volume_info = item.get('volumeInfo', {})
            if 'pageCount' in volume_info and volume_info['pageCount'] <= max_pages:
                published_date = volume_info.get('publishedDate', '')
                published_year_from_date = int(published_date.split('-')[0]) if published_date else None

                if published_year_from_date is not None and published_year_from_date >= published_year:
                    book = {
                        'title': volume_info.get('title', 'N/A'),
                        'author': ', '.join(volume_info.get('authors', ['N/A'])),
                        'pages': volume_info.get('pageCount', 'N/A'),
                        'image_url': volume_info['imageLinks']['thumbnail'] if 'imageLinks' in volume_info else 'N/A',
                        'published_date': published_date,
                    }
                    filtered_books.append(book)

        return filtered_books
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        genre = request.form['category']
        max_pages = int(request.form['max_pages'])
        published_year = int(request.form['published_year'])

        # Call the function to get book recommendations
        recommendations = get_books(api_key="AIzaSyAgnqAeOUBm47F9-blDN1znlMy_8vOmIPs", genre=genre, max_pages=max_pages, published_year=published_year)

        # Render the template with recommendations
        return render_template('index.html', recommendations=recommendations)

    # Render the form for user input
    return render_template('index.html', recommendations=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
