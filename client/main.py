import websocket
import json
import threading
import sys
import os
from datetime import datetime
from dateutil import tz

def _is_json(data):
    try:
        json.loads(data)
        return True
    except:
        return False

def _localize_timestamp(utcDateTimeString, format):
    utc_tz = tz.tzutc()
    local_tz = tz.tzlocal()
    utc_dt = datetime.strptime(utcDateTimeString, format)
    utc_dt = utc_dt.replace(tzinfo=utc_tz)
    local_dt = utc_dt.astimezone(local_tz)
    return local_dt.strftime(format)

def clear_screen():
	os.system('cls') if sys.platform[:3] == 'win' else os.system('clear')

def on_message(ws, message):
    if _is_json(message):
        message = json.loads(message)
        message['timestamp'] = _localize_timestamp(message['timestamp'], '%m/%d/%Y %H:%M:%S')
        message = '\r{} [{}]: {}\n> '.format(message['username'], message['timestamp'], message['message'])
        print(message, end = '')

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print('Welcome ' + username)
    def write():
        while True:
            message = input('> ')
            ws_message = {
                'action': 'onMessage',
                'data': message
            }
            ws.send(json.dumps(ws_message))
            print_message = '{} [{}]: {}'.format(username, datetime.now().strftime('%m/%d/%Y %H:%M:%S'), message)
            print(print_message)
    write_thread = threading.Thread(target=write)
    write_thread.start()

######################################################################################

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    username = input('Please enter your nickname: ')
websocket.enableTrace(False)
ws = websocket.WebSocketApp("wss://jbhdr7m2o0.execute-api.ap-southeast-1.amazonaws.com/dev?username=" + username,
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)
ws.on_open = on_open
ws.run_forever()

