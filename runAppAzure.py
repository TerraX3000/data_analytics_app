from main_app import create_app
from main_app.config_azure import Config

app = create_app(config_class=Config)

if __name__ == "__main__":
    app.run("localhost", 8080, debug=True)
