from os import popen

if __name__ == '__main__':
    migration_message: str = input('migration message: ')
    # FIXME: This seems dangerous for security
    popen(f'alembic revision --autogenerate -m"{migration_message}"')
    popen('alembic upgrade heads')
