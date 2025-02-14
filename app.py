from flask import Flask, request
from openai import OpenAI
from flask_socketio import SocketIO, emit, disconnect
import os
import json
import helper
import db
from dotenv import load_dotenv
import concurrent.futures
import redis


response = {
    'hi':"hello there",
}
users = {}

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
print(os.getenv)
app = Flask(__name__)
conn = db.createDBConection()
socketio = SocketIO(app, cors_allowed_origins="*")
# Set up the Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
helper.loadResponsesFromDB(conn,redis_client)

@socketio.on('connect',namespace="/chat")
def handle_connect():
    user = request.args.get('user_id')
    if not redis_client.get(user):
        emit('response', helper.sendResponse(True, 'HI! I am a chatbot. How can I help you today?'))
        redis_client.set(user, 'connected')
        print(f"{user} to the server on ",helper.get_time())
        return 
    
@socketio.on('chat',namespace="/chat")
def handle_chat(data):
    try:
        if not data:
            emit('response', helper.sendResponse(False, 'No data provided'))
            return
        
        message = data.get('text')
        print("this is the message",message)
        if not message:
            emit('response', helper.sendResponse(False, 'empty message'))
            return

        cached_value = redis_client.get(message)   
        if cached_value:
            cached_value = cached_value.decode('utf-8')
            emit('response', helper.sendResponse(True,cached_value))
            return
        else:
            print("used openai")
            completion = helper.sendOpenAi(client, message)
            redis_client.set(message, completion)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(helper.writeResponseToDB, conn, message, completion)
            emit('response', helper.sendResponse(True, completion))
    except Exception as e:
        emit('response', helper.sendResponse(False, "I am unable to answer right now"))
        print("execption occured",e)

@socketio.on('disconnect',namespace="/chat")
def handle_disconnect():
    user = request.args.get('user_id')
    if user is not None:
        redis_client.delete(user)
        print(f"{user} disconnected from the server on ",helper.get_time())
        return
if __name__ == '__main__':
    socketio.run(app, debug=True, port=8001)