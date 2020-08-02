"""Plotly Dash HTML layout override."""

html_layout = '''
<!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            <link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
            {%css%}
        </head>
     
    <body id="dash_body">   
        <nav class="navbar fixed-top navbar-light bg-light">
        <div class="flex-grow-1 d-flex">
            <div class="d-flex">
                <div class="d-flex " >
                   <a class="nav-item nav-link h4" href="/home">Home</a>
                </div>
                 <div  class="d-flex justify-content-around">
                    <a class="nav-item nav-link h4" href="/generatedData_page"> << Back  </a>
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