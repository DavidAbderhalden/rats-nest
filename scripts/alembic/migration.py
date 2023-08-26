"""Script for all alembic related operations"""
from os import system
import sys


class AlembicOperationsSettings:
    _PROGRAM_ARGUMENTS: list[str] = sys.argv[1:]
    _argument_identifiers: list[str] = ['-v', '--version', '-h', '--help', '-r', '--revision', '-u', '--upgrade']
    _VERSION: str = '0.0.1'
    _USER_MANUAL: str = '''
        - TODO: Write this manual ...
    '''

    def __init__(self) -> None:
        clusters: list[list[str]] = []
        for arg in self._PROGRAM_ARGUMENTS:
            if arg.startswith('--') or arg.startswith('-'):
                clusters.append([arg])
            else:
                clusters[-1].append(arg)

        for cluster in clusters:
            self._preset_cluster(cluster)

    def _preset_cluster(self, cluster: list[str]):
        unknown_identifier: str = cluster[0]
        preset_values: list[str] = cluster[1:]
        if unknown_identifier in self._argument_identifiers:
            match unknown_identifier:
                case '-v' | '--version':
                    self._display_version()
                case '-h' | '--help':
                    self._display_manual()
                case '-r' | '--revision':
                    self._create_revision(preset_values)
                case '-u' | '--upgrade':
                    self._upgrade_head()

        else:
            print(f'\nUnknown parameter \'{unknown_identifier}\'\nUse \'--help\' for user manual.')
            sys.exit(0)

    def _display_version(self) -> None:
        print(f'\nalembic-operations-script version {self._VERSION}')
        sys.exit(0)

    def _display_manual(self):
        print(f'\n{self._USER_MANUAL}')
        sys.exit(0)

    @classmethod
    def _upgrade_head(cls):
        system('alembic upgrade heads')

    @classmethod
    def _create_revision(cls, preset_values: list[str]):
        migration_message: str = input('migration message: ')
        if 'auto' in preset_values:
            system(f'alembic revision --autogenerate -m"{migration_message}"')
        else:
            system(f'alembic revision -m"{migration_message}"')


if __name__ == '__main__':
    try:
        AlembicOperationsSettings()
    except KeyboardInterrupt:
        sys.exit(0)
