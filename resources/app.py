from flask import Flask, jsonify
app = Flask(__name__)


@app.route('/test')
def hello():
    print("HELLOOOOOOOOOO")
    response = jsonify({
        "name": "Eol",
        "country": "Kosovo",
        "age": 19
    })
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)