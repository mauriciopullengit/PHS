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

deleted_count = 0
for cal in calendars:
    events = cal.search(
        start=datetime(2026, 6, 1),
        end=datetime(2026, 6, 30),
        expand=True
    )
    
    for event in events:
        comp = event.icalendar_component
        summary = str(comp.get("SUMMARY", "")).strip()
        summary_normalized = unicodedata.normalize('NFD', summary.lower()).encode('ascii', 'ignore').decode()
        
        if summary_normalized == "reuniao semanal":
            dtstart = comp.get("DTSTART").dt
            try:
                event.delete()
                print(f"  Deletado: {summary} ({dtstart})")
                deleted_count += 1
            except Exception as e:
                print(f"  Erro: {e}")

print(f"\nTotal deletado: {deleted_count} ocorrencia(s) de 'Reuniao semanal'")
