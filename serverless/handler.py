import json
import boto3
import ast
import logging
import urllib3
from datetime import datetime
from chat_connection import ChatConnection
from chat_room import ChatRoom
from chat_message import ChatMessage


def connect(event, context):
    connectionId = event['requestContext']['connectionId']
    username = event['queryStringParameters']['username']

    data = {
        'connection_id': connectionId,
        'username': username
    }
    objChatConnection = ChatConnection()
    objChatConnection.create(data)
    return {
        'statusCode': 200,
        'body': 'Connected'
    }

def disconnect(event, context):
    connectionId = event['requestContext']['connectionId']

    data = {
        'connection_id': connectionId
    }
    objChatConnection = ChatConnection()
    objChatConnection.delete(connectionId)
    return {
        'statusCode': 200,
        'body': 'Disconnected'
    }

def onMessage(event, context):
    objChatConnection = ChatConnection()
    connectionId = event['requestContext']['connectionId']
    username = objChatConnection.getById(connectionId)['username']

    #Message
    message = ast.literal_eval(event['body'])['data']
    message = {
        'room_id': 1,
        'username': username,
        'timestamp': datetime.now().strftime('%m/%d/%Y %H:%M:%S'),
        'message': message
    }

    #Store Messages by User
    _storeMessagesByUser(1, username, message)
    
    #Update Total Messages By Room
    _updateTotalMessagesByRoom(1)

    #Broadcast messages
    lstConnections = objChatConnection.getList()
    for connection in lstConnections:
        if not connection['username']==username:
            response = _broadcastMessage(connection['connection_id'], message, event)

    return {
        'statusCode': 200,
        'body': 'Message Received & Broadcasted'
    }

def _storeMessagesByUser(roomId, username, message):
    objChatMessage = ChatMessage()
    itmChatMessage = objChatMessage.getById(roomId, username)
    if itmChatMessage is None:
        objChatMessage.create(message)
    else:
        objChatMessage.update(message)

def _updateTotalMessagesByRoom(roomId):
    objChatRoom = ChatRoom()
    itmChatRoom = objChatRoom.getById(roomId)
    if itmChatRoom is None:
        objChatRoom.create({
            'room_id': 1,
            'total_messages': 1
        })
    else:
        itmChatRoom['total_messages'] = itmChatRoom['total_messages'] + 1
        objChatRoom.update(itmChatRoom)

def _broadcastMessage(connectionId, message, event):
    # logger = logging.getLogger('dev')
    # logger.setLevel(logging.DEBUG)
    # logger.debug("https://" + event["requestContext"]["domainName"] + "/" + event["requestContext"]["stage"])
    client = boto3.client("apigatewaymanagementapi", 
                              endpoint_url = "https://" + event["requestContext"]["domainName"] + "/" + event["requestContext"]["stage"])
    response = client.post_to_connection(Data=json.dumps(message).encode('utf-8'),
                                             ConnectionId=connectionId)
    return response