import os
import requests
from string import Template

'''
Default configuration values.
These can be modified as needed.
'''
defaults = {
    "destination_folder": "replays",      #Folder where replay files will be saved. Can be changed to any valid path.
    "game": "age2",                       #The Age of {x} title to use. Could be potentially used for other titles. Currently only tested with age2.
    "profile_id": 199325,                  #Hera's profile ID, used for testing. Can be replaced with any profile ID.
    "match_id": 453704442,                 #A match ID from Hera's profile, used for testing. Can be replaced with any match ID.
}

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
#Appears to work without cookies, but including them here to match the captured request.
#'cookie':'MSCC=cid=7ztop15tvhqdnrdzi8yiujxo-c1=2-c2=2-c3=2; age-user=true; age_login_expire=1'
}

endpoints = {
    "replay":
                    {
                    "endpoint": "https://api.ageofempires.com/api/GameStats/AgeII/GetMatchReplay/?matchId={match_id}&profileId={profile_id}",
                    "method": "GET"
                    },
    "match_details": 
                    {
                    "endpoint": "https://api.ageofempires.com/api/GameStats/AgeII/GetMatchDetail",
                    "method": "POST"
                    },
    "player_stats": {
                    "endpoint": "https://api.ageofempires.com/api/GameStats/AgeII/GetFullStats",
                    "method": "POST"
                    },
    "player_match_list":
                    {
                    "endpoint": "https://api.ageofempires.com/api/GameStats/AgeII/GetMatchList",
                    "method": "POST"
                    },
    "player_campaign_stats": 
                    {
                    "endpoint": "https://api.ageofempires.com/api/GameStats/AgeII/GetCampaignStats",
                    "method": "POST"
                    },
    "leaderboard":
                    {
                    "endpoint": "https://api.ageofempires.com/api/v2/ageii/Leaderboard",
                    "method": "POST"
                    },
}

def get_replay_url(match_id, profile_id = 1):
    '''
    Constructs the URL to fetch the replay file for a given match ID and profile ID.
    Profile ID can be anything, as long as somthing is included. Default=1.
    '''
    url = f'https://api.ageofempires.com/api/GameStats/AgeII/GetMatchReplay/?matchId={match_id}&profileId={profile_id}'
    return url

def fetch_replay(match_id, profile_id = 1, destination_folder=defaults["destination_folder"]):
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

def fetch_player_match_list(profile_id, game=defaults["game"], sortColumn="dateTime", sort_direction="DESC", match_type="3"):
    '''
    Fetches the match list for a given profile ID. Only the 10 most recent matches are returned.
    Additional parameters can be set to modify the results.
    '''

    #Full payload example for fetching player match list, captured using Fiddler Everywhere:
    #{"gamertag":"unknown user","playerNumber":0,"undefined":null,"game":"age2","profileId":199325,"sortColumn":"dateTime","sortDirection":"DESC","page":1,"recordCount":10,"matchType":"3"}

    #Only profileId, game, sortColumn, sortDirection, and matchType appear to be required. The rest have no effect.
    #   * (Setting "page" as anything other than 1 appears to return an empty list.)
    #   * It is unclear if setting "game" to anything other than AOE2 will have any effect. (ie. AOE1)
    #   * sortColumn can be dateTime, wins, or civilization
    #   * sortDirection can be ASC or DESC
    #TODO: Investigate matchType values further. Known matchType values: 
    # 1:  Deathmatch
    # 2:  Team Deathmatch
    # 3:  1v1 RandomMap
    # 4:  Team RandomMap
    # 13: Empire Wars
    # 14: Team Empire Wars
    # 25: Return of Rome
    # 26: ??Team Return of Rome **Unconfirmed
    # 29: RedBull Wololo: Londinium

    payload = f'{{"game":"{game}","profileId":"{profile_id}","sortColumn":"{sortColumn}", "sortDirection":"{sort_direction}","matchType":"{match_type}"}}'
    response = fetch_endpoint("player_match_list", profile_id=profile_id, data=payload)    
    return response

def fetch_leaderboard(region="7", match_type="3", console_match_type=15, search_player="", page=1, count=100, sort_column="rank", sort_direction="ASC"):
    '''
    Fetches the leaderboard by region and matchtype. Returns the top 100 players per page. Can also be used for player search by name.
    '''
    payload = f'{{"region":"{region}","matchType":"{match_type}","consoleMatchType":{console_match_type},"searchPlayer":"{search_player}","page":{page},"count":{count},"sortColumn":"{sort_column}","sortDirection":"{sort_direction}"}}'
    response = fetch_endpoint("leaderboard", data=payload)
    return response

def fetch_endpoint(endpoint_name=None, profile_id=1, match_id=1, headers=default_headers, data=None):
    '''
    Fetches various stats from the Age of Empires API. Endpoint must be specified. 
    In the case of a GET request, data will contain the values to be passed in the URL.
    In the case of a POST request, data will contain the payload to be sent in the body of the request,
    which must be in the format of a valid JSON string.
    If no data is provided, a default values will be used for the url/payload.

    If profile_id and match_id are included, they will be used to construct the default payload/url.
    '''

    #Validate the endpoint
    if not endpoint_name or endpoint_name not in endpoints:
        return {"status_code": 400, "message": f"Invalid or missing endpoint. Valid endpoints are: {list(endpoints.keys())}", "content": None}

    #Default payload
    if not data:
        data= f'{{"matchId":"{match_id}", "game":"{defaults["game"]}", "profileId":"{profile_id}"}}'
    
    #Fetch the stats from the API
    print(f"Fetching stats from endpoint: {endpoint_name} with payload: {data}")
    variables = {}

    if endpoints[endpoint_name]["method"] == "GET":
        values = data
        final_endpoint = Template(endpoints[endpoint_name]["endpoint"]).substitute(**values)
        response = requests.request("GET", final_endpoint, headers=headers)
    elif endpoints[endpoint_name]["method"] == "POST":
        response = requests.request("POST", f"{endpoints[endpoint_name]['endpoint']}", headers=headers, data=data)
    else:
        return {"status_code": 400, "message": f"Invalid method for endpoint {endpoint_name}", "content": None}
    
    return {"status_code": response.status_code, "message": response.reason, "content": response.content}

def main():
    match_id = defaults["match_id"] 
    profile_id = defaults["profile_id"]
    # status_code = fetch_replay(match_id, 1)
 
    match_details = fetch_endpoint("match_details", profile_id, match_id)
    full_stats = fetch_endpoint("player_stats", profile_id, match_id)
    player_match_list = fetch_player_match_list(profile_id, match_type="3")
    campaign_stats = fetch_endpoint("player_campaign_stats", profile_id)
    leaderboard = fetch_leaderboard()

    print(f"Match Details Response: {match_details['status_code']} {match_details['message']} \nContents:\n {match_details['content']}\n")
    print(f"Full Stats Response: {full_stats['status_code']} {full_stats['message']} \nContents:\n {full_stats['content']}\n")
    print(f"Player Match List Response: {player_match_list['status_code']} {player_match_list['message']} \nContents:\n {player_match_list['content']}\n")
    print(f"Campaign Stats Response: {campaign_stats['status_code']}  {campaign_stats['message']} \nContents:\n {campaign_stats['content']}\n")
    print(f"Leaderboard Response: {leaderboard['status_code']}  {leaderboard['message']} \nContents:\n {leaderboard['content']}\n")

if  __name__ == "__main__":
    main()