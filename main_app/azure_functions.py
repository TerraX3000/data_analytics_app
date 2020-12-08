import os
import sqlalchemy
import urllib


def getAzureSqlUrl():
    db_host = os.environ.get("DB_HOST", "db_host_placeholder")
    db_user = os.environ.get("DB_USER", "db_user_placeholder")
    db_pass = os.environ.get("DB_PASS", "db_pass_placeholder")
    db_name = os.environ.get("DB_NAME", "db_name_placeholder")

    # print(engine_azure.table_names())

    # dialect+driver://username:password@host:port/database

    # https://stackoverflow.com/questions/25785252/how-to-connect-to-mysql-server-with-ssl-from-a-flask-app
    sqlUrl = sqlalchemy.engine.url.URL(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_pass,
        host=db_host,
        port=3306,
        database=db_name,
        query={"ssl_ca": "main_app/certs/BaltimoreCyberTrustRoot.crt.pem"},
    )

    return sqlUrl


def getSqlEngineOptions():
    db_config = {
        # [START cloud_sql_mysql_sqlalchemy_limit]
        # Pool size is the maximum number of permanent connections to keep.
        "pool_size": 5,
        # Temporarily exceeds the set pool_size if no connections are available.
        "max_overflow": 2,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.
        # [END cloud_sql_mysql_sqlalchemy_limit]
        # [START cloud_sql_mysql_sqlalchemy_backoff]
        # SQLAlchemy automatically uses delays between failed connection attempts,
        # but provides no arguments for configuration.
        # [END cloud_sql_mysql_sqlalchemy_backoff]
        # [START cloud_sql_mysql_sqlalchemy_timeout]
        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        "pool_timeout": 30,  # 30 seconds
        # [END cloud_sql_mysql_sqlalchemy_timeout]
        # [START cloud_sql_mysql_sqlalchemy_lifetime]
        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # reestablished
        "pool_recycle": 1800,  # 30 minutes
        "pool_pre_ping": True,  # enable the connection pool “pre-ping” feature
        # that tests connections for liveness upon each checkout.  Added to
        # address error 'Lost connection to MySQL server during query'
        # [END cloud_sql_mysql_sqlalchemy_lifetime]
    }
    return db_config