import logging


def setup_logger():
    loggers = logging.getLogger(__name__)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S',
                        filename='log_file.log',
                        level=logging.INFO)
    return loggers


logger = setup_logger()
