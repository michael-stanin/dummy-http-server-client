import requests
import time

if __name__ == '__main__':
    while True:
        r = requests.get('http://localhost:5000/') # used in docker-compose
        #r = requests.get('http://http-server-service:5000/') # used in k8s
        print(r.text)
        time.sleep(1)
