class DatabaseOperationsService:
    _connection: None # TODO: Database connection
    _counter: int

    def __init__(self, initial_count: int = 0) -> None:
        self._counter = initial_count

    def add(self, amount: int) -> None:
        self._counter = self._counter + amount

    def get_counter(self) -> int:
        return self._counter