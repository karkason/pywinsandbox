import yattag


def _get_boolean_text(value):
    return 'Default' if value else 'Disabled'


def _format_folder_mappers(folder_mappers, tag, text):
    with tag('MappedFolders'):
        for folder_mapper in folder_mappers:
            with tag('MappedFolder'):
                with tag('HostFolder'):
                    text(str(folder_mapper.path()))
                with tag('ReadOnly'):
                    text(str(folder_mapper.read_only()).lower())


def generate_config_file(config):
    config.folder_mappers = list(filter(lambda m: m.path().exists(), config.folder_mappers))

    document, tag, text = yattag.Doc().tagtext()

    with tag('Configuration'):
        with tag('VGpu'):
            text(_get_boolean_text(config.virtual_gpu))

        with tag('Networking'):
            text(_get_boolean_text(config.networking))

        with tag('LogonCommand'):
            with tag('Command'):
                text(config.logon_script)

        with tag('MemoryInMB'):
            text(config.memory_mb)

        _format_folder_mappers(config.folder_mappers, tag, text)

    return yattag.indent(document.getvalue())
