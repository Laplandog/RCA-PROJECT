import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('192.168.1.196', username='lapland_dog00', password='12345', timeout=15)

cmd = (
    "curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh && "
    "./bin/arduino-cli version && "
    "./bin/arduino-cli core update-index && "
    "./bin/arduino-cli core install arduino:avr"
)
stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
for line in iter(stdout.readline, ""):
    print(line, end="")
exit_status = stdout.channel.recv_exit_status()
print("EXIT_STATUS:", exit_status)
client.close()
