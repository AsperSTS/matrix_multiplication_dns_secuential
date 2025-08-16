import os
import time

pid = os.fork()

if pid > 0:
    # Parent process
    with open('.pidfile', 'w') as f:
        f.write(str(pid))
    # Sleep for a while to allow the parent process to complete
    time.sleep(5)
else:
    # Child process
    os.execlp('sleep', 'sleep', '60')  # Replace '60' with the desired sleep time
