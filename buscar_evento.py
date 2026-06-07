import sys
from datetime import datetime, timedelta
from caldav import DAVClient

sys.stdout.reconfigure(encoding='utf-8')

# Carregar credenciais
env_file = r"C:\Users\mauri\.config\hook\gmail.env"
gmail_user, gmail_pass = None, None

with open(env_file, encoding='utf-8') as f:
    for line in f:
        if line.startswith("GMAIL_USER"):
            gmail_user = line.split("=", 1)[1].strip()
        elif line.startswith("GMAIL_APP_PASSWORD"):
            gmail_pass = line.split("=", 1)[1].strip()

# Conectar ao CalDAV
url = f"https://www.google.com/calendar/dav/{gmail_user}/"
client = DAVClient(url=url, username=gmail_user, password=gmail_pass)
principal = client.principal()

# Listar calendários
calendars = principal.calendars()
print(f"Calendarios encontrados: {len(calendars)}\n")

for cal in calendars:
    cal_name = cal.get_properties().get('{DAV:}displayname', 'Sem nome')
    print(f"Procurando em: {cal_name}")
    
    # Buscar eventos
    events = cal.search(
        start=datetime.now(),
        end=datetime.now() + timedelta(days=90),
        expand=True
    )
    
    found = False
    for event in events:
        comp = event.icalendar_component
        summary = comp.get("SUMMARY", "").strip()
        
        if "natacao" in summary.lower() and "amora" in summary.lower():
            found = True
            dtstart = comp.get("DTSTART")
            dtend = comp.get("DTEND")
            location = comp.get("LOCATION", "[sem local]")
            rrule = comp.get("RRULE")
            
            print(f"  Encontrado: {summary}")
            print(f"    Data/Hora: {dtstart.dt} -> {dtend.dt}")
            print(f"    Local: {location}")
            print(f"    Recorrencia: {'SIM' if rrule else 'NAO'}\n")

if not found:
    print("Nenhum evento com 'Natacao Amora' encontrado.")
