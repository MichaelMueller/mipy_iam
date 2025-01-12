from typing import Any, Optional
import aiofiles, argparse, aioconsole, pydantic


from dotenv import dotenv_values, set_key

##### module public       
async def require(key: str, help:str, type_:str, default:Any=None) -> dict:
    value, existed = get(key, help, type_, default)
    
    if not existed:
        valid_input = False
        while not valid_input:
            user_input = await aioconsole.ainput(f"Enter value for {key}: {help} - default: {default}: ") or default
            try:
                user_input = type_(user_input)    
                set(key, user_input)        
                valid_input = True    
            except (ValueError, argparse.ArgumentTypeError) as e:
                print(f"Invalid value. Expected {type_.__name__}.")
            
    return value

async def get( key: str, help:str, type_:str, default:Any=None ) -> tuple[Any, bool]:
    global _dot_env_dict
    
    # check if we have a cli arg    
    parser = argparse.ArgumentParser()
    parser.add_argument(f"--{key}", type = type_, default=None)
    args, _ = parser.parse_known_args()
    value = getattr(args, key)
    if value is not None:
        return value, True
    
    _load_dotenv()
    if key in _dot_env_dict:
        return type_( _dot_env_dict[key] ), True
    
    return default, False

async def set(key: str, value: str) -> None:
    _load_dotenv()
    _dot_env_dict[key] = value
    await _dump_dotenv()

async def remove(key: str) -> None:
    _load_dotenv()
    del _dot_env_dict[key]
    await _dump_dotenv()
    
##### module private
async def _load_dotenv():
    global _dot_env_dict
    
    if _dot_env_dict == None:
        """Asynchronously reads and parses a .env file."""
        async with aiofiles.open(_ENV_FILE_PATH, mode='r') as file:
            content = await file.read()
        _dot_env_dict = dotenv_values(stream=content)
        
async def _dump_dotenv():
    _load_dotenv()
    lines = []
    for key, value in _dot_env_dict.items():
        lines.append( f"{key}={value}" )
    async with aiofiles.open(_ENV_FILE_PATH, mode='w') as file:
        await file.write("\n".join(lines)) # TODO help strings here??
        
### PRIVATE
_ENV_FILE_PATH = ".env"
_dot_env_dict:dict|None = {}