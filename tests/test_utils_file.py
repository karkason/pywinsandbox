from winsandbox.utils.file import wait_for_file_creation

import tempfile


def test_wait_for_file_creation():
    with tempfile.NamedTemporaryFile() as f:
        assert wait_for_file_creation(f.name, timeout=0)

    assert not wait_for_file_creation(f.name, timeout=0, check_interval=0)
