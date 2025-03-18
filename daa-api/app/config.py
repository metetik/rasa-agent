try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

def get_database_url():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
    
    db_config = config["database"]
    
    database_url = (
        f"postgresql://{db_config['user']}:{db_config['password']}"
        f"@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    )
    return database_url