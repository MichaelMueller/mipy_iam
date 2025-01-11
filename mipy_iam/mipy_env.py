import os, aiofiles.os, asyncio
# pip
from dotenv import load_dotenv
from aiofiles import open as aio_open

# public interface

def get_or_ask_and_wait_for_param(param_name, default=None, value_type=str):    
    """
    Get a parameter from the environment. If not found, ask the user for it.
    Args:
        param_name (str): The name of the environment variable.
        default: The default value if the variable is not found.
        value_type: The expected type (str, int, bool).
    Returns:
        The value of the parameter, converted to the specified type.
    """
    global _dot_env_loaded
    if not _dot_env_loaded:
        load_dotenv()
        _dot_env_loaded = True
        
    value = os.getenv(param_name)
    if value is None:
        # Ask the user for input if not in .env
        user_input = input(f"Enter value for {param_name} (default: {default}): ") or default
        #user_input = await aioconsole.ainput(f"Enter value for {param_name} (default: {default}): ") or default
        try:
            value = value_type(user_input)
        except ValueError:
            print(f"Invalid value. Expected {value_type.__name__}.")
            exit(1)

        # Save to .env file
        with open(".env", "a") as env_file:
            env_file.write(f"{param_name}={user_input}\n")

    else:
        value = value_type(value)

    return value

def set_param(param_name, value):
    os.environ[param_name] = value

# private vars
_dot_env_loaded = False
