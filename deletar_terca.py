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

# Buscar de 02/06 a 31/12/2026
start = datetime(2026, 6, 2, 0, 0, 0)
end = datetime(2026, 12, 31, 23, 59, 59)

events = familia_cal.search(start=start, end=end, expand=True)

print(f"Buscando 'Natacao Amora' terças (18:45)...\n")

deleted_terca = 0
for event in events:
    comp = event.icalendar_component
    summary = str(comp.get("SUMMARY", "")).strip()
    dtstart = comp.get("DTSTART")
    
    summary_normalized = unicodedata.normalize('NFD', summary).encode('ascii', 'ignore').decode()
    
    if "Natacao" in summary_normalized and "Amora" in summary_normalized:
        dt = dtstart.dt
        time_str = str(dt)
        
        # Procurar por 18:45 (terças)
        if "18:45" in time_str:
            try:
                event.delete()
                print(f"  ✅ {time_str}")
                deleted_terca += 1
            except Exception as e:
                print(f"  ❌ {time_str}: {e}")

print(f"\nTotal deletado (terças): {deleted_terca}")
