import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

dias = [
    "2026-06-04",
    "2026-06-11", 
    "2026-06-18",
    "2026-06-25"
]

print("Verificando dias da semana de 'Psicóloga Maurício':\n")

for data_str in dias:
    dt = datetime.strptime(data_str, "%Y-%m-%d")
    dia_semana = dt.strftime("%A")
    
    # Traduzir para português
    dias_pt = {
        'Monday': 'segunda',
        'Tuesday': 'terça',
        'Wednesday': 'quarta',
        'Thursday': 'quinta',
        'Friday': 'sexta',
        'Saturday': 'sábado',
        'Sunday': 'domingo'
    }
    
    dia_pt = dias_pt.get(dia_semana, dia_semana)
    print(f"  {data_str} → {dia_pt.upper()}")
