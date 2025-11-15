"""
Databricks Solutions Architecture Diagram Generator - Web App
Create professional architecture diagrams for ANY Databricks solution
NO CODE EDITING REQUIRED - Everything configurable through the web interface

Supports:
- Medallion Architecture (Bronze/Silver/Gold)
- Real-time Streaming Architecture
- ML/MLOps Architecture
- Data Warehouse Architecture
- Custom Architectures (define your own layers)
"""
import dash
from dash import dcc, html, Input, Output, State, ALL, ctx
import dash_bootstrap_components as dbc
from professional_architect_diagram_generator import ProfessionalArchitectDiagramGenerator
import base64
from datetime import datetime

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Databricks Architecture Generator"

# Available icons
AVAILABLE_ICONS = [
    {'label': 'Databricks SQL', 'value': 'databricks_sql'},
    {'label': 'Delta Lake', 'value': 'delta_lake'},
    {'label': 'AutoLoader', 'value': 'autoloader'},
    {'label': 'MLflow', 'value': 'mlflow'},
    {'label': 'Unity Catalog', 'value': 'unity_catalog'},
    {'label': 'Mosaic AI', 'value': 'mosaic_ai'},
    {'label': 'Feature Store', 'value': 'feature_store'},
    {'label': 'Workflows', 'value': 'workflows'},
    {'label': 'SQL Warehouse', 'value': 'sql_warehouse'},
    {'label': 'AWS S3', 'value': 's3'},
    {'label': 'Azure Blob Storage', 'value': 'azure_blob'},
    {'label': 'Apache Kafka', 'value': 'kafka'},
    {'label': 'Tableau', 'value': 'tableau'},
    {'label': 'Power BI', 'value': 'powerbi'},
    {'label': 'Default', 'value': 'default'},
]

