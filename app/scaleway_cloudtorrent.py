#! python2

#import console
#import dialogs
import urllib2
import json
import requests
import time

api_token = "aaabbb11-9087-5678-1234-000000aaaaaa"
organization = "aaabbb11-9087-5678-5555-000000bbbbbb"
baseurl = "https://cp-par1.scaleway.com"
image = "c564be4f-2dac-4b1b-a239-3f3a441700ed"
headers = {
  "X-Auth-Token":api_token,
  "Content-Type":"application/json"
}


def get_tokens():
    print("getting user data...")
    url = "https://account.scaleway.com/tokens"

    response = requests.get(url,headers=headers)
    r = json.loads(response.text)

    print(r)


def get_user_organizations():
    print("getting user organizations...")
    url = 'https://account.scaleway.com/organizations'

    response = requests.get(url,headers=headers)
    r = json.loads(response.text)

    print(r)


#TODO fix 404 error
def get_user_data():
    print("getting user data...")
    url = baseurl+'/user_data'

    response = requests.get(url,headers=headers)
    r = json.loads(response.text)

    print(r)


def get_images():
    print("getting user data...")
    url = baseurl+'/images'

    response = requests.get(url,headers=headers)
    r = json.loads(response.text)

    print(r)


def list_servers():
    print("listing servers...")
    url = baseurl+"/servers"

    response = requests.get(url,headers=headers)
    r = json.loads(response.text)

    print(r)


def list_volumes():
    print("listing volumes...")
    url = baseurl+"/volumes"

    response = requests.get(url,headers=headers)
    r = json.loads(response.text)

    print(r)

    return(r)


def delete_volume(volume_id):
    print("deleting volume...")

    url = baseurl+"/volumes/"+volume_id

    response = requests.delete(url,headers=headers)

    if response.status_code == 204:
      print('Volume ' + volume_id + ' successfully deleted')
    else:
      print('There was an error while trying to delete volume: ' + volume_id)


def delete_orphan_volumes():
    print("deleting orphans volumes...")

    v = list_volumes()
    volumes = v['volumes']

    for volume in volumes:
      if (volume['server'] == None):
        volume_id = volume['id']
        delete_volume(volume_id)


def get_server_ip(server_id):
    print("getting server public IP...")

    # get public IP
    url = baseurl+"/servers/"+server_id

    response = requests.get(url, headers=headers)
    r = json.loads(response.text)
    ip=r['server']['public_ip']['address']
    print(ip)


def power_on(server_id):
    print("powering on server...")
    url = baseurl+"/servers/"+server_id+'/action'
    body = {"action": "poweron"}

    response = requests.post(url, data=json.dumps(body), headers=headers)
    r = json.loads(response.text)

    time.sleep(30)

    # get public IP
    get_server_ip(server_id)


def power_off(server_id):
    print("powering off server...")
    url = baseurl+"/servers/"+server_id+'/action'
    body = {"action": "poweroff"}

    response = requests.post(url, data=json.dumps(body), headers=headers)
    r = json.loads(response.text)


def create_server():
    print("creating server...")

    # create server
    url = baseurl+"/servers"
    body = {
      "organization":organization,
      "name":"cloudtorr2",
      "image":image,
      "commercial_type":"START1-XS",
      "tags":["www"],
      "enable_ipv6":False,
      "boot_type":"local"
    }

    response = requests.post(url, data=json.dumps(body), headers=headers)
    r = json.loads(response.text)
    print(r)
    server_id=r['server']['id']
    print(">>>> SERVER ID: "+server_id)

    time.sleep(10)

    # turn it on
    power_on(server_id)


def destroy_server(server_id):
    print("destroying servers...")
    url = baseurl+"/servers/"+server_id

    response = requests.delete(url,headers=headers)
    if response.status_code == 204:
      print('Server ' + server_id + ' successfully deleted')
    else:
      print('There was an error while trying to delete server: ' + server_id)


if __name__ == '__main__':
    strings = [
      'Scaleway',
      'What do you want to do?',
      '1. List servers',
      '2. Create server and start it',
      '3. Stop server and destroy it',
      '4. Quit'
      ]
    for s in strings:
      print(s)
    t = input('Enter your choice: ')

    if t == 1:
      list_servers()
      #get_user_organizations()
      #get_user_data()
      #list_volumes()
      #delete_volume('')
      #delete_orphan_volumes()
      #power_on('a4efb55f-bafa-43f8-a67f-e2de8e6b28a4')
    elif t == 2:
      create_server()
    elif t == 3:
      power_off('dd531106-d4c0-44db-ae7d-09ce7099424d')
      time.sleep(30)
      destroy_server('7b5e3f84-8aad-496a-a58f-29239de37949')
    else:
      exit()


