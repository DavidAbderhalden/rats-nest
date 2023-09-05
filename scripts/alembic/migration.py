"""Script for all alembic related operations"""
from subprocess import CalledProcessError, check_output, STDOUT
import sys


def execute_command(command: str) -> str:
    try:
        output = check_output(command, stderr=STDOUT, shell=True, universal_newlines=True)
        return f' Success ->\n{output}'
    except CalledProcessError as error:
        return f'Error [code: {error.returncode}] ->\n{error.output}'


class AlembicOperationsSettings:
    _PROGRAM_ARGUMENTS: list[str] = sys.argv[1:]
    _argument_identifiers: list[str] = [
        '-v', '--version', '-h', '--help', '-r', '--revision', '-u', '--upgrade',  '-d', '--downgrade'
    ]
    _VERSION: str = '0.0.1'
    _USER_MANUAL: str = '''
        - TODO: Write this manual ...
    '''

    def __init__(self) -> None:
        output: dict[str, str] = self.start()
        for executed_command in output:
            print(f'{executed_command}\t\t| {output[executed_command]}')

    def start(self) -> dict[str, str]:
        clusters: list[list[str]] = []
        for arg in self._PROGRAM_ARGUMENTS:
            if arg.startswith('--') or arg.startswith('-'):
                clusters.append([arg])
            else:
                clusters[-1].append(arg)

        execution_result: dict[str, str] = dict()
        for cluster in clusters:
            command: str = ' '.join(cluster)
            execution_result[command] = self._preset_cluster(cluster)
        return execution_result

    def _preset_cluster(self, cluster: list[str]) -> str:
        identifier: str = cluster[0]
        preset_values: list[str] = cluster[1:]
        if identifier in self._argument_identifiers:
            match identifier:
                case '-v' | '--version':
                    return self._display_version()
                case '-h' | '--help':
                    return self._display_manual()
                case '-r' | '--revision':
                    return self._create_revision(preset_values)
                case '-u' | '--upgrade':
                    return self._upgrade(preset_values)
                case '-s' | '--downgrade':
                    return self._downgrade(preset_values)
                case n:
                    return f"{n} wasn't recognized as an internal command"

        else:
            return f'\nUnknown parameter \'{identifier}\'\nUse \'--help\' for user manual\n'

    def _display_version(self) -> str:
        print(f'\nalembic-operations-script version {self._VERSION}')
        return 'ok'

    def _display_manual(self) -> str:
        print(f'\n{self._USER_MANUAL}')
        return 'ok'

    @classmethod
    def _upgrade(cls,  preset_values: list[str]) -> str:
        match preset_values:
            case n if 'head' in n:
                return execute_command('alembic upgrade head')
            case n if 'heads' in n:
                return execute_command('alembic upgrade heads')
            case _:
                return f'unknown input {n}'

    @classmethod
    def _downgrade(cls,  preset_values: list[str]) -> str:
        match preset_values:
            case n if 'base' in n:
                return execute_command('alembic downgrade base')
            case _:
                return f'unknown input {n}'

    @classmethod
    def _create_revision(cls, preset_values: list[str]) -> str:
        migration_message: str = input('migration message: ')
        if 'auto' in preset_values:
            return execute_command(f'alembic revision --autogenerate -m"{migration_message}"')
        else:
            return execute_command(f'alembic revision -m"{migration_message}"')


if __name__ == '__main__':
    try:
        AlembicOperationsSettings()
    except KeyboardInterrupt:
        sys.exit(0)
