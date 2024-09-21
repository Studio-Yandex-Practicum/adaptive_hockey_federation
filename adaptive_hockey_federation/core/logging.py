import logging


def configure_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(level=level,
                        datefmt="%Y-%m-%d %H:%M:%S",
                        format="[%(asctime)s.%(msecs)03d] %(funcName)20s"
                        "%(module)s:%(lineno)d %(levelname)-8s - %(message)s",
                        )
