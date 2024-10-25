from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

#pentru preluarea variabilelor de mediu, #rezolvare diferita fata de Sanjeev
import os
from dotenv import load_dotenv
                       


#pentru "autogenerare" este necesar importul modelelor de date folosite in BD
# pentru a lucra cu obiectele definite in bazadedate.py, se importa aici
#from app.bazadedate1 import Baza   #se da acces la toate obiectele SQLAlchemy


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
#                   adica FastAPI\alembic.ini necesare pentru preluarea valorii
#                   configuratiei mediului de lucru: nume server, BD si utilizator...
#                   si protectiei datelor si aplicatiei: parole, metode de criptare...
config = context.config

#ce urmeaza suprascrie "sqlalchemy.url" din setul de configurare initial alembic.ini
# in alembic.ini lasi sqlalchemy.url = 
# config.set_main_option("sqlalchemy.url",
#                    "postgresql+psycopg2://postgres:Superadmin@localhost:5432/fastapi")


#rezolvare diferita de a lui Sanjeev si a Alembic Tutorial pentru preluare var. de mediu
load_dotenv('D:\Proiecte\FastAPI\mediudelucru.env') #folosita adresarea absoluta a fisier
database_hostname = os.getenv('DB_hostname')
database_port = os.getenv('DB_PORT')
database_password = os.getenv('DB_password')
database_name = os.getenv('DB_name')
database_username = os.getenv('DB_username')
#pentru test
print("[env.py] Citite din fisierul mediudelucr.env: database_hostname = ", database_hostname, ", database_port = ",
      database_port, ", database_password = ", database_password, ", database_name = ", database_name, ", database_username = ",
      database_username)
config.set_main_option("sqlalchemy.url",
f'postgresql://{database_username}:{database_password}@{database_hostname}:{database_port}/{database_name}') 

# Interpret the config file for Python logging. <- ce-o fi asta?
# This line sets up loggers basically.  
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel 
#           #la mine: from app.modele import Baza
# target_metadata = mymodel.Base.metadata   
#           #la mine mymodel.Base este app.bazadedate1.Baza
#           # Baza.metadata     #?? nu am un astfel de obiect in Baza 
#           # !! cursul foloseste SQLALchemy.v1, v depasita !!!
#target_metadata = None
from app.bazadedate1 import Baza
target_metadata = Baza

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
