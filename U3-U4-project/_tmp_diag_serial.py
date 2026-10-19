import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('192.168.1.196', username='lapland_dog00', password='12345', timeout=15)

cmds = [
    "groups lapland_dog00",
    "ls -l /dev/ttyUSB0",
    "systemctl is-active ModemManager 2>&1",
    "systemctl is-enabled ModemManager 2>&1",
    "fuser /dev/ttyUSB0 2>&1 || echo no_process_holding_it",
]
for c in cmds:
    stdin, stdout, stderr = client.exec_command(c)
    out = stdout.read().decode(errors='replace')
    err = stderr.read().decode(errors='replace')
    print(f"$ {c}")
    print(out)
    if err.strip():
        print("STDERR:", err)
    print("---")
client.close()
