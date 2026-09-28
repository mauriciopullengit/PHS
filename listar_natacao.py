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
        break

events = familia_cal.search(
    start=datetime(2026, 5, 1),
    end=datetime(2026, 7, 1),
    expand=False
)

print("Todos os eventos 'Natacao Amora':\n")
for event in events:
    comp = event.icalendar_component
    summary = comp.get("SUMMARY", "").strip()
    
    if "Natacao Amora" in summary:
        uid = comp.get("UID", "").strip()
        rrule = comp.get("RRULE")
        recurrence_id = comp.get("RECURRENCE-ID")
        dtstart = comp.get("DTSTART")
        
        print(f"Titulo: {summary}")
        print(f"  UID: {uid}")
        print(f"  Data: {dtstart.dt if hasattr(dtstart, 'dt') else dtstart}")
        print(f"  RRULE: {rrule}")
        print(f"  RECURRENCE-ID: {recurrence_id}\n")
