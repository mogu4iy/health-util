CONFIG_SCHEMA_FIELD_REQUIRED = ["host", "port", "password"]
CONFIG_FIELD_DEFAULT= {"protocol": "redis", "port": 6379}
CONFIG_FIELD_REQUIRED = ["host", "port", "password", "protocol"]

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
    print(config["name"], "  healtcheck  ", config["timeout"])