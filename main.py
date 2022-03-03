import requests
import json
import os

def generate_token():
    """ Generate bearer token

    :return: Return json response
    :rtype: json
    """
    
    url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyBmvSYlFxiQYhaxpUeresGeaSdkjP1w-gs'
    
    data = {
        "email": os.environ['EMAIL'],
        "password": os.environ['SENHA'],
        "returnSecureToken": True
    }

    response = requests.post(url, data=data)

    try:
        return json.loads(response.text)['idToken']
    except: return False


def get_sessions_data(token):
    """Get sessions data

    :param token: Bearer token auth
    :type token: string
    :return: Sessions json data
    :rtype: json
    """
    
    if not token: return { "erro": "Missing token"}
    
    url = 'https://api.zenklub.com.br/appointments?status=new,invite,paid,reschedule,reserved&includeProfessional=true&limit=10'
    headers = {'Authorization': 'Bearer ' + token}

    response = requests.get(url, headers=headers)
    return json.loads()

if __name__ == '__main__':
    token = generate_token()
    sessions = get_sessions_data(token)      
        
    print(sessions)