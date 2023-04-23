from flask import Flask, render_template, request
from domainavailability import *
import openai
import re
import tldextract

app = Flask(__name__)

api_key = 'at_FEUoybwjBYW4pg10dpfwOncrI27Cc'
client = Client(api_key)

openai.api_key = "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"

def check_domain_availability(domain):
    result = client.data(domain)
    return result.is_available()

def generate_domain_suggestions(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Suggest 10 possibily domain names for a business with the following description, the domain names should be brandable and does not include several dashes: do not suggest any 4 words domains either and avoid number if possible{prompt}",
        max_tokens=600,
        n=1,
        stop=None,
        temperature=0.8,
    )

    # Extract domain suggestions from the response
    text = response.choices[0].text.strip()
    suggestions = re.findall(r'\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', text)
    return suggestions


def is_valid_domain(domain):
    extracted = tldextract.extract(domain)
    return bool(extracted.domain) and bool(extracted.suffix)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'business' in request.form:
            business_description = request.form['business']
            # Get domain suggestions from ChatGPT API
            domain_suggestions = generate_domain_suggestions(business_description)

            # Add .com TLD if it's not present
            domain_suggestions = [domain if re.search(r'\..+$', domain) else domain + '.com' for domain in domain_suggestions]

            # Validate domain suggestions and check availability
            results = {}
            for domain in domain_suggestions:
                if is_valid_domain(domain):
                    results[domain] = check_domain_availability(domain)
                else:
                    results[domain] = False

            return render_template('index.html', results=results)
        else:
            return render_template('index.html', error='Please enter a business description.')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
