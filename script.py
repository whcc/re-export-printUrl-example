import os
import json
import requests
import random

prospector_url = os.environ.get('PROSPECTOR_URL')
key_id = os.environ.get('CLIENT_KEY_ID')
key_secret = os.environ.get('CLIENT_KEY_SECRET')
editor_id = os.environ.get('EDITOR_ID')
user_id = os.environ.get('USER_ID')

def fetch_token():
    payload = { 'key': key_id, 'secret': key_secret, 'claims': { 'accountId': user_id }}
    token_response = requests.post(f'{prospector_url}/auth/access-token', data=json.dumps(payload))
    return token_response.json()

def fetch_editor(auth, editor_id):
    response = requests.get(f'{prospector_url}/editors/{editor_id}', headers=auth)
    return response.json()

def list_photos(photos):
    photos = [{ 'printUrl': x['printUrl'], 'id': x['id']} for x in photos]
    return photos

def update_photos(photos):
    for p in photos:
        width = random.randrange(100, 900)
        height = random.randrange(100, 900)
        p['printUrl'] = f'https://placekitten.com/g/{width}/{height}'

    return photos

def export_editor(auth, editor_id, photos):
    payload = {'editors': [{'editorId': editor_id, 'photos': photos}] }
    response = requests.put(f'{prospector_url}/oas/editors/export', headers=auth, data=json.dumps(payload))
    return response

print('Fetching Token...')
token_response = fetch_token()
token = token_response['accessToken']

auth_header = { 'Authorization': f'Bearer {token}'}
print('Fetching Editor')
editor = fetch_editor(auth_header, editor_id)

print('Getting list of photos')
photos = list_photos(editor['photos'])

print('Replacing printUrls')
updated_photos = update_photos(photos)
print(json.dumps(updated_photos, indent=4))

print('Re-exporting with new printUrls')
response = export_editor(auth_header, editor_id, photos)
print(json.dumps(response.json(), indent=4))
print('Complete')


