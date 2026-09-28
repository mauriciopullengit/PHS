import sys
from datetime import datetime, timedelta
from caldav import DAVClient

sys.stdout.reconfigure(encoding='utf-8')

# Carregar credenciais
env_file = r"C:\Users\mau\.config\hook\gmail.env"
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
print(f"Eventos em {gmail_user} (semana que vem em diante):\n")

# Data inicio (semana que vem, segunda-feira)
today = datetime.now()
days_until_monday = (7 - today.weekday()) % 7
if days_until_monday == 0:
    days_until_monday = 0
start_date = today + timedelta(days=days_until_monday)

for cal in calendars:
    cal_name = cal.get_properties().get('{DAV:}displayname', 'Sem nome')
    
    # Buscar eventos
    events = cal.search(
        start=start_date,
        end=start_date + timedelta(days=30),
        expand=True
    )
    
    if events:
        print(f"  Calendario: {cal_name}")
        for event in events:
            comp = event.icalendar_component
            summary = comp.get("SUMMARY", "").strip()
            dtstart = comp.get("DTSTART")
            dtend = comp.get("DTEND")
            location = comp.get("LOCATION", "[sem local]")
            
            print(f"    • {summary}")
            print(f"      {dtstart.dt} -> {dtend.dt}")
            print(f"      Local: {location}\n")
