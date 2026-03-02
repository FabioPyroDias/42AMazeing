from errors import InvalidParameterError, InvalidConfigurationError

CONFIG_KEYS = [
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT"
    "SEED",
    "ALGORITHM",
    "DISPLAY"
]

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

'''
Todos estes except vao ter de ser no main.
Aqui, neste script, so vao haver raises.
'''