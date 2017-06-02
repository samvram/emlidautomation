#!c:/Python/python.exe -u

# This block of code gets the latest file and stores it in the location the script runs in



import base64
import paramiko
import cmd

# Creating a SSH client named 'client'
# The method is to bypass RSA SSH DNA key so the 2nd line does Auto Add
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())   

# The IP is to be set a proper static one, the given username and password are present for SSHing
client.connect('192.168.3.145', username='root', password='emlidreach')

#Initialization of lists that are essential for finding the latest file
sam=[];
raw=[];
dt=[];



# We get file list of logs, print it as well as store it in the list sam
stdin, stdout, stderr = client.exec_command('ls logs')
for line in stdout:
    print('>>> ' + line.strip('\n'))
    sam.append(line.strip('\n'))


# We filter to get the name of all raw files from sam and print all file names
print('sam is:')
for i in range(0,len(sam)):
    print(sam[i])
    if(sam[i][0:3] == 'raw'):
        raw.append(sam[i])

# We print all the raw files and get the date and time part of the filename and add them to date list
print('\n The raw files are')
for i in range(0,len(raw)):
    print(raw[i])
    dt.append(raw[i][4:-4])

# dt is a string list and we make it integer while printing them
print('\n The dates are')
for i in range(0,len(dt)):
    dt[i]=int(dt[i])
    print(dt[i])

# We find the latest date as it is the largest value present
for i in range(0,len(dt)):
    if(max(dt)==dt[i]):
        latestfile=raw[i]

# Printing the name of the latest file
print('\nThe latest file is ',latestfile)
resultfile = latestfile

# Appending the complete address to get the files from
latestfile = 'logs/'+latestfile

#FTP Standard protocol commands to make file transfer
ftp = client.open_sftp()
ftp.get(latestfile,resultfile)
ftp.close()

print('\nThe result file has been saved\n')

client.close()
