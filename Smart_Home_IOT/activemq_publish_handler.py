import sys
import os
import stomp
import constants as keys


def send_message_2_queue(host, port, user, pwd, dest, data):
    conn = stomp.Connection(host_and_ports=[(host, port)])
    conn.connect(login=user, passcode=pwd)
    conn.send(body=data, destination=dest, persistent='false')
    conn.disconnect()
