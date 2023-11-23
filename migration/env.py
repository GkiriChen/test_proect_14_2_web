from logging.config import fileConfig
import asyncio
from sqlalchemy.engine import Connection
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

from src.database.models import Base
from src.conf.config import settings

# Initialize Alembic configuration
config = context.config

# Check if an Alembic configuration file is specified
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for migrations
target_metadata = Base.metadata

# Set the database URL
config.set_main_option("sqlalchemy.url", settings.postgres_url)


def do_run_migrations(connection: Connection) -> None:
    # Configure Alembic context with the connection and target metadata
    context.configure(connection=connection, target_metadata=target_metadata)

    # Run migrations within a transaction
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario, we need to create an Engine
    and associate a connection with the context.
    """

    # Create an asynchronous engine and connection
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Execute migrations in asynchronous mode
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    # Dispose of resources after migrations are complete
    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


# Call the function to run migrations in online mode
run_migrations_online()
