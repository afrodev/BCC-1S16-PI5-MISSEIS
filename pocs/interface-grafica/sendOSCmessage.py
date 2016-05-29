import argparse
import random
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="localhost",
  help="The ip of the OSC server")

parser.add_argument("--port", type=int, default=7580,
  help="The port the OSC server is listening on")

args = parser.parse_args()

client = udp_client.UDPClient(args.ip, args.port)

def sendMessageOSC(messageOsc):
    msg = osc_message_builder.OscMessageBuilder(address="" + messageOsc)
    msg.add_arg(random.random())
    msg = msg.build()
    print("Sending", msg.dgram)
    client.send(msg)
    time.sleep(1)