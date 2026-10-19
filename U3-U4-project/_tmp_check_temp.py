import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('192.168.1.196', username='lapland_dog00', password='12345', timeout=10)

cmds = [
    "vcgencmd measure_temp",
    "vcgencmd get_throttled",
    "uptime",
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
