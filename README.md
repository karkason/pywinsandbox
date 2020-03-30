# PyWinSandbox
Python [Windows Sandbox](https://techcommunity.microsoft.com/t5/windows-kernel-internals/windows-sandbox/ba-p/301849) library.
Create a new Windows Sandbox machine, control it with a simple RPyC interface.

A good usage for this library would be to easily run sandboxed tests in a controlled envionment.

Quick Start
------------

PyWinSandbox can be installed using pip:

```sh
$ python3 -m pip install -U pywinsandbox
```

If you want to run the latest version of the code, you can install from git:

```sh
$ python3 -m pip install -U git+git://github.com/karkason/pywinsandbox.git
```

Note that the Windows Sandbox should be enabled in your system in order to use PyWinSandbox. [See the following Microsoft article on how to do that.](https://techcommunity.microsoft.com/t5/windows-kernel-internals/windows-sandbox/ba-p/301849)

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

Also a console script is available:

```sh
# wsb / winsandbox are aliases

# Create an interactive sandbox session. Spawns an IPython shell.
wsb -i

# Spawn an "offline" Windows Sandbox instance, with a command line.
wsb -s "explorer C:\windows\system32" 
```

A shell extension is available to easily sandbox executables with the right click menu:
```sh
# Run these commands with Administrator privileges

# Register the shell extension
wsb -r
# Unregister the shell extension
wsb -u
```