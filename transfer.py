#!c:/Python/python.exe -u

import base64
import paramiko
import cmd


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


client.connect('192.168.3.145', username='root', password='emlidreach')


sam=[];
raw=[];
dt=[];
stdin, stdout, stderr = client.exec_command('ls logs')
for line in stdout:
    print('>>> ' + line.strip('\n'))
    sam.append(line.strip('\n'))


print('sam is:')
for i in range(0,len(sam)):
    print(sam[i])
    if(sam[i][0:3] == 'raw'):
        raw.append(sam[i])

print('\n The raw files are')
for i in range(0,len(raw)):
    print(raw[i])
    dt.append(raw[i][4:-4])

print('\n The dates are')
for i in range(0,len(dt)):
    dt[i]=int(dt[i])
    print(dt[i])

for i in range(0,len(dt)):
    if(max(dt)==dt[i]):
        latestfile=raw[i]

print('\nThe latest file is ',latestfile)
resultfile = latestfile
latestfile = 'logs/'+latestfile

ftp = client.open_sftp()
ftp.get(latestfile,resultfile)
ftp.close()

print('\nThe result file has been saved\n')

client.close()
