
# Usage 

`dwnFTP.py <target bacteria> <local target dir> <file type>`

# Description 

Syncronizes from ftp://ftp.ncbi.nlm.nih.gov/genomes/Bacteria/ to *Local target directory* all the files of *file type* that match *target bacteria*, maintaining directory structure

# Example of usage

`dwnFTP.py "Streptococcus_agalactiae" "GBS" "*.faa"``

Downloads all the *faa* files from *Streptococcus agalactiae* to the *GBS* directory
Running the script again with the same parameters updates any files that changed and adds novel genomes. 
