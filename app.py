"""
Databricks Presentation Creator - Dash Application
Interactive web app for creating Databricks-branded presentations using Claude AI
"""
import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from databricks_auth import DatabricksAuth
from claude_client import ClaudeClient
from ppt_generator import PPTGenerator
import base64
import traceback
from datetime import datetime


# Initialize Dash app with Databricks-style theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

# Databricks brand colors
DATABRICKS_RED = '#FF3621'
DATABRICKS_DARK = '#1B3139'
DATABRICKS_BLUE = '#00A4E4'
DATABRICKS_GRAY = '#F5F5F5'

# Custom CSS for Databricks branding
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Databricks Presentation Creator</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                background-color: #f5f5f5;
            }
            .databricks-header {
                background: linear-gradient(135deg, #1B3139 0%, #2C4A56 100%);
                color: white;
                padding: 20px;
                margin-bottom: 30px;
                border-bottom: 4px solid #FF3621;
            }
            .card {
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            .btn-databricks {
                background-color: #FF3621 !important;
                border-color: #FF3621 !important;
                color: white !important;
                font-weight: 600;
                padding: 12px 30px;
                border-radius: 4px;
                transition: all 0.3s;
            }
            .btn-databricks:hover {
                background-color: #E62E1C !important;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(255, 54, 33, 0.3);
            }
            .form-control:focus {
                border-color: #FF3621;
                box-shadow: 0 0 0 0.2rem rgba(255, 54, 33, 0.25);
            }
            .status-indicator {
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
                margin: 10px 0;
            }
            .status-success {
                background-color: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .status-error {
                background-color: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            .status-info {
                background-color: #d1ecf1;
                color: #0c5460;
                border: 1px solid #bee5eb;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1([
            html.Span("Databricks ", style={'color': DATABRICKS_RED}),
            html.Span("Presentation Creator", style={'color': 'white'})
        ], style={'margin': 0, 'fontSize': '36px'}),
        html.P("AI-Powered Solutions Architecture Presentations",
               style={'margin': '10px 0 0 0', 'opacity': 0.9, 'fontSize': '18px'})
    ], className='databricks-header'),

    # Main content
    dbc.Container([
        dbc.Row([
            dbc.Col([
                # Connection Status Card
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Connection Status", className="card-title"),
                        html.Div(id='connection-status', children=[
                            html.Div("Checking Databricks connection...", className="status-indicator status-info")
                        ])
                    ])
                ], className="mb-4"),

                # Configuration Card
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Presentation Configuration", className="card-title mb-4"),

                        # Number of slides
                        html.Label("Number of Slides", className="form-label fw-bold"),
                        dcc.Input(
                            id='num-slides',
                            type='number',
                            value=5,
                            min=1,
                            max=20,
                            className='form-control mb-3'
                        ),

                        # Sections (optional)
                        html.Label("Sections (Optional - comma-separated)", className="form-label fw-bold"),
                        dcc.Input(
                            id='sections',
                            type='text',
                            placeholder='e.g., Introduction, Architecture, Implementation',
                            className='form-control mb-3'
                        ),

                        # Prompt
                        html.Label("Presentation Topic & Requirements", className="form-label fw-bold"),
                        dcc.Textarea(
                            id='prompt',
                            placeholder='Describe the presentation you want to create...\n\nExample: Create a presentation about real-time data processing using Databricks for a retail customer. Include medallion architecture, Delta Live Tables, and MLOps best practices.',
                            className='form-control mb-3',
                            style={'height': '200px', 'resize': 'vertical'}
                        ),

                        # Generate button
                        html.Div([
                            dbc.Button(
                                "Generate Presentation",
                                id='generate-btn',
                                className='btn-databricks',
                                n_clicks=0,
                                style={'width': '100%', 'marginTop': '20px'}
                            )
                        ]),

                        # Loading indicator
                        dcc.Loading(
                            id="loading",
                            type="default",
                            children=html.Div(id='loading-output')
                        ),
                    ])
                ]),

            ], width=6),

            dbc.Col([
                # Output Card
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Generated Presentation", className="card-title mb-4"),
                        html.Div(id='output-area', children=[
                            html.P("Configure your presentation and click 'Generate Presentation' to begin.",
                                   className="text-muted")
                        ]),
                        html.Div(id='download-area')
                    ])
                ], style={'minHeight': '400px'}),

                # Info Card
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Features", className="card-title"),
                        html.Ul([
                            html.Li("Claude Sonnet 4.5 AI generation"),
                            html.Li("Databricks branding & colors"),
                            html.Li("Medallion architecture diagrams"),
                            html.Li("Architecture building blocks"),
                            html.Li("Solutions architect best practices"),
                        ], style={'marginBottom': 0})
                    ])
                ], className="mt-3"),
            ], width=6),
        ]),
    ], fluid=True),

    # Store for auth credentials
    dcc.Store(id='auth-store'),
])


