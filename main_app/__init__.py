from flask import Flask

# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import event, MetaData
# from sqlalchemy.engine import Engine
# from sqlite3 import Connection as SQLite3Connection
# from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand
# import pytz

# Third-party libraries for login authorization and management
# from authlib.integrations.flask_client import OAuth

# from flask_login import (
#     LoginManager,
#     current_user,
#     login_required,
#     login_user,
#     logout_user,
# )


# This function is necessary to perform cacade deletes in SQLite
# @event.listens_for(Engine, "connect")
# def _set_sqlite_pragma(dbapi_connection, connection_record):
#     if isinstance(dbapi_connection, SQLite3Connection):
#         cursor = dbapi_connection.cursor()
#         cursor.execute("PRAGMA foreign_keys=ON;")
#         cursor.close()


# naming_convention = {
#     "ix": "ix_%(column_0_label)s",
#     "uq": "uq_%(table_name)s_%(column_0_name)s",
#     "ck": "ck_%(table_name)s_%(column_0_name)s",
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#     "pk": "pk_%(table_name)s",
# }

# Instantiate the database
# db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
# migrate = Migrate()
# # Instantiate up the login_manager
# login_manager = LoginManager()
# # Instantiate oauth for managing authentication
# oauth = OAuth()


# This function is used in jinja2 templates to display UTC datetime strings in local time
# def datetimefilter(value, format="%a %b %-d @ %-I:%M %p"):
#     tz = pytz.timezone("US/Eastern")  # timezone you want to convert to from UTC
#     utc = pytz.timezone("UTC")
#     value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
#     local_dt = value.astimezone(tz)
#     return local_dt.strftime(format)


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # app.jinja_env.globals.update(zip=zip)
    # app.jinja_env.filters["datetimefilter"] = datetimefilter
    # Initialize the database with the app
    # db.init_app(app)
    # Initialize Migrate with the app and the database
    # migrate.init_app(app, db)

    # Set up for using Google Login and API (if running on Google Cloud)
    useGoogleLoginAndAPI = app.config.get("USE_GOOGLE_LOGIN_AND_API")
    print("useGoogleLoginAndAPI =", useGoogleLoginAndAPI)
    if useGoogleLoginAndAPI:
        pass
        # User session management setup
        # https://flask-login.readthedocs.io/en/latest
        # login_manager.init_app(app)

        # OAuth 2 client setup
        # GOOGLE_DISCOVERY_URL = (
        #     "https://accounts.google.com/.well-known/openid-configuration"
        # )
        # oauth.init_app(app)
        # oauth.register(
        #     name="google",
        #     server_metadata_url=GOOGLE_DISCOVERY_URL,
        #     client_kwargs={"scope": "openid email profile"},
        # )

    from main_app.main.routes import main_bp
    from main_app.datavisualizationsamples.routes import datavisualizationsamples_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(datavisualizationsamples_bp)

    return app
