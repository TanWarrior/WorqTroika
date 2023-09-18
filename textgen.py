from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_notes', methods=['POST'])
def generate_notes():
    question = request.form.get('question')

    # Make a request to the Worqhat API
    url = "https://api.worqhat.com/api/ai/content/v2"
    headers = {
        "Authorization": "Bearer sk-cb66f6d3f4b34978a7714eb9a6651f21",
        "Content-Type": "application/json"
    }
    data = {
        "question": question,
        "randomness": 0.4
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        try:
            notes = response.json()['content']
            return render_template('notes.html', notes=notes)
        except KeyError:
            return "Error: Response format is unexpected"
    else:
        return "Error: Unable to generate notes"

if __name__ == '__main__':
    app.run(debug=True)