@app.callback(
    [Output('connection-status', 'children'),
     Output('auth-store', 'data')],
    Input('connection-status', 'id')
)
def check_databricks_connection(_):
    """Check Databricks connection on app load"""
    try:
        db_auth = DatabricksAuth()
        success, message = db_auth.test_connection()

        if success:
            status_div = html.Div([
                html.Div([
                    html.I(className="bi bi-check-circle-fill me-2"),
                    message
                ], className="status-indicator status-success")
            ])
            credentials = db_auth.get_credentials()
            return status_div, credentials
        else:
            status_div = html.Div([
                html.Div([
                    html.I(className="bi bi-exclamation-triangle-fill me-2"),
                    f"Connection failed: {message}"
                ], className="status-indicator status-error"),
                html.P("Please ensure Databricks CLI is configured correctly.", className="text-muted mt-2")
            ])
            return status_div, None

    except Exception as e:
        status_div = html.Div([
            html.Div([
                html.I(className="bi bi-exclamation-triangle-fill me-2"),
                f"Error: {str(e)}"
            ], className="status-indicator status-error"),
            html.P("Please run 'databricks configure' to set up your credentials.", className="text-muted mt-2")
        ])
        return status_div, None


@app.callback(
    [Output('output-area', 'children'),
     Output('download-area', 'children'),
     Output('loading-output', 'children')],
    Input('generate-btn', 'n_clicks'),
    [State('num-slides', 'value'),
     State('sections', 'value'),
     State('prompt', 'value'),
     State('auth-store', 'data')],
    prevent_initial_call=True
)
def generate_presentation(n_clicks, num_slides, sections_str, prompt, auth_data):
    """Generate presentation using Claude and create PowerPoint"""
    if not n_clicks:
        return dash.no_update, dash.no_update, dash.no_update

    # Validate inputs
    if not prompt or not prompt.strip():
        error_msg = html.Div([
            html.Div("Please provide a presentation topic and requirements.",
                    className="status-indicator status-error")
        ])
        return error_msg, None, None

    if not auth_data:
        error_msg = html.Div([
            html.Div("Databricks authentication not available. Please check your connection.",
                    className="status-indicator status-error")
        ])
        return error_msg, None, None

    try:
        # Parse sections
        sections = None
        if sections_str and sections_str.strip():
            sections = [s.strip() for s in sections_str.split(',') if s.strip()]

        # Initialize Claude client
        claude_client = ClaudeClient(
            host=auth_data['host'],
            token=auth_data['token']
        )

        # Generate content
        status_msg = html.Div([
            html.Div("Generating presentation content with Claude AI...",
                    className="status-indicator status-info")
        ])

        content = claude_client.generate_presentation_content(
            prompt=prompt,
            num_slides=num_slides,
            sections=sections
        )

        # Create PowerPoint
        ppt_gen = PPTGenerator()
        ppt_gen.create_presentation(content)

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"databricks_presentation_{timestamp}.pptx"
        filepath = f"/tmp/{filename}"

        # Save presentation
        ppt_gen.save_presentation(filepath)

        # Read file for download
        with open(filepath, 'rb') as f:
            ppt_bytes = f.read()

        encoded = base64.b64encode(ppt_bytes).decode()

        # Create success message
        success_msg = html.Div([
            html.Div([
                html.I(className="bi bi-check-circle-fill me-2"),
                "Presentation generated successfully!"
            ], className="status-indicator status-success"),
            html.Div([
                html.H5("Presentation Details:", className="mt-3"),
                html.P(f"Title: {content.get('title', 'Untitled')}"),
                html.P(f"Number of slides: {len(content.get('slides', []))}"),
                html.P(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"),
            ])
        ])

        # Create download button
        download_btn = html.Div([
            html.A(
                dbc.Button(
                    [html.I(className="bi bi-download me-2"), "Download Presentation"],
                    className="btn-databricks mt-3",
                    style={'width': '100%'}
                ),
                id='download-link',
                download=filename,
                href=f"data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,{encoded}",
            )
        ], className="mt-3")

        return success_msg, download_btn, None

    except Exception as e:
        error_msg = html.Div([
            html.Div([
                html.I(className="bi bi-exclamation-triangle-fill me-2"),
                f"Error generating presentation: {str(e)}"
            ], className="status-indicator status-error"),
            html.Details([
                html.Summary("Show error details"),
                html.Pre(traceback.format_exc(), style={'fontSize': '12px', 'marginTop': '10px'})
            ])
        ])
        return error_msg, None, None


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Databricks Presentation Creator")
    print("="*60)
    print("\nStarting Dash application...")
    print("Open your browser to: http://localhost:8050")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")

    app.run_server(debug=True, host='0.0.0.0', port=8050)
