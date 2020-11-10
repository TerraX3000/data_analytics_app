from main_app import getWebContent
from main_app.models import WebContent


def html_layout(title, returnToPage):
    return_href = "/" + returnToPage
    if returnToPage == "datavisualizationsamples":
        return_link_label = "Data Visualization Overview"
    elif returnToPage == "datasetanalyzer":
        return_link_label = "Dataset Analyzer"
    elif returnToPage == "telematics":
        return_link_label = "Telematics Analysis Demo Overview"
    else:
        return_link_label = "Previous Page"
    webContent = getWebContent(WebContent)
    if "dash-app-background-color" in webContent["layout"]:
        backgroundColor = webContent["layout"]["dash-app-background-color"]
    else:
        backgroundColor = webContent["layout"]["background-color"]

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
            <a href=" """
        + return_href
        + """ " class="w3-large"><i class="w3-padding fa fa-chevron-left"></i> Return to """
        + return_link_label
        + """</a>
            <span class="w3-bar-item w3-right">Data Analytics</span>
            </div>
        
        <div class="w3-main" style="margin-left:0px;margin-top:43px;">
            <div class="w3-col">
                <div class="w3-container """
        + webContent["layout"]["title-bar-color"]
        + """ w3-row">
                    <div class="w3-threequarter">
                        <h2>"""
        + title
        + """</h2>
                    </div>
                </div>
            </div>
        </div>
            <div class="w3-panel """
        + webContent["layout"]["background-color"]
        + """ "></div>
            <div class=" """
        + backgroundColor
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
