# PyWinSandbox
Python [Windows Sandbox](https://techcommunity.microsoft.com/t5/windows-kernel-internals/windows-sandbox/ba-p/301849) library.
Create a new Windows Sandbox machine, control it with a simple RPyC interface.

Examples
-------

```python
import winsandbox

sandbox = winsandbox.new_sandbox()
sandbox.rpyc.modules.subprocess.run('explorer .')

# Create a sandbox with a mapped directory.
# Directories are mapped under desktop.
sandbox = winsandbox.new_sandbox(folder_mappers=[winsandbox.FolderMapper(r'C:\users\public')])
tree = sandbox.rpyc.modules.subprocess.check_output(r'cmd /c tree %userprofile%\Desktop\public')

# Create an offline sandbox with a logon script.
sandbox = winsandbox.new_sandbox(networking=False, logon_script="explorer .")
```
