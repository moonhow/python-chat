import boto3
from boto3.dynamodb.conditions import Key, Attr

class ChatRoom:
    def create(self, data):
        dynamodb = boto3.resource('dynamodb')
        tblChatRoom = dynamodb.Table('chat_room')
        tblChatRoom.put_item(
            Item = {
                'room_id': data['room_id'],
                'total_messages': data['total_messages']
            }
        )
        return 'Success'

    def update(self, data):
        dynamodb = boto3.resource('dynamodb')
        tblChatRoom = dynamodb.Table('chat_room')
        tblChatRoom.update_item(Key={'room_id': data['room_id']}, 
            UpdateExpression = 'SET total_messages = :value',
            ExpressionAttributeValues = {
                ':value' : data['total_messages']
            },
            ReturnValues = 'UPDATED_NEW'
        )
        return 'Success'

    def delete(self, roomId):
        dynamodb = boto3.resource('dynamodb')
        tblChatRoom = dynamodb.Table('chat_room')
        tblChatRoom.delete_item(
            Key = {
                'room_id': roomId
            }
        )
        return 'Success'

    def getList(self):
        dynamodb = boto3.resource('dynamodb')
        tblChatRoom = dynamodb.Table('chat_room')
        self.items = tblChatRoom.scan()
        if 'Items' in self.items:
            self.items = self.items['Items']
        else:
            self.items = None
        return self.items

    def getById(self, roomId):
        dynamodb = boto3.resource('dynamodb')
        tblChatRoom = dynamodb.Table('chat_room')
        self.item = tblChatRoom.get_item(Key={'room_id': roomId})
        if 'Item' in self.item:
            self.item = self.item['Item']
        else:
            self.item = None
        return self.item