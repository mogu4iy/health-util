import pika
import time

CONFIG_SCHEMA_FIELD_REQUIRED = ["host", "password", "username"]
CONFIG_FIELD_DEFAULT= {"protocol": "amqp", "port": 5672, "vhost": "/"}
CONFIG_FIELD_REQUIRED = ["host", "port", "password", "username", "protocol", "vhost"]

def validate_service_schema(config):
    for field in CONFIG_SCHEMA_FIELD_REQUIRED:
        if config.get(field) is None:
            raise Exception(f"Service: service '{config['name']}' field '{field}' is required.")

def prepare_config(config):
    for field in CONFIG_FIELD_DEFAULT:
        if config.get(field) is None:
            config[field] = CONFIG_FIELD_DEFAULT[field]

def validate_service(schema, config):
    for field in CONFIG_SCHEMA_FIELD_REQUIRED:
        if config.get(field) is None:
            raise Exception(f"Service: service '{config['name']}' field '{field}' is required.")
        if str(config[field]).strip(" ") == "" and schema[field].get("allowEmpty") != True:
            raise Exception(f"Service: service '{config['name']}' field '{field}' is invalid.")

def health_check(config):
    queue_name = f'{config["name"]}-healthcheck'.lower()
    credentials = pika.PlainCredentials(config["username"], config["password"])
    conn_params = pika.ConnectionParameters(host=config["host"], port=config["port"], virtual_host = config["vhost"], credentials = credentials)
    start_time = time.time()
    count = 0
    while True:
        if count > config["retry"]:
            raise Exception(f"Service: '{config['name']}' too many retries.")
        count += 1
        try:
            connection = pika.BlockingConnection(conn_params)
            channel = connection.channel()
            channel.basic_qos(prefetch_count=1)
            channel.queue_declare(queue_name, durable = False, auto_delete = True)
            channel.basic_consume(queue_name, lambda x: print(x))
            connection.close()
            break
        except Exception as e:
            print(e)
            print("-"*5)
        if time.time() - start_time > config["timeout"]:
            raise Exception(f"Service: '{config['name']}' timeout exception.")