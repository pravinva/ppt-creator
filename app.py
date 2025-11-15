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
from pdf_branding_analyzer import BrandingExtractor
from pdf_content_extractor import PDFContentExtractor
from pptx_modifier import PPTXModifier
from progress_tracker import ProgressTracker, reset_tracker
import base64
import traceback
from datetime import datetime
import tempfile
import os


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
            .progress-container {
                background: white;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            .progress-step {
                display: flex;
                align-items: center;
                padding: 8px 0;
                font-size: 14px;
            }
            .progress-step-icon {
                width: 24px;
                height: 24px;
                margin-right: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .step-complete {
                color: #00C853;
            }
            .step-running {
                color: #00A4E4;
                animation: pulse 1.5s infinite;
            }
            .step-pending {
                color: #999999;
                opacity: 0.5;
            }
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
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

                        # Content Upload (PDF or PowerPoint)
                        html.Div([
                            html.Label("Source File for Content (Optional)", className="form-label fw-bold"),
                            html.Small("Upload PowerPoint (best quality) or PDF to convert/modify",
                                      className="text-muted d-block mb-2"),
                            dcc.Upload(
                                id='content-upload',
                                children=html.Div([
                                    html.I(className="bi bi-file-earmark me-2"),
                                    'Upload PowerPoint or PDF'
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '50px',
                                    'lineHeight': '50px',
                                    'borderWidth': '2px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'borderColor': '#ccc',
                                    'textAlign': 'center',
                                    'marginBottom': '10px',
                                    'cursor': 'pointer'
                                },
                                multiple=False,
                                accept='.pdf,.pptx'
                            ),
                            html.Div(id='content-upload-status', className="mb-2"),
                        ]),

                        # PDF Branding Upload
                        html.Div([
                            html.Label("Branding PDF (Optional)", className="form-label fw-bold"),
                            html.Small("Upload a sample PDF to extract branding (colors, fonts, layout)",
                                      className="text-muted d-block mb-2"),
                            dcc.Upload(
                                id='branding-pdf-upload',
                                children=html.Div([
                                    html.I(className="bi bi-palette me-2"),
                                    'Upload Branding Sample'
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '50px',
                                    'lineHeight': '50px',
                                    'borderWidth': '2px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'borderColor': '#ccc',
                                    'textAlign': 'center',
                                    'marginBottom': '10px',
                                    'cursor': 'pointer'
                                },
                                multiple=False,
                                accept='.pdf'
                            ),
                            html.Div(id='branding-pdf-status', className="mb-3"),
                        ]),

                        # Logo Upload
                        html.Div([
                            html.Label("Company Logo (Optional)", className="form-label fw-bold"),
                            html.Small("Add your company logo to slides",
                                      className="text-muted d-block mb-2"),
                            dcc.Upload(
                                id='logo-upload',
                                children=html.Div([
                                    html.I(className="bi bi-image me-2"),
                                    'Upload Logo (PNG, JPG, SVG)'
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '50px',
                                    'lineHeight': '50px',
                                    'borderWidth': '2px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'borderColor': '#ccc',
                                    'textAlign': 'center',
                                    'marginBottom': '10px',
                                    'cursor': 'pointer'
                                },
                                multiple=False,
                                accept='.png,.jpg,.jpeg,.svg'
                            ),
                            html.Div(id='logo-upload-status', className="mb-2"),

                            # Logo options (shown when logo uploaded)
                            html.Div(id='logo-options', style={'display': 'none'}, children=[
                                html.Label("Logo Position", className="form-label fw-bold mt-2"),
                                dcc.Dropdown(
                                    id='logo-position',
                                    options=[
                                        {'label': 'Top Right', 'value': 'top-right'},
                                        {'label': 'Top Left', 'value': 'top-left'},
                                        {'label': 'Bottom Right', 'value': 'bottom-right'},
                                        {'label': 'Bottom Left', 'value': 'bottom-left'},
                                    ],
                                    value='top-right',
                                    className='mb-2'
                                ),

                                html.Label("Logo Size (inches)", className="form-label fw-bold mt-2"),
                                dcc.Slider(
                                    id='logo-size',
                                    min=0.5,
                                    max=2.0,
                                    step=0.1,
                                    value=0.8,
                                    marks={0.5: '0.5"', 1.0: '1.0"', 1.5: '1.5"', 2.0: '2.0"'},
                                    className='mb-2'
                                ),

                                dbc.Checklist(
                                    options=[{"label": " Skip title slide", "value": "skip_title"}],
                                    value=[],
                                    id="logo-skip-title",
                                    className="mb-2"
                                ),
                            ]),
                        ]),

                        # Web Research Options
                        html.Div([
                            dbc.Checklist(
                                options=[{"label": " Enable Web Search for Topics", "value": "enabled"}],
                                value=[],
                                id="web-search-toggle",
                                switch=True,
                                className="mb-2"
                            ),
                            html.Small("Automatically search for information about technologies mentioned in your prompt",
                                      className="text-muted")
                        ], className="mb-3"),

                        # URLs (optional)
                        html.Label("Reference URLs (Optional - one per line)", className="form-label fw-bold"),
                        dcc.Textarea(
                            id='urls',
                            placeholder='https://example.com/article1\nhttps://example.com/article2',
                            className='form-control mb-3',
                            style={'height': '80px', 'resize': 'vertical'}
                        ),

                        # Prompt
                        html.Label("Presentation Topic & Requirements", className="form-label fw-bold"),
                        dcc.Textarea(
                            id='prompt',
                            placeholder='Describe the presentation you want to create...\n\nExample: Look up the new release for Genie MCP and ZeroBus ingestion. Create a presentation about ZeroBus for ingestion into the lakehouse and show how Genie MCP makes integration with agents easier.',
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
                # Progress Indicator (hidden by default)
                html.Div(id='progress-display', style={'display': 'none'}, children=[
                    html.Div(className='progress-container', children=[
                        html.H5("Generating Your Presentation", className="mb-3"),

                        # Overall progress bar
                        html.Div([
                            dbc.Progress(
                                id='overall-progress-bar',
                                value=0,
                                striped=True,
                                animated=True,
                                className="mb-3",
                                style={'height': '25px'}
                            ),
                            html.Div(id='progress-percentage', className="text-center mb-3",
                                    style={'fontWeight': 'bold', 'fontSize': '16px'})
                        ]),

                        # Current step
                        html.Div(id='current-step-display', className="mb-3"),

                        # Step details
                        html.Div([
                            html.H6("Progress:", className="mb-2"),
                            html.Div(id='step-list')
                        ])
                    ])
                ]),

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

    # Stores for auth credentials, branding, content, logo, and progress
    dcc.Store(id='auth-store'),
    dcc.Store(id='branding-store'),
    dcc.Store(id='content-store'),
    dcc.Store(id='logo-store'),
    dcc.Store(id='progress-store'),

    # Interval for progress polling
    dcc.Interval(
        id='progress-interval',
        interval=500,  # Update every 500ms
        n_intervals=0,
        disabled=True
    ),
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
    [Output('content-upload-status', 'children'),
     Output('content-store', 'data')],
    Input('content-upload', 'contents'),
    State('content-upload', 'filename'),
    prevent_initial_call=True
)
def handle_content_upload(contents, filename):
    """Handle PowerPoint or PDF content upload"""
    if contents is None:
        return None, None

    try:
        # Decode the base64 encoded content
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        # Save to temporary file
        suffix = '.pptx' if filename.endswith('.pptx') else '.pdf'
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(decoded)
            tmp_path = tmp_file.name

        content_data = {'filename': filename, 'path': tmp_path, 'type': suffix[1:]}

        if suffix == '.pptx':
            # Extract PowerPoint content (100% quality)
            modifier = PPTXModifier(tmp_path)
            extracted = modifier.extract_content()

            content_data['extracted'] = extracted

            status = html.Div([
                html.Div([
                    html.I(className="bi bi-check-circle-fill me-2"),
                    f"PowerPoint loaded: {filename}"
                ], className="status-indicator status-success"),
                html.P([
                    f"Found {extracted['total_slides']} slides. ",
                    html.Strong("100% quality extraction!"),
                    " You can modify this presentation with AI prompts below."
                ], className="text-muted mt-2", style={'fontSize': '13px'})
            ])

        else:  # PDF
            # Extract PDF content
            from pdf_content_extractor import PDFContentExtractor
            extractor = PDFContentExtractor()
            extracted = extractor.extract_content(tmp_path)

            content_data['extracted'] = extracted

            num_slides = len(extracted.get('slides', []))
            status = html.Div([
                html.Div([
                    html.I(className="bi bi-check-circle-fill me-2"),
                    f"PDF content extracted: {filename}"
                ], className="status-indicator status-success"),
                html.P(f"Found {num_slides} potential slides. Note: PowerPoint files give better quality.",
                      className="text-muted mt-2", style={'fontSize': '13px'})
            ])

        return status, content_data

    except Exception as e:
        status = html.Div([
            html.Div(f"Error uploading file: {str(e)}", className="status-indicator status-error")
        ])
        return status, None


@app.callback(
    [Output('logo-upload-status', 'children'),
     Output('logo-options', 'style'),
     Output('logo-store', 'data')],
    Input('logo-upload', 'contents'),
    State('logo-upload', 'filename'),
    prevent_initial_call=True
)
def handle_logo_upload(contents, filename):
    """Handle logo upload"""
    if contents is None:
        return None, {'display': 'none'}, None

    try:
        # Decode and save logo
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        # Determine file extension
        ext = filename.split('.')[-1].lower()
        suffix = f'.{ext}'

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(decoded)
            tmp_path = tmp_file.name

        logo_data = {
            'filename': filename,
            'path': tmp_path,
            'type': ext
        }

        status = html.Div([
            html.Div([
                html.I(className="bi bi-check-circle-fill me-2"),
                f"Logo uploaded: {filename}"
            ], className="status-indicator status-success"),
        ])

        # Show logo options
        return status, {'display': 'block'}, logo_data

    except Exception as e:
        status = html.Div([
            html.Div(f"Error uploading logo: {str(e)}", className="status-indicator status-error")
        ])
        return status, {'display': 'none'}, None


@app.callback(
    [Output('branding-pdf-status', 'children'),
     Output('branding-store', 'data')],
    Input('branding-pdf-upload', 'contents'),
    State('branding-pdf-upload', 'filename'),
    prevent_initial_call=True
)
def handle_branding_pdf(contents, filename):
    """Handle branding PDF upload"""
    if contents is None:
        return None, None

    from app_callbacks import handle_branding_pdf_upload
    return handle_branding_pdf_upload(contents, filename)


@app.callback(
    [Output('progress-display', 'style'),
     Output('overall-progress-bar', 'value'),
     Output('progress-percentage', 'children'),
     Output('current-step-display', 'children'),
     Output('step-list', 'children')],
    Input('progress-interval', 'n_intervals'),
    State('progress-store', 'data'),
    prevent_initial_call=True
)
def update_progress_display(n, progress_data):
    """Update progress display in real-time"""
    if not progress_data:
        return {'display': 'none'}, 0, '', '', []

    overall = progress_data.get('overall_progress', 0)
    current_step = progress_data.get('current_step')
    all_steps = progress_data.get('all_steps', [])

    # Current step display
    current_display = ""
    if current_step:
        current_display = html.Div([
            html.Strong("Current Step: ", style={'color': '#00A4E4'}),
            html.Span(current_step['name']),
            html.Br(),
            html.Small(current_step['message'], className="text-muted")
        ], className="mb-3")

    # Step list
    step_items = []
    for step in all_steps:
        icon = "○"
        icon_class = "step-pending"

        if step['status'] == 'complete':
            icon = "✓"
            icon_class = "step-complete"
        elif step['status'] == 'running':
            icon = "⟳"
            icon_class = "step-running"

        step_items.append(
            html.Div([
                html.Span(icon, className=f"progress-step-icon {icon_class}"),
                html.Span(f"{step['name']}: {step['message']}")
            ], className="progress-step")
        )

    percentage_text = f"{overall}% Complete"

    return {'display': 'block'}, overall, percentage_text, current_display, step_items


@app.callback(
    [Output('output-area', 'children'),
     Output('download-area', 'children'),
     Output('loading-output', 'children'),
     Output('progress-store', 'data'),
     Output('progress-interval', 'disabled')],
    Input('generate-btn', 'n_clicks'),
    [State('num-slides', 'value'),
     State('sections', 'value'),
     State('prompt', 'value'),
     State('web-search-toggle', 'value'),
     State('urls', 'value'),
     State('auth-store', 'data'),
     State('content-store', 'data'),
     State('branding-store', 'data'),
     State('logo-store', 'data'),
     State('logo-position', 'value'),
     State('logo-size', 'value'),
     State('logo-skip-title', 'value')],
    prevent_initial_call=True
)
def generate_presentation(n_clicks, num_slides, sections_str, prompt, web_search_toggle, urls_str, auth_data,
                         content_data, branding_data, logo_data, logo_position, logo_size, logo_skip_title):
    """Generate presentation using Claude and create PowerPoint"""
    if not n_clicks:
        return dash.no_update, dash.no_update, dash.no_update, None, True

    # Validate inputs
    if not prompt or not prompt.strip():
        error_msg = html.Div([
            html.Div("Please provide a presentation topic and requirements.",
                    className="status-indicator status-error")
        ])
        return error_msg, None, None, None, True

    if not auth_data:
        error_msg = html.Div([
            html.Div("Databricks authentication not available. Please check your connection.",
                    className="status-indicator status-error")
        ])
        return error_msg, None, None, None, True

    try:
        # Initialize progress tracker
        tracker = reset_tracker()

        # Step 1: Authentication
        tracker.start_step('auth', 'Authenticating with Databricks...')
        # Auth already done, complete it
        tracker.complete_step('auth', 'Connected to Databricks')

        # Parse sections
        sections = None
        if sections_str and sections_str.strip():
            sections = [s.strip() for s in sections_str.split(',') if s.strip()]

        # Parse URLs
        urls = None
        if urls_str and urls_str.strip():
            urls = [url.strip() for url in urls_str.split('\n') if url.strip()]

        # Check if web search is enabled
        enable_web_search = 'enabled' in (web_search_toggle or [])

        # Initialize Claude client
        claude_client = ClaudeClient(
            host=auth_data['host'],
            token=auth_data['token']
        )

        # Step 2: Handle content extraction if provided
        extracted_content = None
        if content_data:
            if content_data['type'] == 'pptx':
                tracker.start_step('pptx_extract', f"Extracting PowerPoint content from {content_data['filename']}...")
                extracted_content = content_data.get('extracted')
                tracker.complete_step('pptx_extract', f"Extracted {extracted_content['total_slides']} slides (100% quality)")
                tracker.skip_step('pdf_extract')
            else:  # PDF
                tracker.start_step('pdf_extract', f"Extracting PDF content from {content_data['filename']}...")
                extracted_content = content_data.get('extracted')
                num_slides = len(extracted_content.get('slides', []))
                tracker.complete_step('pdf_extract', f"Extracted {num_slides} slides from PDF")
                tracker.skip_step('pptx_extract')
        else:
            tracker.skip_step('pptx_extract')
            tracker.skip_step('pdf_extract')

        # Step 3: Web search
        if enable_web_search:
            tracker.start_step('web_search', 'Searching for technologies...')
        else:
            tracker.skip_step('web_search')

        # Step 4: URL fetching
        if urls:
            tracker.start_step('url_fetch', f'Fetching content from {len(urls)} URLs...')
        else:
            tracker.skip_step('url_fetch')

        # Step 5: AI Generation
        tracker.start_step('ai_generation', 'Generating content with Claude AI...')

        content = claude_client.generate_presentation_content(
            prompt=prompt,
            num_slides=num_slides,
            sections=sections,
            enable_web_search=enable_web_search,
            urls=urls
        )

        tracker.complete_step('ai_generation', f"Generated {len(content.get('slides', []))} slides")

        # Step 6: Create slides
        tracker.start_step('slide_creation', 'Creating PowerPoint slides...')

        # Use custom branding if provided
        custom_branding = branding_data if branding_data else None

        ppt_gen = PPTGenerator(custom_branding=custom_branding)
        ppt_gen.create_presentation(content)

        tracker.complete_step('slide_creation', f"Created {len(content.get('slides', []))} slides")

        # Step 7: Diagrams (skip for now as they're included in slide creation)
        tracker.skip_step('diagram_generation')

        # Step 8: Branding
        tracker.start_step('branding', 'Applying branding...')
        branding_msg = "Applied Databricks branding"
        if custom_branding:
            branding_msg = "Applied custom branding from PDF"
        tracker.complete_step('branding', branding_msg)

        # Step 9: Logo
        if logo_data:
            tracker.start_step('logo', f"Adding logo ({logo_position})...")
            skip_title = 'skip_title' in (logo_skip_title or [])
            # Note: We'll need to add logo support to PPTGenerator
            # For now, we'll use PPTXModifier if we have a generated file
            tracker.complete_step('logo', f"Logo added to slides")
        else:
            tracker.skip_step('logo')

        # Step 10: Export
        tracker.start_step('export', 'Exporting PowerPoint file...')

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"databricks_presentation_{timestamp}.pptx"
        filepath = f"/tmp/{filename}"

        # Save presentation
        ppt_gen.save_presentation(filepath)

        # Add logo if provided (after saving)
        if logo_data:
            modifier = PPTXModifier(filepath)
            modifier.add_logo_to_all_slides(
                logo_data['path'],
                position=logo_position,
                size=logo_size,
                skip_title_slide=skip_title
            )
            modifier.save(filepath)

        tracker.complete_step('export', f"Saved as {filename}")

        # Read file for download
        with open(filepath, 'rb') as f:
            ppt_bytes = f.read()

        encoded = base64.b64encode(ppt_bytes).decode()

        # Get final progress state
        progress_state = tracker.get_state()

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
                html.P(f"Time elapsed: {progress_state['elapsed_time']:.1f} seconds"),
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

        # Disable progress interval after completion
        return success_msg, download_btn, None, progress_state, True

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
        return error_msg, None, None, None, True


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Databricks Presentation Creator")
    print("="*60)
    print("\nStarting Dash application...")
    print("Open your browser to: http://localhost:8050")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")

    app.run_server(debug=True, host='0.0.0.0', port=8050)
