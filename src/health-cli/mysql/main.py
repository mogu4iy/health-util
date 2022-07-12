import mysql.connector
import time

CONFIG_SCHEMA_FIELD_REQUIRED = ["host", "password", "username"]
CONFIG_FIELD_DEFAULT= {"protocol": "mysql", "port": 3306}
CONFIG_FIELD_REQUIRED = ["host", "port", "password", "username", "protocol"]

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
    start_time = time.time()
    count = 0
    while True:
        time.sleep(config["interval"])
        if count > config["retry"]:
            raise Exception(f"Service: '{config['name']}' too many retries.")
        count += 1
        try:
            connection = mysql.connector.connect(host=config["host"],port=config["port"],user=config["username"],password=config["password"])
            cursor = connection.cursor()
            cursor.execute("SELECT CURDATE()")
            row = cursor.fetchone()
            print("Current date is: {0}".format(row[0]))
            connection.close()
            break
        except Exception as e:
            print(e)
            print("-"*5)
        if time.time() - start_time > config["timeout"]:
            raise Exception(f"Service: '{config['name']}' timeout exception.")