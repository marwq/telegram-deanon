from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    BOT_TOKEN: str
    BOT_USERNAME: str
    TARGET_USERNAME: str
    PATH_TO_TYNIDB: str
    
    class Config:
        env_file = ".env"
        
settings = Settings()