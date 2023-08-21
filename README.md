# Rat's Nest

Rat's Nest is a private project started to get into fastapi.

## Installation

Clone the repository, then navigate to the root directory.

Install all the dependencies with pip. You can also use a virtual environment for this.

```bash
pip install -r requirements.txt
```

## Environment Variables

The application needs to run in an environment with specific variables. The list below shows them all:
```properties
RANDOM_URL=<str>
```

## Build the Database

On application startup it will try to connect to a database. In order for the connection to be established
you are provided with a Dockerfile located in the root of the project `./Dockerfile`.

To build the Docker-Image use the following command:
```bash
docker build -t rats-nest-db:latest . --no-cache
```

Once the build process is finished you can start your MariaDB container using the command:
```bash
docker run -p 8888:3306 --env-file <path-to-env-file> -d rats-nest-db:latest
```
For the `<path-to-env-file>` you will need to provide a valid environment file. It should contain the following
attributes:
```properties
MARIADB_RANDOM_ROOT_PASSWORD=<yes|no>
MARIADB_ROOT_HOST=<hostname>
MARIADB_USER=<username>
MARIADB_PASSWORD=<password>
MARIADB_DATABASE=<database>
```

## Start the Application
TODO

## Contributing

I don't think someone would want to contribute to this playground application but if you feel exceptionally
cool go for it! Just open a pull-request and I'll give my best to have a look.

## License

[GNU](https://choosealicense.com/licenses/gpl-3.0/)