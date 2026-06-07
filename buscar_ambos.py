import sys
from datetime import datetime
from caldav import DAVClient

sys.stdout.reconfigure(encoding='utf-8')

# Buscar em maurinata19@gmail.com (conta 2)
env_file = r"C:\Users\mauri\.config\hook\gmail2.env"
gmail_user, gmail_pass = None, None

with open(env_file, encoding='utf-8') as f:
    for line in f:
        if line.startswith("GMAIL_USER"):
            gmail_user = line.split("=", 1)[1].strip()
        elif line.startswith("GMAIL_APP_PASSWORD"):
            gmail_pass = line.split("=", 1)[1].strip()

print(f"Buscando em {gmail_user}...\n")

url = f"https://www.google.com/calendar/dav/{gmail_user}/"
client = DAVClient(url=url, username=gmail_user, password=gmail_pass)
principal = client.principal()

calendars = principal.calendars()

found_psicologa = False
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
        
        if ("psicóloga" in summary.lower() or "psicologa" in summary.lower()) and \
           ("maurício" in summary.lower() or "mauricio" in summary.lower()):
            found_psicologa = True
            print(f"Encontrado: {summary}")
            print(f"  Calendario: {cal_name}")
            print(f"  Data: {dtstart.dt}")
            print(f"  Recorrente: {'SIM' if rrule else 'NAO'}")

if not found_psicologa:
    print("Evento 'Psicóloga Maurício' não encontrado em maurinata19@gmail.com")
    print("\nTodos os eventos em maurinata19@gmail.com (jun 2026):\n")
    
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
