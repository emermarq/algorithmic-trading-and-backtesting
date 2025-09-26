from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# importa sua Base de modelos
import os
import sys

# garante que a pasta "app" está no path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db.models import Base  # IMPORTANTE: aqui está o declarative_base()

# Configuração do Alembic
config = context.config
fileConfig(config.config_file_name)

# Alembic precisa do metadata para comparar com o banco
target_metadata = Base.metadata


def run_migrations_offline():
    """Executa migrações em modo offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Executa migrações em modo online."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
