from main_app import getWebContent
from main_app.models import WebContent


def html_layout():
    webContent = getWebContent(WebContent)
    webContent["layout"]["top-bar-color"]
    webContent["layout"]["title-bar-color"]
    webContent["layout"]["background-color"]
    layout = (
        """
<!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
        </head>
        <body class=" """
        + webContent["layout"]["background-color"]
        + """ " ">
        <!-- Top container -->
            <div class="w3-bar w3-top """
        + webContent["layout"]["top-bar-color"]
        + """ w3-large" style="z-index:4">
            <a href="/datavisualizationsamples" class="w3-large"><i class="w3-padding fa fa-chevron-left"></i> Return to Data Visualization Overview</a>
            <span class="w3-bar-item w3-right">Data Analytics</span>
            </div>
        
        <div class="w3-main" style="margin-left:0px;margin-top:43px;">
            <div class="w3-col">
                <div class="w3-container """
        + webContent["layout"]["title-bar-color"]
        + """ w3-row">
                    <div class="w3-third">
                        <h2>Dash Examples</h2>
                    </div>
                </div>
            </div>
        </div>
            <div class="w3-panel """
        + webContent["layout"]["background-color"]
        + """ "></div>
            <div class=" """
        + webContent["layout"]["background-color"]
        + """ ">
                {%app_entry%}
            </div>
            <footer class=" """
        + webContent["layout"]["background-color"]
        + """ ">
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
"""
    )
    return layout
