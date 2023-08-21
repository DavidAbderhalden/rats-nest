FROM mysql:latest

COPY /conf.d/config-file.cnf /etc/mysql/conf.d/config-file.cnf

COPY /init/init.sql /docker-entrypoint-initdb.d

EXPOSE 3306

CMD ["mysqld"]