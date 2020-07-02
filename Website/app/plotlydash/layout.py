"""Plotly Dash HTML layout override."""

html_layout = '''
<!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            <link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
            {%css%}
        </head>
     
    <body id="dash_body">   
        <nav class="navbar fixed-top navbar-light bg-light">
        <div class="flex-grow-1 d-flex">
            <div class="d-flex">
                <div class="d-flex " >
                   <a class="nav-item nav-link h3" href="/home">Home</a>
                </div>
                <div  class="d-flex justify-content-end">
                    <a class="nav-item nav-link h3" href="/dashapp">Visualization Dashboard</a>
                </div>
            </div>
            <div class="d-flex ml-auto">
                <span class="navbar-brand" href="#">
                    <img src="/static/assets/DAC_logo.png"
                         width="30" height="30"
                         class="d-inline-block"
                         alt="Virginia Tech">
                </span>
            </div>
        </div>
    </nav>
  
        <div class=" mr-3  container-fluid ">
        {%app_entry%}
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        </body>
    </html>
'''