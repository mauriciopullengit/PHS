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

print(f"Buscando 'Psicóloga Maurício' em todos os calendarios...\n")

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
        dtstart = comp.get("DTSTART")
        rrule = comp.get("RRULE")
        
        # Busca flexível (com ou sem acentos)
        if ("psicóloga" in summary.lower() or "psicologa" in summary.lower()) and \
           ("maurício" in summary.lower() or "mauricio" in summary.lower()):
            found.append({
                'summary': summary,
                'cal': cal_name,
                'dtstart': dtstart.dt,
                'rrule': bool(rrule),
                'event': event
            })

if found:
    print(f"Encontrado(s) {len(found)} evento(s):\n")
    for evt in found:
        print(f"  • {evt['summary']}")
        print(f"    Calendario: {evt['cal']}")
        print(f"    Data: {evt['dtstart']}")
        print(f"    Recorrente: {'SIM' if evt['rrule'] else 'NAO'}\n")
else:
    print("Nenhum evento encontrado.")
    print("\nListando TODOS os eventos de junho para referencia:\n")
    
    for cal in calendars:
        cal_name = cal.get_properties().get('{DAV:}displayname', '')
        events = cal.search(start=datetime(2026, 6, 1), end=datetime(2026, 6, 30), expand=True)
        
        if events:
            print(f"[{cal_name}]")
            for event in events:
                comp = event.icalendar_component
                summary = str(comp.get("SUMMARY", "")).strip()
                print(f"  • {summary}")
            print()
