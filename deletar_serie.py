import sys
from datetime import datetime, timedelta
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
familia_cal = None

for cal in calendars:
    cal_name = cal.get_properties().get('{DAV:}displayname', '')
    if 'Fam' in cal_name:
        familia_cal = cal
        break

# Buscar com janela maior
events = familia_cal.search(
    start=datetime(2026, 5, 1),
    end=datetime(2026, 7, 1),
    expand=False
)

print(f"Total de eventos encontrados: {len(events)}\n")

deleted_count = 0
for event in events:
    comp = event.icalendar_component
    summary = comp.get("SUMMARY", "").strip()
    rrule = comp.get("RRULE")
    dtstart = comp.get("DTSTART")
    
    if "Natacao Amora" in summary and rrule:
        print(f"Encontrado evento recorrente:")
        print(f"  Titulo: {summary}")
        print(f"  Inicio: {dtstart.dt if hasattr(dtstart, 'dt') else dtstart}")
        print(f"  RRULE: {rrule}\n")
        
        # Modificar RRULE
        comp.pop("RRULE")
        comp.add("RRULE", {"FREQ": "WEEKLY", "BYDAY": "TU,TH", "UNTIL": "20260601"})
        
        event.save()
        print(f"  ✅ Modificado: agora termina em 01/06/2026\n")
        deleted_count += 1

if deleted_count > 0:
    print(f"Resultado: {deleted_count} serie(s) truncada(s)")
    print("Natacao Amora removida a partir de 02/06 (indefinidamente)")
else:
    print("Nenhuma serie recorrente encontrada")
