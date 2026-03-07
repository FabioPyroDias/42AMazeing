from parser import read_config_file
from errors import InvalidParameterError, InvalidConfigurationError
from errors import InvalidValueError


if __name__ == "__main__":
    try:
        configs = read_config_file("config.txt")
        print(configs)
    except FileNotFoundError:
        print("File not found")
    except SyntaxError:
        print("TODO: Nao sei o que isto faz")
    except InvalidParameterError as error:
        print(error)
    except InvalidConfigurationError as error:
        print(error)
    except InvalidValueError as error:
        print(error)
