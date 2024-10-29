import logging


def setup_logging(logging_file: str):
    # Create a custom logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set the root logger to the lowest level

    # Create handlers
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)  # Set the stream handler to INFO level

    file_handler = logging.FileHandler(logging_file, mode="w")
    file_handler.setLevel(logging.DEBUG)  # Set the file handler to DEBUG level

    # Create formatters and add them to the handlers
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    # Set specific loggers to WARNING level
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Uncomment if needed
    # set_verbose(True)
    # set_debug(True)


def format_execution_time(execution_time):
    days, remainder = divmod(execution_time, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_str_parts = []
    if days > 0:
        time_str_parts.append(f"{int(days)} days")
    if hours > 0 or days > 0:
        time_str_parts.append(f"{int(hours)} hours")
    if minutes > 0 or hours > 0 or days > 0:
        time_str_parts.append(f"{int(minutes)} minutes")
    time_str_parts.append(f"{seconds:.2f} seconds")
    return "Execution time: " + " ".join(time_str_parts)
