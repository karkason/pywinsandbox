import yattag


def _get_boolean_text(value):
    return 'Default' if value else 'Disabled'


def _format_folder_mappers(folder_mappers, tag, text):
    with tag('MappedFolders'):
        for folder_mapper in folder_mappers:
            with tag('MappedFolder'):
                with tag('HostFolder'):
                    text(str(folder_mapper.path().resolve()))
                with tag('ReadOnly'):
                    text(str(folder_mapper.read_only()).lower())


def generate_config_file(vgpu_enabled, networking_enabled, folder_mappers, logon_command):
    document, tag, text = yattag.Doc().tagtext()

    with tag('Configuration'):
        with tag('VGpu'):
            text(_get_boolean_text(vgpu_enabled))

        with tag('Networking'):
            text(_get_boolean_text(networking_enabled))

        with tag('LogonCommand'):
            with tag('Command'):
                text(logon_command)

        _format_folder_mappers(folder_mappers, tag, text)

    return yattag.indent(document.getvalue())
