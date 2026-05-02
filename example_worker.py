import logging


class ExampleWorker:
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger

    def run(self) -> None:
        self.logger.info("ExampleWorker is using the configured logger.")
