import sys
from datetime import datetime
from caldav import DAVClient

sys.stdout.reconfigure(encoding='utf-8')

env_file = r"C:\Users\mau\.config\hook\gmail.env"
gmail_user, gmail_pass = None, None

with open(env_file, encoding='utf-8') as f:
    for line in f:
        if line.startswith("GMAIL_USER"):
            gmail_user = line.split("=", 1)[1].strip()
        elif line.startswith("GMAIL_APP_PASSWORD"):
            gmail_pass = line.split("=", 1)[1].strip()

url = f"https://www.google.com/calendar/dav/{gmail_user}/"
client = DAVClient(url=url, username=gmail_user, password=gmail_pass)
principal = client.principal()

calendars = principal.calendars()
familia_cal = None

for cal in calendars:
    cal_name = cal.get_properties().get('{DAV:}displayname', '')
    if 'Fam' in cal_name:
        familia_cal = cal
        print(f"Calendario: {cal_name}\n")
        break

# Listar todos (sem search, apenas list)
try:
    all_events = familia_cal.get_all_events()
    print(f"Total de eventos no calendario: {len(all_events)}\n")
    
    for event in all_events:
        comp = event.icalendar_component
        summary = comp.get("SUMMARY", "?").strip()
        dtstart = comp.get("DTSTART")
        rrule = comp.get("RRULE")
        
        print(f"• {summary}")
        if rrule:
            print(f"  (RECORRENTE: {rrule})")
except Exception as e:
    print(f"Erro: {e}")
