import requests
from requests.auth import HTTPDigestAuth

def Auth_methods(user:str,password:str):
    url = f"https://httpbin.org/basic-auth/{user}/{password}"
    response = requests.get(url,auth = (user,password), timeout = 10)
    if response.status_code ==200:
        return response.json(),response.status_code
    return response.status_code
result1 = Auth_methods("panich","12345")
print('===Auth_methods===')
print(result1)

def Bearer_methods(token:str):
    url = f"https://httpbin.org/bearer"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url,headers = headers,timeout = 10)
    if response.status_code ==200:
        return response.json(),response.status_code
    return response.status_code
result2 = Bearer_methods("token_jgjhkkfl")
print('===Bearer_methods===')
print(result2)

def Digest_methods(qop:str, user:str, password:str):
    url = f"https://httpbin.org/digest-auth/{qop}/{user}/{password}"
    response = requests.get(url,auth = HTTPDigestAuth(user, password), timeout = 10)
    if response.status_code ==200:
        return response.json(),response.status_code
    return response.status_code
result3 = Digest_methods("qop", "panich", "12345")
print('===Digest_methods===')
print(result3)

def Digest_auth_methods(qop:str, user:str, password:str, algoritm:str = 'MD5'):
    url = f"https://httpbin.org/digest-auth/{qop}/{user}/{password}/{algoritm}"
    response = requests.get(url,auth = HTTPDigestAuth(user, password), timeout = 10)
    if response.status_code ==200:
        return response.json(),response.status_code
    return response.status_code
result4 = Digest_auth_methods("qop", "panich", "12345", "MD5")
print('===Digest_auth_methods===')
print(result4)

def Digest_auth_methods_stale_after(qop:str, user:str, password:str, algoritm:str = 'MD5', stale_after:str = 'never'):
    url = f"https://httpbin.org/digest-auth/{qop}/{user}/{password}/{algoritm}/{stale_after}"
    response = requests.get(url,auth = HTTPDigestAuth(user, password), timeout = 10)
    if response.status_code ==200:
        return response.json(),response.status_code
    return response.status_code
result5 = Digest_auth_methods_stale_after("qop", "panich", "12345", "MD5",'never')
print('===Digest_auth_methods_stale_after===')
print(result5)

def Hidden_basic_auth_methods(user: str, password: str):
    url = f"https://httpbin.org/hidden-basic-auth/{user}/{password}"
    response = requests.get(url, auth = (user,password), timeout = 10)
    if response.status_code ==200:
        return response.json(),response.status_code
    return response.status_code
result6 = Hidden_basic_auth_methods("panich", "12345")
print('===Hidden_basic_auth_methods==')
print(result6)
