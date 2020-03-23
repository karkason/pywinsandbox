from winsandbox.utils.file import wait_for_file_creation

import os
import tempfile


def test_wait_for_file_creation():
    temp_file_path = tempfile.mktemp()
    with open(temp_file_path, "w") as f:
        assert wait_for_file_creation(f.name, timeout=0, check_interval=0)

    os.remove(temp_file_path)
    assert not wait_for_file_creation(f.name, timeout=0)
