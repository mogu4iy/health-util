import urllib.parse
import requests
import time 

CONFIG_SCHEMA_FIELD_REQUIRED = ["host", "port", "password"]
CONFIG_FIELD_DEFAULT= {"protocol": "redis", "port": 6379, "health_route": "/health"}
CONFIG_FIELD_REQUIRED = ["host", "port", "password", "protocol", "health_route"]

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
    health_url = urllib.parse.urljoin(f"{config['protocol']}://{config['host']}:{config['port']}", config["health_route"])
    start_time = time.time()
    count = 0
    while True:
        time.sleep(config["interval"])
        if count > config["retry"]:
            raise Exception(f"Service: '{config['name']}' too many retries.")
        count += 1
        try:
            response = requests.get(health_url)
            if (response.status_code != 200):
                raise Exception("response status code")
            break
        except Exception as e:
            print(e)
            print("-"*5)
        if time.time() - start_time > config["timeout"]:
            raise Exception(f"Service: '{config['name']}' timeout exception.")