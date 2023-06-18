import requests
import random
import time
import json
from faker import Faker

fake = Faker()

LOGIN_URL = 'http://127.0.0.1:8000/api/users/login/'
credentials = {
    'username': 'sveta',
    'password': '111'
}

response = requests.post(LOGIN_URL, json=credentials)
response.raise_for_status()
access_token = response.json()['access_token']

headers = {
    'Authorization': f'Bearer {access_token}'
}

USERS_URL = 'http://127.0.0.1:8000/api/users/list/'
response = requests.get(USERS_URL, headers=headers)
response.raise_for_status()
users = response.json()

buyers = [user['id'] for user in users if user['position'] == 'Buyer']
team_leads = [user['id'] for user in users if user['position'] == 'Team Lead']

TEAMS_URL = 'http://127.0.0.1:8000/api/teams/create/'

while buyers and team_leads:
    team_lead = random.choice(team_leads)
    team_leads.remove(team_lead)

    num_members = min(random.randint(3, 8), len(buyers))
    members = random.sample(buyers, num_members)

    for member in members:
        buyers.remove(member)

    payload = {
        'name': fake.company().capitalize(),
        'team_lead': team_lead,
        'members': members
    }

    while True:
        try:
            response = requests.post(TEAMS_URL, json=payload, headers=headers)
            response.raise_for_status()
            print(f"Successfully created team: {payload['name']}")
            break
        except requests.exceptions.HTTPError as e:
            try:
                error_message = json.loads(response.text)
                if 'team_lead' in error_message and 'already exists' in error_message['team_lead'][0]:
                    print(f"Team Lead already exists. Skipping...")
                    break
                else:
                    print(f"Failed to create team due to {e}. Server response: {response.text}")
            except json.decoder.JSONDecodeError:
                print(f"Failed to parse server response as JSON: {response.text}")
                continue
            time.sleep(1)
