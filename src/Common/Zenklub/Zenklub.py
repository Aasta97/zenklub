
from datetime import datetime
import requests
import json
import os

class Zenklub:
    def __init__(self):
        self.token = self.__generate_token()


    def __generate_token(self):
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


    def get_sessions_data(self):
        """Get sessions data

        :param token: Bearer token auth
        :type token: string
        :return: Sessions json data
        :rtype: json
        """
        
        if not self.token: return { "erro": "Missing token"}
        
        url = 'https://api.zenklub.com.br/appointments?status=new,invite,paid,reschedule,reserved&includeProfessional=true&limit=10'
        headers = {'Authorization': 'Bearer ' + self.token}

        response = requests.get(url, headers=headers)
        return json.loads(response.text)


    def get_uncompleted_sessions_data(self, sessions):
        """ Filter new sessions

        :param sessions: Sessions data
        :type sessions: json
        :return: Filtered sessions
        :rtype: list
        """
        
        now = datetime.now()

        result = []
        for session in sessions["items"]:
            day = str(session["day"]).replace('T', ' ').replace('.000Z', '')
            day = datetime.strptime(day, '%Y-%m-%d %H:%M:%S')
            if day >= now:
                result.append({
                    "paymentDate": session["paymentDate"],
                    "professionalName": session["professionalName"],
                    "day": session["day"],
                    "dayEnd": session["dayEnd"],
                    "originalPrice": session["originalPrice"]
                })
        
        return result
    