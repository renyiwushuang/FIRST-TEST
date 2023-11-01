
import threading
try:
    import paho.mqtt.client as mqtt
except:
    from .paho.mqtt import client as mqtt
from queue import Queue

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #print(userdata)
    for sub in userdata['sl']:
        print("sub:%s"%sub)
        client.subscribe(sub)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    userdata['mq'].put((msg.payload,msg.topic))

# mqtt thread entry
class mqtt_thread_entry(threading.Thread):
    def __init__(self, t_name,user_queue,broker_ip,sub_list):
        threading.Thread.__init__(self)
        self.name = t_name
        self.mq = user_queue #on_messageq ueue
        self.broker_ip = broker_ip #mqtt broker ip
        self.sub_list = sub_list #sub list

        data = dict()
        data['mq'] = self.mq
        data['sl'] = self.sub_list#sub list

        self.client = mqtt.Client(userdata=data)

    def mqtt_pub(self,topic,data):
        self.client.publish(topic, data)

    def run(self):
        self.client.on_connect = on_connect
        self.client.on_message = on_message

        self.client.connect(self.broker_ip, 1883, 60)
        self.client.loop_forever()

# The callback for when a PUBLISH message is received from the server.
def mqtt_thread_init (broker_ip,sub_list,user_queue):
    mqtt_t = mqtt_thread_entry("mqtt_thread",user_queue,broker_ip,sub_list)
    mqtt_t.start()
    return mqtt_t
