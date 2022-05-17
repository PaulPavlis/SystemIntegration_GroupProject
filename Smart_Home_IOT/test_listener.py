import stomp
import json
import constants as keys
import time


class MsgListener(stomp.ConnectionListener):
    def __init__(self):
        # to keep the count of messages received
        self.msg_recieved = 0

    def on_error(self, message):
        print('received an error "% s"' % message)

    def on_message(self, header, body):
        print(body)
        self.msg_received += 1
        # add your logic based on the message received here


# Establish a connection
con = stomp.Connection([(keys.HOST, keys.PORT)])
# listener class to be instantiated.
listener = MsgListener()
con.set_listener("", listener)
# wait will ensure it waits till connection is established and acknowledged.
con.connect(keys.USER, keys.PASSWORD, wait=True)
# subscribe to a particular topic or queue by giving the path and headers if required by the server.
con.subscribe(keys.SUBSCRIBE_TOPICS[0], 1, headers={})

print("Started and waiting for messages...")
while 1:
    time.sleep(2)
