from fastapi import FastAPI
import mipy_users, mipy_log, mipy_iam.db as db, mipy_iam.interactive as interactive
import mipy_config
import uvicorn

# include mipy_users and mipy_config and create a fastapi application
app = FastAPI()

# Include mipy_users and mipy_config routers
app.include_router(mipy_users.router)
app.include_router(mipy_config.router)

if __name__ == "__main__":
    
    log_level, _ = mipy_log.init()
    db.init()
    
    host = interactive.get_or_ask_and_wait_for_param("HOST", default="127.0.0.1", value_type=str)
    port = interactive.get_or_ask_and_wait_for_param("PORT", default="5000", value_type=int)
    dev = interactive.get_or_ask_and_wait_for_param("DEV", default="0", value_type=lambda x: x in ["1", "true", "y"])
    
    uvicorn.run("main:app", host=host, port=port, reload=dev, log_level=log_level)