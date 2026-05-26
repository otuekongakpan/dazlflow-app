from urllib import response

from flask import Flask, request, render_template
import requests  # Import the new library

app = Flask(__name__)

# Replace this string with your exact deployment link from Step 3!
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbwlPXiVr4vLxR8LL0XBXzsrYuL2qhou-_JxM5anO_mHwp8P_Q6chlA41nfFZfRVOqY/exec"

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')

# 3. CONTACT PAGE
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    if request.method == 'POST':
        email = request.form['email']
        
        # Send the email data over to your Google Sheet web app
        try:
            # NEW (Tells Python to follow Google's internal redirect)
            response = requests.post(GOOGLE_SHEET_URL, data={'email': email}, allow_redirects=True)
            # Check if Google accepted it cleanly
            if response.status_code == 200:
                return "✅ You've been added to the waitlist!"
            else:
                # Add this temporary debug line to see the exact issue:
                return f"❌ Google Error Code {response.status_code}: {response.text[:200]}"
        except Exception as e:
            return f"❌ Server connection error: {str(e)}"

    return render_template('waitlist.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)