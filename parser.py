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
    with open(path, 'r') as config:
        line = "!"
        while line != "":
            line = config.readline()
            skip = False
            for character in line:
                if not (character == ' ' or character == '\t'):
                    if character == '#':
                        skip = True
                    break
            if skip:
                continue
            arguments = line.split("=")
            if len(arguments) != 2:
                raise InvalidConfigurationError("Configuration " \
                                                "Error: expected " \
                                                "'Key=Value'")
            selected_key = None
            key_index = 0
            while key_index < len(CONFIG_KEYS):
                if CONFIG_KEYS[key_index] == arguments[0]:
                    selected_key = CONFIG_KEYS[key_index]
                    break
                key_index += 1
            if not selected_key:
                raise InvalidParameterError(f"Parameter Error: " \
                                            f"{arguments[0]} is invalid")
            print(line)
    print("TODO")
    return None

'''
Todos estes except vao ter de ser no main.
Aqui, neste script, so vao haver raises.
'''