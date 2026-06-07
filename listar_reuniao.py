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

print(f"Buscando eventos em {gmail_user}...\n")

reuniao_events = []
psicologa_events = []

for cal in calendars:
    cal_name = cal.get_properties().get('{DAV:}displayname', '')
    
    events = cal.search(
        start=datetime(2026, 6, 1),
        end=datetime(2026, 6, 30),
        expand=True
    )
    
    for event in events:
        comp = event.icalendar_component
        summary = str(comp.get("SUMMARY", "")).strip()
        dtstart = comp.get("DTSTART")
        rrule = comp.get("RRULE")
        
        summary_lower = unicodedata.normalize('NFD', summary.lower()).encode('ascii', 'ignore').decode()
        
        if "reuniao semanal" in summary_lower:
            reuniao_events.append({
                'summary': summary,
                'dtstart': dtstart.dt,
                'rrule': bool(rrule),
                'cal': cal_name,
                'event': event
            })
        
        if "psicologa" in summary_lower and "mauricio" in summary_lower:
            psicologa_events.append({
                'summary': summary,
                'dtstart': dtstart.dt,
                'rrule': bool(rrule),
                'cal': cal_name,
                'event': event
            })

print(f"Reuniao Semanal encontrada(s): {len(reuniao_events)}")
for evt in reuniao_events:
    print(f"  • {evt['summary']}")
    print(f"    Calendario: {evt['cal']}")
    print(f"    Data: {evt['dtstart']}")
    print(f"    Recorrente: {'SIM' if evt['rrule'] else 'NAO'}\n")

print(f"Psicologa Mauricio encontrada(s): {len(psicologa_events)}")
for evt in psicologa_events:
    print(f"  • {evt['summary']}")
    print(f"    Calendario: {evt['cal']}")
    print(f"    Data: {evt['dtstart']}")
    print(f"    Recorrente: {'SIM' if evt['rrule'] else 'NAO'}\n")
