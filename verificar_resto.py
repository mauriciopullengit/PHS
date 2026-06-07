import sys
import unicodedata
from datetime import datetime
from caldav import DAVClient

sys.stdout.reconfigure(encoding='utf-8')

env_file = r"C:\Users\mauri\.config\hook\gmail.env"
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

start = datetime(2026, 5, 1, 0, 0, 0)
end = datetime(2026, 12, 31, 23, 59, 59)

events = familia_cal.search(start=start, end=end, expand=True)

print(f"Verificando 'Natacao Amora' em todo o periodo (mai-dez)...\n")

natacao_events = []
for event in events:
    comp = event.icalendar_component
    summary = str(comp.get("SUMMARY", "")).strip()
    dtstart = comp.get("DTSTART")
    
    summary_normalized = unicodedata.normalize('NFD', summary).encode('ascii', 'ignore').decode()
    
    if "Natacao" in summary_normalized and "Amora" in summary_normalized:
        natacao_events.append(str(dtstart.dt))

if natacao_events:
    print(f"Encontrados {len(natacao_events)} evento(s) 'Natacao Amora':\n")
    for dt in sorted(natacao_events):
        print(f"  • {dt}")
else:
    print("Nenhum evento 'Natacao Amora' encontrado (SUCESSO!)")
