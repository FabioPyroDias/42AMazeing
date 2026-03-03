from parser import read_config_file
from errors import InvalidParameterError, InvalidConfigurationError


if __name__ == "__main__":
    try:
        read_config_file("test.txt")
    except FileNotFoundError:
        print(f"File not found")
    except SyntaxError:
        print("TODO: Nao sei o que isto faz")
    except InvalidParameterError as error:
        print(error)
    except InvalidConfigurationError as error:
        print(error)