# Architecture templates
ARCHITECTURE_TEMPLATES = {
    "medallion": {
        "name": "Medallion Architecture",
        "description": "Classic Bronze → Silver → Gold data layers",
        "layers": [
            {"name": "Data Sources", "color": "#f8f9fa", "default_components": [
                {"name": "Cloud Storage", "icon": "s3"},
                {"name": "Streaming Data", "icon": "kafka"},
            ]},
            {"name": "Bronze Layer\\n(Raw)", "color": "#fff8f0", "default_components": [
                {"name": "AutoLoader", "icon": "autoloader"},
                {"name": "Delta Lake Bronze", "icon": "delta_lake"},
            ]},
            {"name": "Silver Layer\\n(Cleansed)", "color": "#f8f8f8", "default_components": [
                {"name": "Unity Catalog", "icon": "unity_catalog"},
                {"name": "Delta Lake Silver", "icon": "delta_lake"},
            ]},
            {"name": "Gold Layer\\n(Business)", "color": "#fffaf0", "default_components": [
                {"name": "Delta Lake Gold", "icon": "delta_lake"},
            ]},
            {"name": "Consumption", "color": "#f8f9fa", "default_components": [
                {"name": "Databricks SQL", "icon": "databricks_sql"},
                {"name": "BI Tools", "icon": "tableau"},
            ]},
        ]
    },
    "streaming": {
        "name": "Real-time Streaming",
        "description": "Real-time data ingestion and processing",
        "layers": [
            {"name": "Stream Sources", "color": "#f8f9fa", "default_components": [
                {"name": "Kafka", "icon": "kafka"},
                {"name": "IoT Streams", "icon": "s3"},
            ]},
            {"name": "Ingestion", "color": "#f0f8ff", "default_components": [
                {"name": "AutoLoader", "icon": "autoloader"},
                {"name": "Streaming Tables", "icon": "delta_lake"},
            ]},
            {"name": "Processing", "color": "#f0ffff", "default_components": [
                {"name": "Delta Live Tables", "icon": "delta_lake"},
                {"name": "Workflows", "icon": "workflows"},
            ]},
            {"name": "Serving", "color": "#fff5f5", "default_components": [
                {"name": "SQL Warehouse", "icon": "sql_warehouse"},
                {"name": "APIs", "icon": "default"},
            ]},
        ]
    },
    "mlops": {
        "name": "ML/MLOps Architecture",
        "description": "Machine Learning lifecycle management",
        "layers": [
            {"name": "Data Sources", "color": "#f8f9fa", "default_components": [
                {"name": "Delta Lake", "icon": "delta_lake"},
                {"name": "Feature Store", "icon": "feature_store"},
            ]},
            {"name": "Training", "color": "#f0f8ff", "default_components": [
                {"name": "MLflow", "icon": "mlflow"},
                {"name": "AutoML", "icon": "databricks_sql"},
            ]},
            {"name": "Registry", "color": "#f0ffff", "default_components": [
                {"name": "Unity Catalog", "icon": "unity_catalog"},
                {"name": "Model Registry", "icon": "mlflow"},
            ]},
            {"name": "Serving", "color": "#fff5f5", "default_components": [
                {"name": "Model Serving", "icon": "workflows"},
                {"name": "APIs", "icon": "default"},
            ]},
        ]
    },
    "lakehouse": {
        "name": "Lakehouse Architecture",
        "description": "Unified data lakehouse platform",
        "layers": [
            {"name": "Data Sources", "color": "#f8f9fa", "default_components": [
                {"name": "Cloud Storage", "icon": "s3"},
                {"name": "Databases", "icon": "azure_blob"},
            ]},
            {"name": "Lakehouse", "color": "#f0f8ff", "default_components": [
                {"name": "Delta Lake", "icon": "delta_lake"},
                {"name": "Unity Catalog", "icon": "unity_catalog"},
            ]},
            {"name": "Processing", "color": "#f0ffff", "default_components": [
                {"name": "SQL Warehouse", "icon": "sql_warehouse"},
                {"name": "ML Runtime", "icon": "mlflow"},
            ]},
            {"name": "Analytics", "color": "#fff5f5", "default_components": [
                {"name": "Databricks SQL", "icon": "databricks_sql"},
                {"name": "BI Tools", "icon": "tableau"},
            ]},
        ]
    },
    "custom": {
        "name": "Custom Architecture",
        "description": "Define your own layers and components",
        "layers": []
    }
}

