import json
import requests
from pprint import pprint
import pandas as pd
import datetime
import time
from progress.bar import IncrementalBar
bar = IncrementalBar('Countdown', max = 5)

with open ('token_test.txt', 'r') as file:
    token = file.read().strip()
    
class VKuser:
    url = 'https://api.vk.com/method/'
    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
            }
        
    def get_photo_profile(self, owner_id = None):
        photo_profile_url = self.url + 'photos.get'
        photo_profile_params = {
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'owner_id': owner_id
            }
        req = requests.get(photo_profile_url, params ={**self.params, **photo_profile_params}).json()
        # print('get_photo_profile')
        return req
    
    def get_info_photo(self, list):
        file={}
        file['file_name'] = self.file_name(list['likes']) + str(list['date']) + '.jpeg'
        file['file_width'] = list['sizes'][-1]['width']
        file['file_height'] = list['sizes'][-1]['height']
        file['size'] = list['sizes'][-1]['type']
        file['url'] =  list['sizes'][-1]['url']
        # print('get_info_photo')
        return file
    
    def file_name(self, list):
        sum = 0
        for keys, values in list.items():
            sum+=values
        # print('file_name')
        return str(sum)
        
    def create_file_json(self, owner_id = None):
        files_dict={'items':[]}
        photos_album = self.get_photo_profile(owner_id)
        n=1
        for i in photos_album['response']['items']:
            # print(self.get_info_photo(i))
            files_dict['items'].append(self.get_info_photo(i))
            print(f'Количество полученых строк {n}')
            n+=1
        
        with open ('photo_info.json','w',encoding = 'utf-8') as f:
            info = self.sort_json(files_dict)
            json.dump(info, f, ensure_ascii=False, indent=2)
        
        return "Файл photo_info.json сформирован"
        
        
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
    

class YD_user:
    def __init__(self, token: str):
        self.token = token
        
    def add_directory(self, date=str):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        # today = datetime.date.today()
        headers = {'Content-Type': 'application/json', 'Authorization': 'OAuth {}'.format(self.token)}
        params = {'path': date}
        response = requests.put(upload_url, headers = headers, params=params)
        # print('add_directory')
    
    def check_directory(self):
        today = datetime.date.today()
        check_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Content-Type': 'application/json', 'Authorization': 'OAuth {}'.format(self.token)}
        params = {'path':'/'}
        response = requests.get(check_url, headers = headers, params=params).json()
        check_list=[]
        for i in response['_embedded']['items']:
            check_list.append(i['name'])
        if str(today) not in check_list:
            self.add_directory(today)
        return(str(today))
        
    def check_photo(self, file_name):
        check_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Content-Type': 'application/json', 'Authorization': 'OAuth {}'.format(self.token)}
        params = {'path': f'/{self.check_directory()}/'}
        response = requests.get(check_url, headers = headers, params=params).json()
        check_list=[]
        for i in response['_embedded']['items']:
            if i['name'] not in check_list:
                check_list.append(i['name'])        
        if file_name not in check_list:
            return True
        else:
                return False
            
    def upload(self):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        with open ('photo_info.json', encoding='utf-8') as f:
            data = json.load(f)
            upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            for i in data['items'][:5]:
                file_name = i["file_name"]
                file_url = i['url']
                if self.check_photo(file_name) == True:
                    # print(i["file_name"], i['url'])
                    headers = {'Content-Type': 'application/json', 'Authorization': 'OAuth {}'.format(self.token)}
                    path = f'/{self.check_directory()}/{file_name}'
                    # print(path)
                    params = {'path': path,'url': file_url}
                    response = requests.post(upload_url, headers=headers, params=params)
                    # print('done')
                bar.next()
                time.sleep(1)
            bar.finish()
            return response.json()
        
      



if __name__ =='__main__':
    ID_user_VK = input('Введите id пользователя vk: ')
    Yandex_token = input('Введите токен с полигона ЯндексДиск: ')
    
    vk_client = VKuser(token, '5.131')
    pprint(vk_client.create_file_json(ID_user_VK))
    YD_user = YD_user(Yandex_token)
    YD_user.upload()
