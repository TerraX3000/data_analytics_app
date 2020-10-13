"""Plotly Dash HTML layout override."""

html_layout = """
<!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
        </head>
        <body class="w3-light-grey">
        <!-- Top container -->
            <div class="w3-bar w3-top w3-blue w3-large" style="z-index:4">
            <a href="/dashsamples" class="w3-large"><i class="w3-padding fa fa-chevron-left"></i> Return to Data Visualization Overview</a>
            <span class="w3-bar-item w3-right">Data Analytics</span>
            </div>
        
        <div class="w3-main" style="margin-left:0px;margin-top:43px;">
            <div class="w3-col">
                <div class="w3-container w3-amber w3-row">
                    <div class="w3-third">
                        <h2>Dash Examples</h2>
                    </div>
                </div>
            </div>
        </div>
            <div class="w3-panel"></div>
            <div class="w3-container">
                {%app_entry%}
            </div>
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
"""
