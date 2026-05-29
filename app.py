from flask import Flask, request, render_template
import requests
import os
from flask_mail import Mail, Message
from threading import Thread

app = Flask(__name__)

GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbyT1M3SNEqo0svvyj_w16Om3TMP7KFqB3sv9VqtnxV11kKSKCrlTHm3trAm-mcCLl_g/exec"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'dazlflow.ops@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your_actual_app_password')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/fuel-the-flow')
def fuel_the_flow():
    return render_template('fuel.html')

# Your ONE route for the entire site
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    
    # 1. Capture both name and email
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip().lower()
    
    if not name or not email:
        return "❌ Please provide both a name and a valid email address.", 400

    try:
        # 2. Send both to Google Sheets
        response = requests.post(GOOGLE_SHEET_URL, data={'name': name, 'email': email}, allow_redirects=True)
        result = response.json()
        
        if result.get("status") == "success":
            try:
                # 3. Personalize the email using the name variable
                msg = Message("Welcome to the DazlFlow ecosystem",
                              sender=('DazlFlow Team', 'dazlflow.ops@gmail.com'),
                              recipients=[email])
                
                # Using the name variable here
                msg.body = (f"Hi {name},\n\n"
                            "Thank you so much for joining the DazlFlow waitlist! We are incredibly excited "
                            "to have you on board as we build a new, anti-algorithm infrastructure for "
                            "independent music culture.\n\n"
                            "We are currently in the foundation phase, mapping out the architecture "
                            "that will allow artists and listeners to connect on a deeper, more emotional level. "
                            "You’ve just secured your place in the ecosystem, and we will be reaching out "
                            "with exclusive updates and beta-access invites soon.\n\n"
                            "In the meantime, feel free to visit our site to explore the vision further.\n\n"
                            "Stay tuned for the frequency.\n\n"
                            "Best,\nThe DazlFlow Team\n"
                            "https://dazlflow-app.onrender.com/") # Adding a URL helps Gmail see it as a real, interactive message
                                
                thr = Thread(target=send_async_email, args=[app, msg])
                thr.start()
            except Exception as e:
                print(f"Email failed to send: {str(e)}")
            
            return render_template('thankyou.html')
        return f"❌ Error: {result.get('message', 'Unknown error')}", 500
    except Exception as e:
        return f"❌ Server error: {str(e)}", 500
    
def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Async email failed: {e}")
            
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)