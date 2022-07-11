VERSION = "0.0.1"
FILE_TYPE = {
    "JSON": "json"
}
SERVICE_TYPE = {
    "REDIS": "redis",
    "MYSQL": "mysql",
    "INFLUXDB": "influxdb",
    "RABBIT_MQ": "rabbit_mq",
    "REST_API": "rest_api"
}
CONFIG_FIELD_REQUIRED = [{"name": "services", "type": list}]
CONFIG_SERVICE_FIELD_REQUIRED = [{"name": "name", "type": str}, {"name": "type", "type": str}, {"name": "timeout", "type": int}]