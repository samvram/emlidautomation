import base64
import paramiko
import cmd

class nettrans:
    """
       Nettrans is to get files via ftp operation over ssh protocol
       While creation you need to specify IP, Username and Password 
       of the client from whom you want the files.
       
       example use:
             nettrans sam('192.168.3.145','root','emlidreach')
          
       Various modes of operation:
       Mode latest - Fetch the latest RAW file with .UBX extension
       Mode all - Fetch all the files present in ~/logs folder
       Mode raws - Fetch all the RAW files in the ~/logs folder

       example use:
             nettrans sam('192.168.3.145','root','emlidreach')
             sam.create_connection( )
             sam.mode_select('all')

       The file transfer occurs once we implement the above
       
       example use:
             sam.get_file( )

       You must close all connections made during the operation

       example use:
             sam.close_connection( )
       
       More modes to come soon

    """
       
    def __init__(ip,username,password):
        self.ip=ip
        self.uname=username
        self.pw=password
        self.mode=0

    def mode_select(self, x):
        self.mode=x

    def create_connection(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=uname, password=pw)
        ftp=client.open_sftp( )

    def get_file(self):
        sam=[];
        raw=[];
        dt=[];
        
        stdin, stdout, stderr = client.exec_command('ls logs')
        for line in stdout:
            print('>>> ' + line.strip('\n'))
            sam.append(line.strip('\n'))

        if(mode=='latest'):
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
            ftp.get(latestfile,resultfile)

        if(mode=='all'):
            for i in range(0,len(sam)):
                fetchfile='logs/'+sam[i]
                resultfile=sam[i]
                ftp.get(sam[i],resultfile)

        if(mode=='raws'):
            for i in range(0,len(sam)):
                print(sam[i])
                if(sam[i][0:3] == 'raw'):
                    raw.append(sam[i])

            for i in range(0,len(raw)):
                fetchfile='logs/'+raw[i]
                resultfile=raw[i]
                ftp.get(raw[i],resultfile)


    def close_connection(self):
        client.close( )
        ftp.close( )

            
            
               
