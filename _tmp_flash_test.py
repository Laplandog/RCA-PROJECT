import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('192.168.1.196', username='lapland_dog00', password='12345', timeout=15)

sketch = '''void setup() {
  Serial.begin(115200);
}

int counter = 0;

void loop() {
  Serial.print("hello from arduino, count=");
  Serial.println(counter);
  counter++;
  delay(1000);
}
'''

sftp = client.open_sftp()
try:
    sftp.mkdir('/home/lapland_dog00/serial_test')
except IOError:
    pass
with sftp.file('/home/lapland_dog00/serial_test/serial_test.ino', 'w') as f:
    f.write(sketch)
sftp.close()

cmd = (
    "cd /home/lapland_dog00 && "
    "./bin/arduino-cli compile --fqbn arduino:avr:uno serial_test && "
    "./bin/arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno serial_test"
)
stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
for line in iter(stdout.readline, ""):
    print(line, end="")
exit_status = stdout.channel.recv_exit_status()
print("EXIT_STATUS:", exit_status)
client.close()
