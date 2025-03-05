from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=['settings.toml', '.secrets.toml'],
    envvar_prefix=False,
    load_dotenv=True,
    dotenv_path=".env",
)
