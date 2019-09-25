from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt #import the client1
import time

def on_message(client,userdata,message):
	mac = str(message.payload.decode("utf-8"))
	print("message received: " , mac)
	results = client.query('SELECT total FROM traffic_accounting WHERE mac = \''+mac+'\' and time > now() - 1h;')
	points = results.get_points()
	points = list(points)
	#print(len(points))
	if len(points) == 0:
        	json_insert = [ { "measurement" : "traffic_accounting", "tags" : { "mac" : mac }, "fields" : { "total" : 1 } } ]
        	client.write_points(json_insert)

# MQTT server

broker_address="localhost" 
broker_port=1883
broker_user=""
broker_password=""

# Influx setup
client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('sniffer')


print("creating new instance")
client = mqtt.Client("mqttsniffer") #create new instance

client.username_pw_set(broker_user,broker_password)

print("connecting to broker")
client.connect(broker_address,port=broker_port) #connect to broker

client.loop_start()

print("Subscribing to topic")
client.subscribe("esp/sniffer")

client.on_message=on_message        #attach function to callback

try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	print("bye")
	client.disconnect()
	client.loop_stop()
