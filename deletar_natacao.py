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

# Buscar eventos em 02/06
events = familia_cal.search(
    start=datetime(2026, 6, 2, 0, 0, 0),
    end=datetime(2026, 6, 3, 0, 0, 0),
    expand=True
)

print(f"Processando {len(events)} evento(s) em 02/06...\n")

deleted_count = 0
for event in events:
    comp = event.icalendar_component
    summary = str(comp.get("SUMMARY", "")).strip()
    dtstart = comp.get("DTSTART")
    
    # Normalizar para comparacao (remove acentos)
    summary_normalized = unicodedata.normalize('NFD', summary).encode('ascii', 'ignore').decode()
    
    print(f"Evento: {summary} ({summary_normalized})")
    
    if "Natacao" in summary_normalized and "Amora" in summary_normalized:
        print(f"  Data/Hora: {dtstart.dt}")
        print(f"  Deletando...")
        
        try:
            event.delete()
            print(f"  ✅ Deletado!\n")
            deleted_count += 1
        except Exception as e:
            print(f"  ❌ Erro: {e}\n")

print(f"\nTotal deletado: {deleted_count} evento(s)")
