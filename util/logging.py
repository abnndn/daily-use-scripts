import logging.handlers

def setup_logger(name=__name__):
    """Set up and return a logger with rotating file handler."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Check if logger already has handlers to avoid duplication
    if not logger.handlers:
        logger_file_handler = logging.handlers.RotatingFileHandler(
            "weekly-report.log",
            maxBytes=1024 * 1024,
            backupCount=1,
            encoding="utf8",
        )
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        logger_file_handler.setFormatter(formatter)
        logger.addHandler(logger_file_handler)
    
    return logger
