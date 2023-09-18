from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Face Comparison</title>
    </head>
    <body>
        <h1>Face Comparison</h1>
        <form id="upload-form" enctype="multipart/form-data" method="post" action="/compare_faces">
            <input type="file" id="user-image" name="user_image" accept="image/*" required>
            <input type="file" id="webcam-image" name="webcam_image" accept="image/*" required>
            <button type="submit">Compare Faces</button>
        </form>
        <div id="result"></div>
        <script>
            const form = document.getElementById('upload-form');
            const resultDiv = document.getElementById('result');

            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                resultDiv.innerHTML = 'Comparing faces...';

                const formData = new FormData(form);
                try {
                    const response = await fetch('/compare_faces', {
                        method: 'POST',
                        body: formData,
                    });

                    if (response.status === 200) {
                        const result = await response.json();
                        resultDiv.innerHTML = JSON.stringify(result, null, 2);
                    } else {
                        resultDiv.innerHTML = 'Face comparison failed.';
                    }
                } catch (error) {
                    console.error(error);
                    resultDiv.innerHTML = 'An error occurred during face comparison.';
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/compare_faces', methods=['POST'])
def compare_faces():
    url = "https://api.worqhat.com/api/ai/images/v2/facial-comparison"

    files = {
        'source_image': ('user_image.jpeg', request.files['user_image'], 'image/jpeg'),
        'target_image': ('webcam_image.jpeg', request.files['webcam_image'], 'image/jpeg')
    }

    headers = {
        'Authorization': 'Bearer sk-eee576b8e5774fd8be604db01b1300da'
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        result = response.json()
        return jsonify(result)
    else:
        return jsonify({'error': 'Face comparison failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)
