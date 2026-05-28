from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbw6QLWwwqmyXE2mdtsxORPJxMyxpSzM2rMEg8N17eD65dira-PN05_Dynq1G5s_30I9/exec"

# Your ONE route for the entire site
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # This looks for 'index.html' in your 'templates' folder
        return render_template('index.html')
    
    # Process POST submission (if your form action is "/")
    email = request.form.get('email', '').strip().lower()
    if not email:
        return "❌ Please provide a valid email address.", 400

    try:
        response = requests.post(GOOGLE_SHEET_URL, data={'email': email}, allow_redirects=True)
        result = response.json()
        
        if result.get("status") == "success":
            return "✅ You're on the list! <a href='/'>Back Home</a>"
        return f"❌ Error: {result.get('message', 'Unknown error')}", 500
    except Exception as e:
        return f"❌ Server error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)