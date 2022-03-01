import credentials
import requests
from flask import Flask, request, Response
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Adds support for GET requests for webhook
@app.route('/webhook', methods=['GET'])
def webhook():
    mode = request.args.get('hub.mode')
    verify_token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    # Check if sent token is correct
    if mode and verify_token:
        if mode == 'subscribe' and verify_token == credentials.WEBHOOK_VERIFY_TOKEN():
            print('WEBHOOK_VERIFIED')
            return Response(challenge, status=200, mimetype='application/json')
        else:
            return Response("Unable to authorize", status=400, mimetype='application/json')
    return Response("Test", status=200, mimetype='application/json')

@app.route("/webhook", methods=['POST'])
def webhook_handle():
    data = request.get_json()
    message = data['entry'][0]['messaging'][0]['message']
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    if message['text']:
        request_body = {
                'recipient': {
                    'id': sender_id
                },
                'message': {"text":"hello, world!"}
            }
        response = requests.post('https://graph.facebook.com/v5.0/me/messages?access_token='+ credentials.PAGE_ACCESS_TOKEN(), json=request_body).json()
        return response
    return 'ok'

if __name__ == "__main__":
    app.run(threaded=True)