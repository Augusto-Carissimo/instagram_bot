import json
import requests
import pandas as pd

def get_response_from_medium_api(creds, next_page_token =''):
    url = 'https://photoslibrary.googleapis.com/v1/mediaItems:search'
    payload = {
      "pageSize": 100,
      "pageToken": next_page_token
    }
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(creds.token)
    }

    try:
        res = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    except:
        print('Request error')

    return(res)

def list_of_media_items(creds, retrieved_items, next_page_token =''):
    '''
    Args:
        creds: credentials from credintials/token_photoslibrary_v1.pickle
        retrieved_items: existing data frame with all find media items so far
        next_page_token: request['nextPageToken']
    Return:
        retrieved_items: media items data frame extended by the articles found for the specified tag
        reponse: respose object for nextPageToken

    '''

    items_list_df = pd.DataFrame()

    response = get_response_from_medium_api(creds, next_page_token)

    try:
      for item in response.json()['mediaItems']:
        each_item_df = pd.DataFrame(item)
        each_item_df.drop(['mimeType', 'mediaMetadata'], axis = 1, inplace = True)
        items_list_df = pd.concat([items_list_df, each_item_df])

    except:
      print(response.text)

    items_list_df.drop_duplicates(subset='id', inplace=True)
    media_items_df = pd.concat([retrieved_items, items_list_df])

    return(response, media_items_df)