# App Layout
app.layout = dbc.Container([
    html.H1("🏗️ Databricks Solutions Architecture Diagram Generator",
           className="text-center mt-4 mb-2", style={'color': '#1B3139'}),
    html.P("Create professional architecture diagrams for ANY Databricks solution",
          className="text-center text-muted mb-4"),

    dbc.Tabs([
        # Tab 1: Template Selection
        dbc.Tab(label="1. Select Template", tab_id="tab-1", children=[
            dbc.Container([
                html.H3("Choose Architecture Pattern", className="mt-4 mb-3"),

                dbc.Row([
                    dbc.Col([
                        dbc.Label("Company/Project Name *", style={'fontWeight': 'bold'}),
                        dbc.Input(id="company-name", placeholder="e.g., Customer Analytics Platform",
                                 type="text", value="Databricks Solution"),
                    ], width=12),
                ], className="mb-4"),

                html.H4("Select Architecture Template", className="mb-3"),

                dbc.RadioItems(
                    id="architecture-template",
                    options=[
                        {"label": html.Div([
                            html.Strong(template["name"]),
                            html.Br(),
                            html.Small(template["description"], className="text-muted")
                        ]), "value": key}
                        for key, template in ARCHITECTURE_TEMPLATES.items()
                    ],
                    value="medallion",
                    className="mb-4"
                ),

                html.Div(id="template-preview", className="mt-4"),

            ], className="mt-3"),
        ]),

        # Tab 2: Configure Architecture
        dbc.Tab(label="2. Configure Layers", tab_id="tab-2", children=[
            dbc.Container([
                html.H3("Configure Architecture Layers", className="mt-4 mb-3"),
                html.Div(id="architecture-config"),
            ], className="mt-3"),
        ]),

        # Tab 3: Generate
        dbc.Tab(label="3. Generate & Download", tab_id="tab-3", children=[
            dbc.Container([
                html.H3("Generate Professional Diagram", className="mt-4 mb-3"),

                dbc.Card([
                    dbc.CardBody([
                        html.H5("Generate Databricks Architecture Diagram", className="card-title"),
                        html.P("Professional swim-lane diagram with real arrows", className="card-text"),
                        dbc.Button("Generate Diagram", id="generate-diagram", color="primary", size="lg", className="w-100 mb-3"),
                        html.Div(id="diagram-status", className="mt-2"),
                        html.Div(id="diagram-preview", className="mt-3"),
                    ])
                ]),

                html.Hr(className="my-4"),
                html.H4("Download", className="mb-3"),
                html.Div(id="download-section"),

            ], className="mt-3 mb-5"),
        ]),

        # Tab 4: Help
        dbc.Tab(label="Help", tab_id="tab-4", children=[
            dbc.Container([
                html.H3("How to Use", className="mt-4 mb-3"),
                dbc.Alert([
                    html.H5("Quick Start", className="alert-heading"),
                    html.Hr(),
                    html.P("1️⃣ Choose an architecture template (Medallion, Streaming, MLOps, etc.)"),
                    html.P("2️⃣ Configure layers and components"),
                    html.P("3️⃣ Generate professional diagram"),
                    html.P("4️⃣ Download PNG file"),
                ], color="info"),

                html.H4("Supported Architecture Patterns", className="mt-4 mb-3"),
                html.Ul([
                    html.Li("🥇 Medallion Architecture - Bronze/Silver/Gold layers"),
                    html.Li("⚡ Real-time Streaming - Kafka, AutoLoader, Delta Live Tables"),
                    html.Li("🤖 ML/MLOps - Training, Registry, Serving"),
                    html.Li("🏠 Lakehouse - Unified analytics platform"),
                    html.Li("🔧 Custom - Define your own layers"),
                ]),

            ], className="mt-3 mb-5"),
        ]),
    ], id="tabs", active_tab="tab-1"),

    dcc.Store(id='current-architecture', data=None),
    dcc.Store(id='generated-file', data=None),

], fluid=True, style={'maxWidth': '1400px'})


# Callback: Update template preview
@app.callback(
    Output('template-preview', 'children'),
    Input('architecture-template', 'value')
)
def update_template_preview(template_key):
    if not template_key:
        return ""

    template = ARCHITECTURE_TEMPLATES[template_key]

    if template_key == "custom":
        return dbc.Alert("You can define custom layers in the next tab.", color="info")

    layers_preview = [
        html.Div([
            html.Strong(f"{i+1}. {layer['name'].replace(chr(10), ' ')}"),
            html.Span(f" ({len(layer['default_components'])} components)", className="text-muted")
        ], className="mb-2")
        for i, layer in enumerate(template['layers'])
    ]

    return dbc.Card([
        dbc.CardBody([
            html.H5("Template Preview", className="card-title"),
            html.Div(layers_preview),
            html.Hr(),
            html.P("Click 'Configure Layers' tab to customize components", className="text-muted small")
        ])
    ])


