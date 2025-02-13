from flask import Flask, request
from openai import OpenAI
from flask_socketio import SocketIO, emit, disconnect
import os
import helper
import db
from dotenv import load_dotenv
import concurrent.futures


response = {
    'hi':"hello there",
}

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
print(os.getenv)
app = Flask(__name__)
conn = db.createDBConection()
helper.loadResponsesFromDB(conn,response)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect',namespace="/chat")
def handle_connect():
    print('Connected to the server',helper.get_time())
    emit('response', helper.sendResponse(True, 'HI! I am a chatbot. How can I help you today?'))
    
@socketio.on('chat',namespace="/chat")
def handle_chat(data):
    try:
        if not data:
            emit('response', helper.sendResponse(False, 'No data provided'))
            return
        
        message = data.get('text')
        if not message:
            emit('response', helper.sendResponse(False, 'empty message'))
            return
            
        if response.get(message):
            emit('response', helper.sendResponse(True, response[message]))
            return
        else:
            completion = helper.sendOpenAi(client, message)
            response[message] = completion
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(helper.writeResponseToDB, conn, message, completion)
            emit('response', helper.sendResponse(True, completion))
    except Exception as e:
        emit('response', helper.sendResponse(False, str(e)))
        disconnect()

if __name__ == '__main__':
    socketio.run(app, debug=True, port=8001)