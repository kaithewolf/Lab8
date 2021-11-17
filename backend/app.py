from flask import Flask, request

app = Flask(__name__)


# Application Routers
@app.route('/')
def home_handler():
    return 'Please use the API at /api/v1/!'


@app.route('/api/v1/', methods=['POST', 'GET'])
def api_handler():
    # Match request type
    match request.method:
        case 'GET':
            print("GET")
        case 'POST':
            print("POST")
        case _:
            print("Unknown!")


if __name__ == '__main__':

    # Run the app
    app.run()
