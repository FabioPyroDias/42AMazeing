class MazeConfig:
    def __init__(self, config: dict) -> None:
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.output = config["OUTPUT_FILE"]
        self.perfect = config["PERFECT"]
        self.seed = config["SEED"]
        self.algorithm = config.get("ALGORITHM", "Prim")
        self.display = config.get("DISPLAY", "ASCII")

    def __str__(self) -> str:
        return f"Maze {self.width}x{self.height} | Seed: {self.seed}\n"\
               f"Entry: {self.entry} | Exit: {self.exit}\n"\
               f"Perfect: {self.perfect}\n"\
               f"Seed: {self.seed}\n"\
               f"Algorithm: {self.algorithm}\n"\
               f"Display: {self.display}"