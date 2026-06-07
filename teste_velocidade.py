import sys
import time
sys.path.insert(0, r"C:\Users\mauri\OneDrive\Documents\Claude Memory\03- Claude\projetos\Rose\_agenda")

from calendar_api import CalendarAPI

sys.stdout.reconfigure(encoding='utf-8')

print("Teste de Velocidade — CalendarAPI\n")

# Conectar (1 vez)
t0 = time.time()
api = CalendarAPI(account=1)
t_connect = time.time() - t0

print(f"Tempo de conexão: {t_connect:.2f}s\n")

# Listar eventos (1 busca para múltiplos)
t0 = time.time()
events = api.list_events()
t_list = time.time() - t0

print(f"Tempo para listar {len(events)} eventos: {t_list:.2f}s")
print(f"Tempo por evento: {(t_list/len(events)*1000):.1f}ms\n")

# Comparação vs. abordagem anterior (um script por evento)
print("Comparação (teórica):")
print(f"  Abordagem anterior (script/evento): {len(events)} × 2-3s = {len(events) * 2.5:.0f}s")
print(f"  Nova abordagem (batch): {t_list:.2f}s")
print(f"  Aceleração: ~{(len(events) * 2.5) / t_list:.1f}X mais rápido\n")

# Teste de batch delete (sem deletar de verdade)
print("Simulando batch delete de 5 eventos:")
to_delete = [
    {'summary': events[0]['summary'], 'start': events[0]['start']},
]
if len(events) > 1:
    to_delete.append({'summary': events[1]['summary'], 'start': events[1]['start']})

print(f"  Eventos a deletar: {len(to_delete)}")
print(f"  (não deletando de verdade neste teste)")
