import sys
import unicodedata
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

print(f"Buscando 'Psicologa' em todos os calendarios (mai-dez 2026)...\n")

found = []
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
        
        summary_lower = unicodedata.normalize('NFD', summary.lower()).encode('ascii', 'ignore').decode()
        
        if "psicologa" in summary_lower or "psicolog" in summary_lower:
            found.append({
                'summary': summary,
                'cal': cal_name,
                'dtstart': comp.get("DTSTART").dt
            })

if found:
    print(f"Encontrado(s) {len(found)} evento(s):\n")
    for evt in found:
        print(f"  • {evt['summary']}")
        print(f"    Calendario: {evt['cal']}")
        print(f"    Data: {evt['dtstart']}\n")
else:
    print("Nenhum evento com 'Psicologa' encontrado.")
    print("\nTente especificar o nome exato ou verificar em qual calendario esta.")
