from flask import Flask, render_template, request, redirect, url_for
import requests
import PyPDF2
import re
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['pdf']
    if uploaded_file and uploaded_file.filename != '':
        # Extract text from the uploaded PDF using the Worqhat API
        url = "https://api.worqhat.com/api/ai/v2/pdf-extract"
        headers = {
            'Authorization': 'Bearer sk-75998b0cc5e94ad3b5d52778fe9a1906'  # Replace with your API key
        }
        files = {'file': ('file.pdf', uploaded_file.read())}
        response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            try:
                extracted_text = response.json()['data']['content']
                # Generate a quiz from the extracted text
                quiz = generate_quiz(extracted_text)
                return render_template('quiz.html', quiz=quiz)
            except KeyError:
                print("API Response Format Error: Missing 'data' or 'content' key.")
                print(response.text)  # Print the API response for debugging
                return "Error: API response format is unexpected."
        else:
            print(f"API Error: {response.status_code}")
            print(response.text)  # Print the API response for debugging
            return f"Error extracting text from PDF: {response.status_code}"

    return "No file provided."


def generate_quiz(text, num_questions=5):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    selected_sentences = random.sample(sentences, min(num_questions, len(sentences)))

    quiz = []
    for sentence in selected_sentences:
        keywords = re.findall(r'\b\w+\b', sentence)
        if keywords:
            keyword = random.choice(keywords)
            question = sentence.replace(keyword, '_______')
            choices = random.sample(keywords, 3) + [keyword]
            random.shuffle(choices)
            quiz.append({
                'question': question,
                'choices': choices,
                'answer': keyword
            })

    return quiz

if __name__ == '__main__':
    app.run(debug=True)
