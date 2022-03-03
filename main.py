import json
import requests

url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyBmvSYlFxiQYhaxpUeresGeaSdkjP1w-gs'
    
data = {
	"email": "",
	"password": "",
	"returnSecureToken": True
}


r = requests.post(url, data=data)
response = json.loads(r.text)

hed = {'Authorization': 'Bearer ' + response['idToken']}

with requests.Session() as s:    
    r = s.get('https://api.zenklub.com.br/appointments?status=new,invite,paid,reschedule,reserved&includeProfessional=true&limit=10', headers=hed)
    response = json.loads(r.text)
    
    from pprint import pprint
    pprint(response)
    with open('data.json', 'w') as f:
        json.dump(response, f)