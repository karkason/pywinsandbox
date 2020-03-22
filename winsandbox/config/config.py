from recordclass import recordclass

SandboxConfig = recordclass("SandboxConfig", ['folder_mappers', 'networking', 'logon_script', 'virtual_gpu'])
