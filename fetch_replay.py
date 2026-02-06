import os
import requests
import base64

default_desitnation_folder = 'replays'

'''
Example headers and payload for fetching match details.
These were captured using Fiddler Everywhere while using the Age of Empires website.
'''
default_headers = {
 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
 'accept':'application/json, text/javascript, */*; q=0.01',
 'accept-language':'en-US,en;q=0.9',
 'accept-encoding':'gzip, deflate, br, zstd',
 'content-type':'application/json',
 'content-length':'58',
 'origin':'https://www.ageofempires.com',
 'dnt':'1',
 'sec-gpc':'1',
 'referer':'https://www.ageofempires.com/',
 'sec-fetch-dest':'empty',
 'sec-fetch-mode':'cors',
 'sec-fetch-site':'same-site',
 'te':'trailers',
#Appears to work without cookies, but including them to match the captured request.
#'cookie':'MSCC=cid=7ztop15tvhqdnrdzi8yiujxo-c1=2-c2=2-c3=2; age-user=true; age_login_expire=1'
}

endpoints = {
    "match_details": "GetMatchDetail",
    "player_stats": "GetFullStats",
}

def decode_b64_payload(encoded_payload):
    '''
    Helper function for when copying request payloads from Fiddler.
    Used to decode payload to determine its structure.
    Generally only needs to be used when investigating the api.
    '''
    decoded_bytes = base64.b64decode(encoded_payload)
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str

def encode_b64_payload(payload_str):
    '''
    UNUSED HELPER FUNCTION:
    Encodes a payload string to base64.
    Not actually needed for the api requests.
    '''
    encoded_bytes = base64.b64encode(payload_str.encode('utf-8'))
    encoded_str = encoded_bytes.decode('utf-8')
    return encoded_str

def get_replay_url(match_id, profile_id = 1):
    '''
    Constructs the URL to fetch the replay file for a given match ID and profile ID.
    Profile ID can be anything, as long as somthing is included. Default=1.
    '''
    url = f'https://api.ageofempires.com/api/GameStats/AgeII/GetMatchReplay/?matchId={match_id}&profileId={profile_id}'
    return url

def fetch_replay(match_id, profile_id = 1, destination_folder=default_desitnation_folder):
    '''
    Fetches the replay file for a given match ID and profile ID.
    Profile ID can be anything, as long as somthing is included. Default=1.
    Saves the replay file as a zip in the desitnation_folder.
    '''
    url = get_replay_url(match_id, profile_id)
    print(f"Fetching replay from URL: {url}")
    # Download the file from the URL
    response = requests.get(url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        #Create directory if it doesn't exist
        os.makedirs(destination_folder, exist_ok=True)
        # Save the file to the destination folder
        file_name = f'{destination_folder}/{match_id}.zip'
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print(f"File '{file_name}' downloaded successfully!")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
    
    return response.status_code

def fetch_stats(endpoint, match_id=1, profile_id=1, headers=default_headers):
    '''
    Fetches the match details for a given match ID and profile ID.
    Profile ID of one of the human players must be included.
    '''
    # url = get_replay_detail_url(match_id)
    # response = requests.post(url)
    payload = f'{{"matchId":"{match_id}","game":"age2","profileId":"{profile_id}"}}'
    response = requests.request("POST", f"https://api.ageofempires.com/api/GameStats/AgeII/{endpoints[endpoint]}", headers=headers, data=payload)
    
    return response

def main():
    match_id = 45255542
    profile_id = 271202
    # status_code = fetch_replay(match_id, 1)
 
    match_details = fetch_stats("match_details", match_id, profile_id)
    full_stats = fetch_stats("player_stats", match_id, profile_id)

    print(f"Match Details Response: {match_details.status_code} {match_details.content}\n\n")
    print(f"Full Stats Response: {full_stats.status_code} {full_stats.content}\n\n")

if  __name__ == "__main__":
    main()