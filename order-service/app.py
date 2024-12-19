from flask import Flask

app = Flask(__name__)

@app.route('/orders', methods=['GET'])
def orders():
    return "Hello World2!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)  # Changed from 'localhost' to '0.0.0.0'
