# File Transfere Lab with Threads

This labs uses -p /fileName/ 
to pass a file to the server.

I used 'threading' to create a 'lock' that locks the file upload. If some other thread tries to upload the same file, it will wait until the lock is release and if the file was successfuly transfere to the server it will say that the file is already in server.
