import logging, re, sys, os
from typing import Optional

import mipy_env

########## module public
def init(log_level: Optional[str]=None, log_filter: Optional[str]=None) -> tuple[str, Optional[str]]:
    if log_level:
        mipy_env.set_param("LOG_LEVEL", log_level)
    else:        
     log_level = mipy_env.get_or_ask_and_wait_for_param("LOG_LEVEL", default="info", value_type=str)
    if log_filter:
        mipy_env.set_param("LOG_LEVEL", log_level)
    else:
        log_filter = mipy_env.get_or_ask_and_wait_for_param("LOG_FILTER", default=None, value_type=str)
    _init()
    
    return log_level, log_filter
    
def create(name: str) -> logging.Logger:
    _init()
    return logging.getLogger(name)

########## module private
_initialized = False

def _init() -> tuple[str, Optional[str]]:        
    global _initialized
    if _initialized:
        return
    #log_level = mipy_env.get_or_ask_and_wait_for_param("LOG_LEVEL", default="info", value_type=str)
    #log_filter = mipy_env.get_or_ask_and_wait_for_param("LOG_FILTER", default=None, value_type=str)
    
    log_level = os.environ.get("LOG_LEVEL", "warning") 
    log_filter = os.environ.get("LOG_FILTER", None) 
    
    # Set up basic logging
    log_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)  # Set global log level

    # Create and configure a StreamHandler for console output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)

    # Add the handler to the root logger
    for handler in root_logger.handlers:
        root_logger.removeHandler( handler )
    root_logger.addHandler(console_handler)
    
    # Set up regex!
    if log_filter:
        class GlobalRegexFilter(logging.Filter):
            def __init__(self, pattern):
                super().__init__()
                self.pattern = re.compile(pattern)

            def filter(self, record):
                # Suppress log messages that match the regex
                return not self.pattern.search(record.getMessage())            
        root_logger.addFilter(GlobalRegexFilter(log_filter))
        