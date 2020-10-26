import uuid
import boto3
from boto3.dynamodb.conditions import Key, Attr

class ChatMessage:
    def create(self, data):
        dynamodb = boto3.resource('dynamodb')
        tblChatMessage = dynamodb.Table('chat_message')
        tblChatMessage.put_item(
            Item = {
                'room_id': data['room_id'],
                'username': data['username'],
                'messages': [
                    {
                        'timestamp':  data['timestamp'],
                        'message':  data['message']
                    }
                ]
            }
        )
        return 'Success'

    def update(self, data):
        dynamodb = boto3.resource('dynamodb')
        tblChatMessage = dynamodb.Table('chat_message')
        lstMessages = self.item['messages']
        if len(lstMessages)>=20:
            lstMessages.pop(0)
        lstMessages.insert(len(lstMessages), {
            'timestamp':  data['timestamp'],
            'message':  data['message']
        })
        tblChatMessage.update_item(Key={'room_id': data['room_id'], 'username': data['username']}, 
            UpdateExpression = 'SET messages = :value',
            ExpressionAttributeValues = {
                ':value' : lstMessages
            },
            ReturnValues = 'UPDATED_NEW'
        )
        return 'Success'

    def delete(self, roomId, username):
        dynamodb = boto3.resource('dynamodb')
        tblChatMessage = dynamodb.Table('chat_message')
        tblChatMessage.delete_item(
            Key = {
                'room_id': roomId,
                'username': username
            }
        )
        return 'Success'

    def getList(self):
        dynamodb = boto3.resource('dynamodb')
        tblChatMessage = dynamodb.Table('chat_message')
        self.items = tblChatMessage.scan()
        if 'Items' in self.items:
            self.items = self.items['Items']
        else:
            self.items = None
        return self.items

    def getById(self, roomId, username):
        dynamodb = boto3.resource('dynamodb')
        tblChatMessage = dynamodb.Table('chat_message')
        self.item = tblChatMessage.get_item(Key={
            'room_id': roomId,
            'username': username
        })
        if 'Item' in self.item:
            self.item = self.item['Item']
        else:
            self.item = None
        return self.item