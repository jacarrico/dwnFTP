import ftplib
import os
from datetime import datetime
import sys

try:
	target_bug = sys.argv[1]
	target_dir = sys.argv[2]
	file_type = sys.argv[3]
except IndexError:
	print "Usage: dwnFTP.py <target bacteria> <local target dir> <file type> "
	print "Syncs from ftp://ftp.ncbi.nlm.nih.gov/genomes/Bacteria/ to <local target dir> all the files that match <target bacteria>, maintaining directory structure"
	print "jcarrico@fm.ul.pt - 11/09/2014"
	raise SystemExit

def DownloadAndSetTimestamp(local_file,fi,nt):
	lf=open(local_file,'wb')
	f.retrbinary("RETR " + fi, lf.write, 8*1024)
	lf.close()
	print fi + " downloaded!"

	#set the modification time the same as server for future comparison
	os.utime(local_file,( int(nt) , int(nt) ))

print "Connecting to ftp.ncbi.nih.gov..."	
f=ftplib.FTP('ftp.ncbi.nih.gov')
f.login()
f.cwd('/genomes/Bacteria/')
listing=[]
dirs=f.nlst();
print "Connected and Dir list retrieved."

print "Searching for :"+ target_bug
ct=0;
file_type = '*.ffn'
for item in dirs:
	if item.find(target_bug)>-1:
		print item
		#create the dir
		if not os.path.isdir(os.path.join(target_dir,item)):
			print "Dir not found. Creating it..."
			os.makedirs(os.path.join(Target_dir,item))
		#Get the gbk 
		#1) change the dir
		f.cwd(item)
		#2) get *.gbk files in dir
		files=f.nlst(file_type)
		for fi in files:
			print "----------------------------------------------"
			local_file = os.path.join(target_dir,item,fi)
			if os.path.isfile(local_file):
				print "################"
				print "File " + local_file + " already exists."
				#get remote modification time			
				mt = f.sendcmd('MDTM '+ fi)
				#converting to timestamp
				nt = datetime.strptime(mt[4:], "%Y%m%d%H%M%S").strftime("%s")

				if int(nt)==int(os.stat(local_file).st_mtime):
					print fi +" not modified. Download skipped"
				else:
					print "New version of "+fi
					ct+=1
					DownloadAndSetTimestamp(local_file,fi,nt)
					print "NV Local M timestamp : " + str(os.stat(local_file).st_mtime)
					print "NV Local A timestamp : " + str(os.stat(local_file).st_atime)
				print "################"

			else:
				print "################"
				print "New file: "+fi
				ct+=1
				mt = f.sendcmd('MDTM '+ fi)
				#converting to timestamp
				nt = datetime.strptime(mt[4:], "%Y%m%d%H%M%S").strftime("%s")
				DownloadAndSetTimestamp(local_file,fi,nt)
				print "################"

		f.cwd('..')
f.quit()
print "# of "+target_bug+" new files found and downloaded: " + str(ct)






