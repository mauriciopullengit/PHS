import sys
import unicodedata
from datetime import datetime, timedelta
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

# Buscar eventos de 02/06 em diante (6 meses)
start = datetime(2026, 6, 2, 0, 0, 0)
end = datetime(2026, 12, 31, 23, 59, 59)

events = familia_cal.search(
    start=start,
    end=end,
    expand=True
)

print(f"Buscando 'Natacao Amora' de 02/06 a 31/12/2026...\n")

deleted_list = []
for event in events:
    comp = event.icalendar_component
    summary = str(comp.get("SUMMARY", "")).strip()
    dtstart = comp.get("DTSTART")
    
    summary_normalized = unicodedata.normalize('NFD', summary).encode('ascii', 'ignore').decode()
    
    if "Natacao" in summary_normalized and "Amora" in summary_normalized:
        date_str = str(dtstart.dt)
        
        try:
            event.delete()
            deleted_list.append(date_str)
            print(f"  ✅ {date_str}")
        except Exception as e:
            print(f"  ❌ {date_str}: {e}")

print(f"\n\nResultado Final:")
print(f"  Total deletado: {len(deleted_list)} ocorrencia(s)")
if deleted_list:
    print(f"  Datas: {', '.join(deleted_list[:5])}")
    if len(deleted_list) > 5:
        print(f"         ... e mais {len(deleted_list) - 5}")
