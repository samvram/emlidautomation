import base64
import paramiko
import cmd


class modeNotFound(Exception):
    pass
"""Exception for mode not being in previous list"""


class nettrans:
    """
       Nettrans is to get files via ftp operation over ssh protocol
       While creation you need to specify IP, Username and Password 
       of the client from whom you want the files.
       
       example usage ::
             nettrans object('192.168.3.145','root','emlidreach')
          
       Various modes of operation:
       Mode latest - Fetch the latest RAW file with .UBX extension
       Mode all - Fetch all the files present in ~/logs folder
       Mode raws - Fetch all the RAW files in the ~/logs folder

       example usage ::
             nettrans object('192.168.3.145','root','emlidreach')
             object.create_connection( )
             object.mode_select('all')

       The file transfer occurs once we implement the above
       
       example usage::
             object.get_file( )

       You must close all connections made during the operation

       example usage ::
             object.close_connection( )
       
       More modes to come soon

    """
    _modes = ['all','raws','latest']

    def __enter__(self):
        self.create_connection( )

    def __exit__(self):
        self.close_connection( )
       
    def __init__(ip,username,password):
        self.ip=ip
        self.uname=username
        self.pw=password
        self.mode=0

    @property
    def mode_select(self, x):
        if x in _modes:
           self.mode=x
        else
           raise modeNotFound('The mode is not listed')


    def create_connection(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=uname, password=pw)
        ftp=client.open_sftp( )

    def _latest_file_download(files):
        raw=[];
        dt=[];
        for i in range(0,len(files)):
                print(files[i])
                if(files[i][0:3] == 'raw'):
                    raw.append(files[i])
                    
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

    def _all_files_download(files):
        for i in range(0,len(files)):
                fetchfile='logs/'+files[i]
                resultfile=files[i]
                ftp.get(fetchfile,resultfile)


    def _raw_files_download(files):
        raw=[];
        for i in range(0,len(files)):
                print(files[i])
                if(files[i][0:3] == 'raw'):
                    raw.append(files[i])

            for i in range(0,len(raw)):
                fetchfile='logs/'+raw[i]
                resultfile=raw[i]
                ftp.get(fetchfile,resultfile)


    def get_file(self):
        files=[];
             
        stdin, stdout, stderr = client.exec_command('ls logs')
        for line in stdout:
            print('>>> ' + line.strip('\n'))
            files.append(line.strip('\n'))

        if(mode=='latest'):
            _latest_file_download(files)

        if(mode=='all'):
            _all_files_download(files)

        if(mode=='raws'):
            _raw_files_download(files)


    def close_connection(self):
        client.close( )
        ftp.close( )

            
            
               
