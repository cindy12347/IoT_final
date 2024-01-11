import json

json_data = '''
{
  "Items": [
    {"sensorId": "7e8a1261-56a2-4ffd-ac2c-b7a5a1934422", "value": 10, "timestamp": 1704907311714},
    {"sensorId": "7e8a1261-56a2-4ffd-ac2c-b7a5a1934422", "value": 10, "timestamp": 1704907317562},
    {"sensorId": "7e8a1261-56a2-4ffd-ac2c-b7a5a1934422", "value": 19.63, "timestamp": 1704907322996},
    {"sensorId": "7e8a1261-56a2-4ffd-ac2c-b7a5a1934422", "value": 20.46, "timestamp": 1704907327674},
    {"sensorId": "7e8a1261-56a2-4ffd-ac2c-b7a5a1934422", "value": 12.41, "timestamp": 1704907338053},
    {"sensorId": "7e8a1261-56a2-4ffd-ac2c-b7a5a1934422", "value": 23.2, "timestamp": 1704907348777}
  ],
  "Count": 6,
  "ScannedCount": 6
}
'''

# Load JSON data
data = json.loads(json_data)

# Extract values
values = [item["value"] for item in data["Items"]]

# Convert values list to a string
values_text = ', '.join(map(str, values))

# Print the values as text
print("Values as text:", values_text)
