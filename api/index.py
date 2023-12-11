import json
import string
import random
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Load the URL mappings from a JSON file
try:
    with open('urls.json', 'r') as file:
        url_mapping = json.load(file)
except FileNotFoundError:
    url_mapping = {}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['url']
        while True:
            # Generate a random short code
            short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            # Check if the short code has already been used
            if short_code not in url_mapping:
                url_mapping[short_code] = original_url
                # Save the updated URL mappings to the JSON file
                with open('urls.json', 'w') as file:
                    json.dump(url_mapping, file)
                break
        return render_template('index.html', short_url=request.host_url + short_code)
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    if short_code in url_mapping:
        return redirect(url_mapping[short_code])
    return 'URL not found', 404

if __name__ == '__main__':
    app.run(debug=True)