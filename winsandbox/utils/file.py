import os
import time


def wait_for_file_creation(filename, timeout=25, check_interval=1):
    """
    Return true if filename exists, if not keep checking once every check_interval seconds for time_limit seconds.
    """

    if timeout < 1:
        timeout = 1

    now = time.time()
    timeout_time = now + timeout

    while time.time() <= timeout_time:
        if os.path.exists(filename):
            return True
        else:
            # Wait for check interval seconds, then check again.
            time.sleep(check_interval)

    return False
