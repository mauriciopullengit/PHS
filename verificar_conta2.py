import sys
import unicodedata
from datetime import datetime
from caldav import DAVClient

sys.stdout.reconfigure(encoding='utf-8')

env_file = r"C:\Users\mauri\.config\hook\gmail2.env"
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

print(f"Verificando 'Reuniao semanal' em {gmail_user}...\n")

found = False
for cal in calendars:
    cal_name = cal.get_properties().get('{DAV:}displayname', '')
    
    events = cal.search(
        start=datetime(2026, 5, 1),
        end=datetime(2026, 12, 31),
        expand=True
    )
    
    for event in events:
        comp = event.icalendar_component
        summary = str(comp.get("SUMMARY", "")).strip()
        summary_normalized = unicodedata.normalize('NFD', summary.lower()).encode('ascii', 'ignore').decode()
        
        if summary_normalized == "reuniao semanal":
            found = True
            dtstart = comp.get("DTSTART").dt
            print(f"Encontrado em {gmail_user}:")
            print(f"  Calendario: {cal_name}")
            print(f"  Data: {dtstart}\n")

if not found:
    print(f"Nenhum 'Reuniao semanal' em {gmail_user}")
