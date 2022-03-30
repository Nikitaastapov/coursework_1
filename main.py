import json
import requests
from pprint import pprint
import pandas as pd

with open ('token_nik.txt', 'r') as file:
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
        file['file_width'] = list['sizes'][-1]['width']
        file['file_height'] = list['sizes'][-1]['height']
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
            info = self.sort_json(files_dict)
            json.dump(info, f, ensure_ascii=False, indent=2)
        
        return 'Done' 
        
        
    def sort_json(self, files_dict):
        pd_file = pd.DataFrame(files_dict['items'])
        # print(pd)
        pd_sorted =pd_file.sort_values(['file_height', 'file_width'], ascending=False)
        # print(pd_sorted)
        pd_dict = pd_sorted.to_dict('records')
        # print(pd_dict)
        files_dict={'items':[]}
        files_dict['items'] = pd_dict
        return files_dict
        

       
            





if __name__ =='__main__':
    vk_client = VKuser(token, '5.131')
    pprint(vk_client.create_file_json())

