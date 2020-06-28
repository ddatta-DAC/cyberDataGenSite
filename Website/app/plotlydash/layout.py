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
        
        <body >
         
        <nav class="navbar navbar-expand-lg light bg-light">
            <div class="d-flex align-content-around flex-wrap">
                <div class=" align-self-start h3" >
                   <a class="nav-item nav-link" href="/home">Home</a>
                </div>
                <div  class="align-self-end h1">
                 <a class="nav-item nav-link" href="/dashapp">Visualization Dashboard</a>
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