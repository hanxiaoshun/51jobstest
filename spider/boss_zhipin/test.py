import requests

res = requests.get('https://www.zhipin.com')

res.encoding = res.apparent_encoding

print(res.text)