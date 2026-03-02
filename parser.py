from errors import InvalidParameterError, InvalidConfigurationError


def read_config_file(path: str) -> dict:
    try:
        with open(path, 'r') as config:
            pass
    except FileNotFoundError:
        print(f"File {path} not found")
    except SyntaxError:
        print("TODO: Nao sei o que isto faz")
    except InvalidParameterError:
        print("TODO")
    except InvalidConfigurationError:
        print("TODO")
    return None
