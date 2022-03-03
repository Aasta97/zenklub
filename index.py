from src.Common.Google.Calendar import Calendar
from src.Common.Zenklub.Zenklub import Zenklub

if __name__ == '__main__':
    zenklub  = Zenklub()
    calendar = Calendar()

    sessions = zenklub.get_sessions_data()
    sessions = zenklub.get_uncompleted_sessions_data(sessions)
    events   = calendar.list_events()
    
    for session in sessions:
        summary     = f'Sessão - {session["professionalName"]} - {session["day"][:10]}'
        description = f'Sessão de terapia com a {session["professionalName"]} na data {session["day"][:10]}'
        body        = {
            "summary": summary,
            "description": description,
            "start": {"dateTime": session["day"], "timeZone": 'America/Sao_Paulo'},
            "end": {"dateTime": session["dayEnd"], "timeZone": 'America/Sao_Paulo'},
        }
        

        try: summaries = [event["summary"] for event in events if summary == event["summary"]]
        except: 
            print('Criando evento', summary)
            calendar.create_event(body)
        
        for event in events: 
            
            if len(summaries) == 0: 
                print('Criando evento', summary)
                calendar.create_event(body)
                break
            
            if summary == event["summary"]: 
                print('Alterando evento', summary)
                calendar.update_event(body, event_id=event["id"])  