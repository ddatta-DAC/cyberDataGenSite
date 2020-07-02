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
        <div class="container d-flex align-content-around  flex-wrap">
            <div class="d-flex  justify-content-start ">
                <div class=" align-self-start h2" >
                   <a class="nav-item nav-link" href="/home">Home</a>
                </div>
                <div  class="align-self-end h2">
                    <a class="nav-item nav-link active" href="/dashapp">Visualization Dashboard</a>
                </div>
            </div>
            <div class="d-flex justify-content-end">
            <a class="navbar-brand" href="#">
            <img src="/static/DAC_logo.png" width="30" height="30" class="d-inline-block align-top" alt="Virginia Tech">
                
            </a>
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