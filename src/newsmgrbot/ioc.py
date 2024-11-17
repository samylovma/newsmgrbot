import dishka

from newsmgrbot.config import Config


class MainProvider(dishka.Provider):
    def __init__(self, config: Config) -> None:
        super().__init__()
        self.__config: Config = config
