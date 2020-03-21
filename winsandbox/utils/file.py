import os
import time


def watch_file(filename, timeout=60, check_interval=1):
    """
    Return true if filename exists, if not keep checking once every check_interval seconds for time_limit seconds.
    """

    now = time.time()
    timeout_time = now + timeout

    while time.time() <= timeout_time:
        if os.path.exists(filename):
            return True
        else:
            # Wait for check interval seconds, then check again.
            time.sleep(check_interval)

    return False
