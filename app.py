from flask import Flask

app = Flask(__name__)

@app.route('/')
def dashboard():
    return 'blblblbllb!'

if __name__ == '__main__':
    app.run(debug=True)