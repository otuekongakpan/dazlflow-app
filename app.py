from flask import Flask, request, render_template, redirect, url_for
import requests
import os

app = Flask(__name__)

# Ensure this URL points to your latest "New Version" deployment
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbw6QLWwwqmyXE2mdtsxORPJxMyxpSzM2rMEg8N17eD65dira-PN05_Dynq1G5s_30I9/exec"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/waitlist', methods=['POST'])
def waitlist():
    email = request.form.get('email', '').strip().lower()
    
    if not email:
        return "❌ Please provide a valid email address.", 400

    try:
        # Send data to Google Sheet
        response = requests.post(GOOGLE_SHEET_URL, data={'email': email}, allow_redirects=True)
        
        # Check if Google Script responded with valid JSON
        result = response.json()
        
        # Check for Duplicate Status (as defined in your Apps Script)
        if result.get("status") == "error" and result.get("message") == "DUPLICATE":
            return """
            <div style="background:#000; color:#ff453a; font-family:sans-serif; text-align:center; padding:100px; height:100vh;">
                <h2>⚠️ Already on the list</h2>
                <p style="color:#C5EAFC;">You've already signed up. Welcome to the frequency.</p>
                <br><br>
                <a href="/" style="color:#00A8FF; text-decoration:none; border:1px solid #00A8FF; padding:10px 20px; border-radius:20px;">← Back Home</a>
            </div>
            """

        # Success Case
        if result.get("status") == "success":
            return """
            <div style="background:#000; color:#00F0FF; font-family:sans-serif; text-align:center; padding:100px; height:100vh;">
                <h2>✅ You're on the list!</h2>
                <p style="color:#C5EAFC;">Welcome to the frequency.</p>
                <br><br>
                <a href="/" style="color:#00A8FF; text-decoration:none; border:1px solid #00A8FF; padding:10px 20px; border-radius:20px;">← Back Home</a>
            </div>
            """
            
        return f"❌ Error: {result.get('message', 'Unknown error')}", 500

    except Exception as e:
        return f"❌ Server error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)