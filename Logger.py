import logging


def StartLogging(context: str) -> logging.Logger:
    # set up logging to file
    logging.basicConfig(
        filename=f"{context}.log",
        level=logging.DEBUG,
        format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
        filemode="w",
    )
    logger = logging.getLogger(context)
    return logger
