import unittest
from datetime import datetime
from chat_message import ChatMessage

class TestMain(unittest.TestCase):
    def test_create(self):
        self.assertEqual(_create({
                'room_id': 1, 
                'username': 'test',
                'messages': [
                    {
                        'timestamp': datetime.now().strftime('%m/%d/%Y %H:%M:%S'),
                        'message': 'hello'
                    }
                ]
            }), 
        'Success', 'Should be Success')

# if __name__ == '__main__':
#     unittest.main()