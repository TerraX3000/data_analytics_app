from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, MetaData
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import pytz

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
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

# Instantiate the database
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
# # Instantiate up the login_manager
# login_manager = LoginManager()
# # Instantiate oauth for managing authentication
# oauth = OAuth()


# This function is used in jinja2 templates to display UTC datetime strings in local time
def datetimefilter(value, format="%a %b %-d @ %-I:%M %p"):
    tz = pytz.timezone("US/Eastern")  # timezone you want to convert to from UTC
    utc = pytz.timezone("UTC")
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(format)


def getWebContent(WebContent):
    # This function creates a dictionary for webContent data stored in the database.
    # WebContent is accessed by calling this dictionary structure:
    # {{ webContent[pageName][blockName] }}
    # WebContent contains data stored in the SQL database which can be
    # used to store information to customize app content.
    # WebContent is accessible by all templates by referencing
    # the WebContent dictionary.
    webContentDB = WebContent.query.all()
    webContent = {}
    for content in webContentDB:
        if content.webpageName in webContent:
            # print("webpageName found: ", content.webpageName)
            if content.blockName in webContent[content.webpageName]:
                # print("blockname found: ", content.blockName)
                webContent[content.webpageName][content.blockName] = content.webContent
            else:
                # print("new blockname: ", content.blockName)
                webContent[content.webpageName][content.blockName] = content.webContent
        else:
            # print("new webpageName: ", content.webpageName)
            webContent[content.webpageName] = {content.blockName: content.webContent}
    # print("webContent: ", webContent)
    return webContent


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.jinja_env.globals.update(zip=zip)
    app.jinja_env.filters["datetimefilter"] = datetimefilter
    # Initialize the database with the app
    db.init_app(app)
    # Initialize Migrate with the app and the database
    migrate.init_app(app, db)

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
    from main_app.datasetManager.routes import datasetManager_bp
    from main_app.datasetAnalyzer.routes import datasetAnalyzer_bp
    from main_app.researchInfo.routes import researchInfo_bp
    from main_app.dashapps.routes import dashapps_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(datavisualizationsamples_bp)
    app.register_blueprint(datasetManager_bp)
    app.register_blueprint(datasetAnalyzer_bp)
    app.register_blueprint(researchInfo_bp)
    app.register_blueprint(dashapps_bp)

    # Add context processor to make webContent data stored in the database
    # available to all templates by default
    from main_app.models import WebContent

    @app.context_processor
    def setWebContentAppContext():
        return dict(webContent=getWebContent(WebContent))

    # Import Dash application
    # Push an application context so we can use Flask's 'current_app'
    # which is necessary to import db for initializing dataframes
    with app.app_context():
        from main_app.dashapps.dashboard import register_dashapp
        from main_app.dashapps.dashapp1.layout import layout as layout1

        from main_app.dashapps.dashapp2.layout import layout as layout2
        from main_app.dashapps.dashapp2.callbacks import (
            register_callbacks as register_callbacks2,
        )
        from main_app.dashapps.dashapp3.layout import layout as layout3
        from main_app.dashapps.dashapp4.layout import layout as layout4
        from main_app.dashapps.dashapp4.callbacks import (
            register_callbacks as register_callbacks4,
        )
        from main_app.dashapps.dashapp5.layout import layout as layout5
        from main_app.dashapps.dashapp5.callbacks import (
            register_callbacks as register_callbacks5,
        )
        from main_app.dashapps.dashapp6.layout import layout as layout6
        from main_app.dashapps.dashapp6.layout import (
            register_callbacks as register_callbacks6,
        )
        from main_app.dashapps.dashapp7.layout import layout as layout7
        from main_app.dashapps.dashapp7.layout import (
            register_callbacks as register_callbacks7,
        )
        from main_app.dashapps.dashapp8.layout import layout as layout8
        from main_app.dashapps.dashapp8.layout import (
            register_callbacks as register_callbacks8,
        )
        from main_app.dashapps.dashapp10.layout import layout as layout10
        from main_app.dashapps.dashapp10.layout import (
            register_callbacks as register_callbacks10,
        )

    register_dashapp(
        app, "Bar Chart Sample", "dashapp", "datavisualizationsamples", layout1, False
    )
    register_dashapp(
        app,
        "Callback Example",
        "dashapp2",
        "datavisualizationsamples",
        layout2,
        register_callbacks2,
    )
    register_dashapp(
        app, "Population Chart", "dashapp3", "datavisualizationsamples", layout3, False
    )
    register_dashapp(
        app,
        "Cross Filtering",
        "dashapp4",
        "datavisualizationsamples",
        layout4,
        register_callbacks4,
    )
    register_dashapp(
        app,
        "Generic Cross Filtering",
        "dashapp5",
        "datavisualizationsamples",
        layout5,
        register_callbacks5,
    )
    register_dashapp(
        app,
        "Real-Time Data Visualization",
        "dashapp6",
        "datavisualizationsamples",
        layout6,
        register_callbacks6,
    )
    register_dashapp(
        app, "Bar Chart", "dashapp7", "datasetanalyzer", layout7, register_callbacks7
    )
    register_dashapp(
        app, "Scatter Plot", "dashapp8", "datasetanalyzer", layout8, register_callbacks8
    )
    register_dashapp(
        app,
        "Line Plot",
        "dashapp10",
        "datasetanalyzer",
        layout10,
        register_callbacks10,
    )

    return app
