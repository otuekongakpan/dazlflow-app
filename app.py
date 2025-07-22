from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def waitlist():
    if request.method == 'POST':
        email = request.form['email']
        with open('waitlist.txt', 'a') as f:
            f.write(email + '\n')
        return "✅ You've been added to the waitlist!"

    return render_template('index.html')  # Your waitlist page

if __name__ == '__main__':
    app.run(debug=True)