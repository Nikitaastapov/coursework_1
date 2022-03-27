import json
import requests
from pprint import pprint

with open ('token_test.txt', 'r') as file:
    token = file.read().strip()
    
class VKuser:
    url = 'https://api.vk.com/method/'
    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
            }
        
    def get_photo_profile(self):
        photo_profile_url = self.url + 'photos.get'
        photo_profile_params = {
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            # 'count': 5
            }
        req = requests.get(photo_profile_url, params ={**self.params, **photo_profile_params}).json()
        return req
    
    def get_info_photo(self, list):
        file={}
        file['file_name'] = self.file_name(list['likes']) + str(list['date']) + '.jpeg'
        file['size'] = list['sizes'][-1]['type']
        file['url'] =  list['sizes'][-1]['url']
        return file
    
    def file_name(self, list):
        sum = 0
        for keys, values in list.items():
            sum+=values
        return str(sum)
        
            
            
    def create_file_json(self):
        files_dict={'items':[]}
        photos_album = self.get_photo_profile()
        for i in photos_album['response']['items']:
            # print(self.get_info_photo(i))
            files_dict['items'].append(self.get_info_photo(i))
        
        with open ('photo_info.json','w',encoding = 'utf-8') as f:
            json.dump(files_dict, f, ensure_ascii=False, indent=2)
        
        return files_dict
            
            
            
            
            
            
            


# url = 'https://api.vk.com/method/users.get'
# params = {
#     # 'user_ids': '1',
#     'access_token': token,
#     'v': '5.131',
#     'fields': 'education, sex',
#     }
# res = requests.get(url, params = params)
# pprint(res.json())

# url = 'https://api.vk.com/method/groups.search'
# def search_group(q, sorting =0):
#     params = {
#         'q': q,
#         'access_token': token,
#         'v': 5.131,
#         'sort': sorting,
#         'count': 300
#         }
#     req = requests.get(url, params = params)
#     req = req.json()['response']['items']
#     return req

# target_groups = search_group('python')
# # pprint(target_groups)
# target_groups_ids = ','.join(str(group['id']) for group in target_groups)
# pprint(target_groups_ids)

# class VKuser:
#     url = 'https://api.vk.com/method/'
#     def __init__(self, token, version):
#         self.params = {
#             'access_token': token,
#             'v': version
#             }
        
    def search_group(self, q, sorting =0):
        group_search_url = self.url + 'groups.search'
        group_search_params = {
            'q': q,
            'sort': sorting,
            'sort': sorting,
            }
        req = requests.get(group_search_url, params ={**self.params, **group_search_params}).json()
        return req['response']['items']
    
    def search_group_ext(self, q, sorting = 0):
        group_search_ext_url = self.url + 'groups.getById'
        target_groups = self.search_group(q, sorting)
        target_groups_ids = ','.join(str(group['id']) for group in target_groups)
        # print(target_groups_ids)
        groups_info_params = {
            'group_ids': target_groups_ids,
            'fields':'members_count,activity, description'
            }
        req = requests.get(group_search_ext_url, params = {**self.params, **groups_info_params}).json()
        return req['response']
    
    def get_followers(self, user_id = None):
        followers_url = self.url +'users.getFollowers'
        followers_params ={
            'count': 1000,
            'user_id': user_id
            }
        res = requests.get(followers_url, params = {**self.params, **followers_params}).json()
        return res['response']
    
    def get_groups(self, user_id = None):
        groups_url = self.url +'groups.get'
        groups_params ={
            'count': 1000,
            'user_id': user_id,
            'extended': 1,
            'fields': 'members_count'
            }
        res = requests.get(groups_url, params = {**self.params, **groups_params}).json()
        return res
    
    def get_news(self, query):
        news_url = self.url +'newsfeed.search'
        news_params ={
            'q': query,
            'count': 200,
            }
        # res = requests.get(news_url, params = {**self.params, **news_params}).json()
        # return res
        result = {}
        
        while True:
            res = requests.get(news_url, params = {**self.params, **news_params}).json()
            time.sleep(0.33)
            result = res['response']['items']
            if 'next_from' in res['response'].keys():
                news_params['start_from'] = res['response']['next_from']
            else:
                break
        return result
    



vk_client = VKuser(token, '5.131')
# pprint(vk_client.search_group('python'))
# pprint(vk_client.search_group_ext('python'))
# vk_client.search_group_ext('python')

# import pandas as pd
# pd.DataFrame(vk_client.search_group_ext('python'))
# pprint(vk_client.get_followers(1))
# pprint(vk_client.get_groups())
pprint(vk_client.create_file_json())