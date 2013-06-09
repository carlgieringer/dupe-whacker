# dupe-whacker

A project for discovering duplicate files using python.

I unwittingly added my iTunes library to a case-sensitive file system, 
which caused pain when I tried to copy it back to case-insensitive file
system as iTunes had created case-sensitive folders and file names.

I used find_conflicts.py to alert me to all the files whose ID3 information
needed to be updated so as not to conflict when moved to a case-insensitive
file system.

find_duplicates.py probably works, but it took too long to process my entire
library, so I'm not 100% sure.  It works by first comparing file sizes and 
then using sha1 only if file sizes match.
