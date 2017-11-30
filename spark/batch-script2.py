from kafka import KafkaConsumer
import json
import time

while True:
	
	
	time.sleep(200) 

	try:
		consumer = KafkaConsumer('bet-detail-topic', group_id='bet-detail', bootstrap_servers=['kafka:9092'])
	
	except:
		time.sleep(20) 
		consumer = KafkaConsumer('bet-detail-topic', group_id='bet-detail', bootstrap_servers=['kafka:9092'])
		

	for message in consumer:
	 	print(json.loads((message.value).decode('utf-8')))
	 	some_new_listing = json.loads((message.value).decode('utf-8'))
	 	entry = str(some_new_listing['user-id']) + '\t' + str(some_new_listing['item-id']) + '\n'
	 	f=open("access_log.txt", "a+")
	 	f.write(entry)