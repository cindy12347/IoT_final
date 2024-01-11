import json

json_data = '''
{
"sensorId": "7e8a1261-56a2-4ffd-ac2c-b7a5a1934422",
"value": 4.99,
"timestamp": 1704951904935
}
'''

# Load JSON data
data = json.loads(json_data)

sensor_value = data['value']

# Print or use the extracted value
print("Sensor Value:", sensor_value)

