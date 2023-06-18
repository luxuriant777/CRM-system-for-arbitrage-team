import requests

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

list_url = 'http://127.0.0.1:8000/api/teams/list/'
response = requests.get(list_url, headers=headers)
response.raise_for_status()

teams = response.json()
team_ids = [team['id'] for team in teams]

base_url = 'http://127.0.0.1:8000/api/teams/delete/'

for id_counter in team_ids:
    delete_url = base_url + str(id_counter)

    try:
        response = requests.delete(delete_url, headers=headers)
        response.raise_for_status()
        print(f"Successfully deleted team with id: {id_counter}")
    except requests.exceptions.HTTPError as e:
        print(f"No team found with id: {id_counter}, Error: {e}")
