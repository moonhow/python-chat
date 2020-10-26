import boto3
from boto3.dynamodb.conditions import Key, Attr

class ChatConnection:
    def create(self, data):
        dynamodb = boto3.resource('dynamodb')
        tblChatConnection = dynamodb.Table('chat_connection')
        tblChatConnection.put_item(
            Item = {
                'connection_id': data['connection_id'],
                'username': data['username']
            }
        )
        return 'Success'

    def delete(self, connectionId):
        dynamodb = boto3.resource('dynamodb')
        tblChatConnection = dynamodb.Table('chat_connection')
        tblChatConnection.delete_item(
            Key = {
                'connection_id': connectionId
            }
        )
        return 'Success'

    def getList(self):
        dynamodb = boto3.resource('dynamodb')
        tblChatConnection = dynamodb.Table('chat_connection')
        self.items = tblChatConnection.scan()
        if 'Items' in self.items:
            self.items = self.items['Items']
        else:
            self.items = None
        return self.items

    def getById(self, connectionId):
        dynamodb = boto3.resource('dynamodb')
        tblChatConnection = dynamodb.Table('chat_connection')
        self.item = tblChatConnection.get_item(Key={'connection_id': connectionId})
        if 'Item' in self.item:
            self.item = self.item['Item']
        else:
            self.item = None
        return self.item
