# web_backup
Performs the following tasks:

1. Copy the backup files (web and sql dump) to the backup server.
2. Delete the old backup files.
3. Restore website based on a date.

On the production web server, (1) and (2) are performed on a periodic basis. On 
the backup web server, (2) is performed on a periodic basis, (3) is on demand.  
