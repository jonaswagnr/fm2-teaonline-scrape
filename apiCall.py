import requests

# The API URL
url = 'https://www.basededatostea.xyz/api/v2/cards/getData?v=5&card=613'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Print or process the data
    print(data)
else:
    print(f"Failed to retrieve data: {response.status_code}")
