from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app import db
from config import Config

# Alembic Config object
config = context.config

# Use the SQLALCHEMY_DATABASE_URI from Config
config.set_main_option('sqlalchemy.url', Config.SQLALCHEMY_DATABASE_URI)

# Set up logging
fileConfig(config.config_file_name)

# Target metadata for 'autogenerate'
target_metadata = db.metadata

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = db.engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True  # Optional: detects column type changes
        )

        with context.begin_transaction():
            context.run_migrations()

# Execute migrations
run_migrations_online()
