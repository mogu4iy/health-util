from dotenv import load_dotenv
import copy
import json
import os
from .config import SERVICE_TYPE, CONFIG_FIELD_REQUIRED, CONFIG_SERVICE_FIELD_REQUIRED

def parse_config(config_path) -> dict:
    with open(config_path, 'r') as file:
        try:
            config = json.load(file)
        except:
            raise Exception("Config: invalid JSON.")
        return config

def resolve_config(config) -> dict:
    resolved_config = copy.deepcopy(config)
    resolved_config["services"] = []
    for service in config["services"]:
        resolved_service = {}
        for field in service.keys():
            if field in map(lambda x: x["name"],CONFIG_SERVICE_FIELD_REQUIRED):
                resolved_service[field] = service[field]
                continue
            if service[field].get("env") is not None:
                resolved_service[field] = os.getenv(service[field].get("env"))
                continue
            if service[field].get("value") is not None:
                resolved_service[field] = service[field].get("value")
                continue
        resolved_config["services"].append(resolved_service)
    return resolved_config

def get_config(config_path, env_path) -> dict:
    if env_path:
        load_dotenv(env_path)
    config = parse_config(config_path)
    validate_schema(config)
    resolved_config = resolve_config(config)
    validate_config(config, resolved_config)
    return resolved_config

def validate_service_schema(config) -> None:
    for field in CONFIG_SERVICE_FIELD_REQUIRED:
        if config.get(field["name"]) is None:
            raise Exception(f"Service: field '{field['name']}' is required.")
        if type(config[field["name"]]) != field["type"]:
            raise Exception(f"Service: field '{field['name']}' is invalid.")
    for field in config.keys():
        if config.get(field) is None:
            raise Exception(f"Service: field '{field}' is invalid.")
    if config["type"] not in SERVICE_TYPE.values():
        raise Exception(f"Service: type '{config['type']}' is invalid.")
    for config_type in SERVICE_TYPE.values():
        if config["type"] != config_type:
            continue
        validate = __import__(f'{config_type}', globals(), locals(), [], 1).validate_service_schema
        validate(config)
        break

def validate_schema(config) -> None:
    for field in CONFIG_FIELD_REQUIRED:
        if config.get(field["name"]) is None:
            raise Exception(f"Config: field '{field['name']}' is required.")
        if type(config[field["name"]]) != field["type"]:
            raise Exception(f"Config: field '{field['name']}' is invalid.")
    for service in config["services"]:
        validate_service_schema(service)

def validate_service(schema, config) -> None:
    for config_type in SERVICE_TYPE.values():
        if config["type"] != config_type:
            continue
        validate = __import__(f'{config_type}', globals(), locals(), [], 1).validate_service
        validate(schema, config)
        break

def validate_config(schema, config) -> None:
    for index, service in enumerate(config["services"]):
        validate_service(schema["services"][index], service)

def health_check(config):
    for config_type in SERVICE_TYPE.values():
        if config["type"] != config_type:
            continue
        check = __import__(f'{config_type}', globals(), locals(), [], 1).health_check
        check(config)
        break