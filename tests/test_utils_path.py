from winsandbox.utils.path import shared_folder_path_in_sandbox, WINDOWS_SANDBOX_DEFAULT_DESKTOP


def test_shared_folder_path_in_sandbox():
    assert shared_folder_path_in_sandbox(r"C:\test.txt") == WINDOWS_SANDBOX_DEFAULT_DESKTOP / "test.txt"
    assert shared_folder_path_in_sandbox(r"D:\test.txt") == WINDOWS_SANDBOX_DEFAULT_DESKTOP / "test.txt"
    assert shared_folder_path_in_sandbox(r"test.txt") == WINDOWS_SANDBOX_DEFAULT_DESKTOP / "test.txt"
    assert shared_folder_path_in_sandbox(r"C:\some\test.txt") == WINDOWS_SANDBOX_DEFAULT_DESKTOP / "test.txt"
    assert shared_folder_path_in_sandbox(r"C:\some\random\path\test.txt") == WINDOWS_SANDBOX_DEFAULT_DESKTOP / "test.txt"