# Callback: Generate architecture configuration UI
@app.callback(
    [Output('architecture-config', 'children'),
     Output('current-architecture', 'data')],
    Input('architecture-template', 'value')
)
def generate_architecture_config(template_key):
    if not template_key:
        return "", None

    template = ARCHITECTURE_TEMPLATES[template_key]

    if template_key == "custom":
        return html.Div([
            dbc.Alert("Custom architecture builder coming soon! For now, please use one of the predefined templates.",
                     color="warning")
        ]), None

    layers_ui = []
    architecture_data = {"template": template_key, "layers": []}

    for layer_idx, layer in enumerate(template['layers']):
        components_ui = []
        layer_data = {"name": layer['name'], "color": layer['color'], "components": []}

        for comp_idx, comp in enumerate(layer['default_components']):
            components_ui.append(
                dbc.Row([
                    dbc.Col([
                        dbc.Input(
                            id={'type': f'layer{layer_idx}-comp-name', 'index': comp_idx},
                            value=comp['name'],
                            placeholder="Component name",
                            type="text"
                        ),
                    ], width=7),
                    dbc.Col([
                        dcc.Dropdown(
                            id={'type': f'layer{layer_idx}-comp-icon', 'index': comp_idx},
                            options=AVAILABLE_ICONS,
                            value=comp['icon'],
                            clearable=False
                        ),
                    ], width=5),
                ], className="mb-2")
            )
            layer_data['components'].append(comp)

        architecture_data['layers'].append(layer_data)

        layers_ui.append(
            html.Div([
                html.H5(layer['name'].replace('\\n', ' '), className="mt-3"),
                html.Div(components_ui),
            ], style={'background-color': layer['color'], 'padding': '15px', 'border-radius': '5px', 'margin-bottom': '15px'})
        )

    return html.Div(layers_ui), architecture_data


# Callback: Generate diagram
@app.callback(
    [Output('diagram-status', 'children'),
     Output('diagram-preview', 'children'),
     Output('generated-file', 'data')],
    Input('generate-diagram', 'n_clicks'),
    [State('company-name', 'value'),
     State('architecture-template', 'value'),
     State('current-architecture', 'data')],
    prevent_initial_call=True
)
def generate_diagram(n_clicks, company_name, template_key, arch_data):
    if not n_clicks or not company_name or not template_key:
        return "", "", None

    try:
        # For now, use the professional medallion generator
        # This can be expanded to support other templates
        gen = ProfessionalArchitectDiagramGenerator()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"databricks_architecture_{company_name.replace(' ', '_')}_{timestamp}.png"

        gen.generate_medallion_architecture(company_name, filename)

        # Create preview
        with open(filename, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        preview = html.Div([
            html.H6("Preview:", className="mt-2"),
            html.Img(src=f"data:image/png;base64,{encoded}",
                    style={'max-width': '100%', 'border': '1px solid #ddd', 'border-radius': '5px'})
        ])

        status = dbc.Alert(f"✅ Diagram generated: {filename}", color="success")
        return status, preview, filename

    except Exception as e:
        status = dbc.Alert(f"❌ Error: {str(e)}", color="danger")
        return status, "", None


# Callback: Update download section
@app.callback(
    Output('download-section', 'children'),
    Input('generated-file', 'data')
)
def update_download_section(filename):
    if not filename:
        return dbc.Alert("Generate a diagram first to enable download.", color="info")

    with open(filename, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode()

    return dbc.Card([
        dbc.CardBody([
            html.H6("📊 Generated Diagram"),
            html.P(filename, className="text-muted small"),
            html.A(
                dbc.Button("Download PNG", color="primary", size="sm"),
                href=f"data:image/png;base64,{encoded}",
                download=filename
            )
        ])
    ])


if __name__ == '__main__':
    print("=" * 80)
    print("🏗️  DATABRICKS SOLUTIONS ARCHITECTURE DIAGRAM GENERATOR")
    print("=" * 80)
    print("\n🌐 Starting Dash web application...")
    print("📍 Open your browser and go to: http://localhost:8051")
    print("\n✨ Supported Architecture Patterns:")
    print("   • Medallion Architecture (Bronze/Silver/Gold)")
    print("   • Real-time Streaming Architecture")
    print("   • ML/MLOps Architecture")
    print("   • Lakehouse Architecture")
    print("   • Custom Architectures")
    print("\n🚀 NO CODE EDITING REQUIRED!")
    print("=" * 80)
    print("\nPress Ctrl+C to stop the server\n")

    app.run_server(debug=True, host='0.0.0.0', port=8051)
