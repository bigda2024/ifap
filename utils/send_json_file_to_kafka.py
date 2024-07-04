import json
from kafka import KafkaProducer
from datetime import datetime

def load_config(file_path):

    with open(file_path, 'r') as file:
        return json.load(file)

def send_json_file_to_kafka(input_params):

    

    try:
        config = load_config('utils/config.json')



                
        __bootstrap_server = config['bootstrap_server']
        
        topic = config['topic']
        
        json_data = json.dumps(input_params)

        producer = KafkaProducer(
             bootstrap_servers=[__bootstrap_server],
             api_version=(0,11,5),
             value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize JSON to bytes
         )
        
        producer.send(topic, value=json_data)
        producer.flush()
        producer.close()

        current_datetime = datetime.now() 
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        print(formatted_datetime, ": Event posted to Kafka topic... ", str(json_data))

    except Exception as e:
        print("An error occurred:", str(e))

