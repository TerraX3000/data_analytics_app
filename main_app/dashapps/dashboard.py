"""Instantiate a Dash app."""
import dash
from .layout import html_layout


def register_dashapp(app, title, base_pathname, layout, register_callbacks_fun):
    # Meta tags for viewport responsiveness
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no",
    }
    # __name__,
    # assets_folder=get_root_path(__name__) + f"/{base_pathname}/assets/",
    # url_base_pathname=f"/{base_pathname}/",
    # routes_pathname_prefix="/{base_pathname}/",
    print("base_pathname = ", base_pathname)
    my_dashapp = dash.Dash(
        __name__,
        server=app,
        url_base_pathname=f"/{base_pathname}/",
        meta_tags=[meta_viewport],
        external_stylesheets=[
            "/static/dash.css",
            "https://fonts.googleapis.com/css?family=Lato",
            "https://www.w3schools.com/w3css/4/w3.css",
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
        ],
    )
    # Push an application context so we can use Flask's 'current_app'
    with app.app_context():
        my_dashapp.index_string = html_layout
        my_dashapp.title = title
        my_dashapp.layout = layout
        print("app context")
        if register_callbacks_fun:
            register_callbacks_fun(my_dashapp)
            print("register callbacks")
