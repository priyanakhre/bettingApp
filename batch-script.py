from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
import time

while True:
	print("yes ")
	time.sleep(90) 
	print("no ")
	#es = Elasticsearch(['es'])
	
	
	es = Elasticsearch(['es'])
	
	consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
	

	for message in consumer:
	 	print(json.loads((message.value).decode('utf-8')))
	 	some_new_listing = json.loads((message.value).decode('utf-8'))
	 	es.index(index='listing_index', doc_type='listing', id=some_new_listing['id'], body=some_new_listing)
	 	es.indices.refresh(index="listing_index")