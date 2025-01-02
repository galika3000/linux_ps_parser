import subprocess
from datetime import datetime

com = ['ps', 'aux']
process = subprocess.run(com, stdout=subprocess.PIPE, text=True)

lines = process.stdout.splitlines()
users = set()
pids = set()
mem = 0
cpu = 0
max_mem = []
max_cpu = []
for line in lines[1:]:
    parts = line.split()
    if len(parts)>1:
        users.add(parts[0])
        pids.add(parts[1])
        cpu+=float(parts[2])
        mem+=float(parts[3])
        max_mem.append((parts[3], parts[10]))
        max_cpu.append((parts[2], parts[10]))
mem_sorted = sorted(max_mem, key=lambda k: k[0], reverse=True)
cpu_sorted = sorted(max_cpu, key=lambda k: k[0], reverse=True)

# Просто на баше я бы написала
# ps h -eo command --sort=-%mem | head -n 1
# но раз в задании сказано, что надо на питоне, то пишем на питоне

print("Отчет о состоянии системы:")
print("Пользователи системы:  ", users)
print("Процесов запущено:  ", len(pids))
print('\n')

print("Пользовательских процессов:")
user_proc = []
for user in users:
    comm = ['ps', '-fU', user]
    process = subprocess.run(comm, stdout=subprocess.PIPE, text=True)
    lines = process.stdout.splitlines()
    users_count = 0
    for line in lines[1:]:
        users_count+=1
    user_proc.append((user, users_count))    
    print(user, ":", users_count)

print ("Всего памяти используется:  ", mem, "%")
print ("Всего CPU используется:  ", cpu, "%")
print ("Больше всего памяти использует:  ", mem_sorted[0][1] [:20])
print ("Больше всего cpu использует:  ", cpu_sorted[0][1] [:20])

filename = datetime.now().strftime("%d-%m-%Y-%H:%M-scan.txt")

with open(filename, 'w') as file: 
    print("Отчет о состоянии системы:", file=file)
    print("Пользователи системы:  ", users, file=file)
    print("Процесов запущено:  ", len(pids), file=file)
    print('\n', file=file)
    print("Пользовательских процессов:", file=file)  
    for x in user_proc:
        print(x[0], ': ', x[1], file=file)
    print('\n')
    print ("Всего памяти используется:  ", mem, "%", file=file)
    print ("Всего CPU используется:  ", cpu, "%", file=file)
    print ("Больше всего памяти использует:  ", mem_sorted[0][1] [:20],  file=file)
    print ("Больше всего cpu использует:  ", cpu_sorted[0][1] [:20], file=file)
