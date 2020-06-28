"""Plotly Dash HTML layout override."""

html_layout = '''
<!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
        </head>
        <body class="dash-template">
            <header>
              <div class="navbar navbar-expand-lg navbar-light bg-light">
                <a href="/">
                    <h1>Visualization Dashboard</h1>
                  </a>
                <nav>
                 <a href="/index">
                    <h1>Home</h1>
                  </a>
                </nav>
            </div>
            </header>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
'''