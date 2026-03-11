from maze_config import MazeConfig
from errors import InvalidParameterError, InvalidConfigurationError
from errors import InvalidValueError


SIZE_LIMITS = (3, 200)

def parser_integer(key: str, argument: str) -> int:
    try:
        value = argument.split("#")
        if len(value[0]) == 0:
            raise InvalidValueError(f"Value Error: {key} needs to have value")
        value = int(value[0])
        return value
    except ValueError:
        raise InvalidValueError(f"Value Error: {key} expected integer")


def parser_vector2(key: str, argument: str):
    try:
        values = argument.split("#")
        values = values[0].split(",")
        if len(values) != 2:
            raise InvalidValueError(f"Value Error: {key} expected two "
                                    f"integers split by \',\'")
        return (int(values[0]), int(values[1]))
    except ValueError:
        raise InvalidValueError(f"Value Error: {key} expected two integers "
                                f"split by \',\'")


def parser_string(key: str, argument: str):
    if not argument:
        raise InvalidValueError(f"Value Error: {key} expected argument")
    return argument


def parser_boolean(key: str, argument: str):
    value = argument.split("#")
    value = value[0].strip()
    if not (value == "True" or value == "False"):
        raise InvalidValueError(f"Value Error: {key} expected bool")
    return value == "True"


def parser_algorithm(key: str, argument: str):
    if not (argument == "Prim" or argument == "Kruskal"):
        raise InvalidValueError(f"Value Error: {key} expected TODO TODO TODO TODO")
    return argument


def parser_display(key: str, argument: str):
    if not (argument == "ASCII" or argument == "Graphical"):
        raise InvalidValueError(f"Value Error: {key} expected TODO TODO TODO TODO")
    return argument


CONFIG_KEYS = {
    "WIDTH": parser_integer,
    "HEIGHT": parser_integer,
    "ENTRY": parser_vector2,
    "EXIT": parser_vector2,
    "OUTPUT_FILE": parser_string,
    "PERFECT": parser_boolean,
    "SEED": parser_integer,
    "ALGORITHM": parser_algorithm,
    "DISPLAY": parser_display,
}

REQUIRED_KEYS = {
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT"
}


def validate_configs(configs: dict):
    width = configs["WIDTH"]
    if width < SIZE_LIMITS[0]:
        raise InvalidValueError(f"Value Error: WIDTH must be at least "
                                f"{SIZE_LIMITS[0]}")
    if width > SIZE_LIMITS[1]:
        raise InvalidValueError(f"Value Error: WIDTH must be at most "
                                f"{SIZE_LIMITS[1]}")
    height = configs["HEIGHT"]
    if height < SIZE_LIMITS[0]:
        raise InvalidValueError(f"Value Error: HEIGHT must be at least "
                                f"{SIZE_LIMITS[0]}")
    if height > SIZE_LIMITS[1]:
        raise InvalidValueError(f"Value Error: HEIGHT must be at most "
                                f"{SIZE_LIMITS[1]}")
    entry_point_coord_x, entry_point_coord_y = configs["ENTRY"]
    if ((entry_point_coord_x < 0 or entry_point_coord_x >= width) or
        (entry_point_coord_y < 0 or entry_point_coord_y >= height)):
        raise InvalidValueError(f"Value Error: ENTRY coordinates must be "
                                f"within 0 and {width - 1} for x and "
                                f"within 0 and {height - 1} for y")
    exit_point_coord_x, exit_point_coord_y = configs["EXIT"]
    if ((exit_point_coord_x < 0 or exit_point_coord_x >= width) or
        (exit_point_coord_y < 0 or exit_point_coord_y >= height) or
        (entry_point_coord_x == exit_point_coord_x and
        entry_point_coord_y == exit_point_coord_y)):
        raise InvalidValueError(f"Value Error: EXIT coordinates must be "
                                f"within 0 and {width - 1} for x and "
                                f"within 0 and {height - 1} for y")
    seed = configs.get("SEED", None)
    if seed is None:
        configs["SEED"] = 42
    else:
        if seed < 0 or seed > 4294967295:
            raise InvalidValueError("Value Error: SEED must be within 0 "
                                    "and 4294967295")


def read_config_file(path: str) -> dict:
    configs = {}
    with open(path, 'r') as config:
        for line in config:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            arguments = line.split("=", 1)
            if len(arguments) != 2:
                raise InvalidConfigurationError("Configuration "
                                                "Error: expected "
                                                "'Key=Value'")
            if arguments[0].strip() not in CONFIG_KEYS:
                raise InvalidParameterError(f"Parameter Error: "
                                            f"{arguments[0].strip()} "
                                            f"is invalid")
            parsed_value = CONFIG_KEYS[arguments[0].strip()](
                (arguments[0].strip()), arguments[1].strip())
            if arguments[0].strip() in configs:
                raise InvalidConfigurationError(f"Configuration Error: "
                                                f"duplicated "
                                                f"{arguments[0].strip()} "
                                                f"parameter")
            configs[arguments[0].strip()] = parsed_value
        config.close()
    required_key_counter = 0
    for key in REQUIRED_KEYS:
        for config in configs:
            if key == config:
                required_key_counter += 1
    if required_key_counter != len(REQUIRED_KEYS):
        raise InvalidConfigurationError("Configuration Error: "
                                        "missing required keys")
    validate_configs(configs)
    return MazeConfig(configs)
