"""
Professional Agentic AI Architecture Generator - Dash Web App
Complete GUI for generating professional diagrams and presentations
NO CODE EDITING REQUIRED - Everything configurable through the web interface
"""
import dash
from dash import dcc, html, Input, Output, State, ALL, ctx, MATCH
import dash_bootstrap_components as dbc
from professional_agentic_ai_generator import ProfessionalAgenticAIGenerator
from agentic_ai_pptx_generator import AgenticAIPPTXGenerator
import base64
import os
from datetime import datetime
import json

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Professional Agentic AI Generator"

# Available icons for dropdown
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
    {'label': 'Default (Databricks Logo)', 'value': 'default'},
]

def create_component_row(phase, index, default_name="", default_icon="default"):
    """Create a component input row for journey phases"""
    return dbc.Row([
        dbc.Col([
            dbc.Input(
                id={'type': f'phase{phase}-comp-name', 'index': index},
                value=default_name,
                placeholder="Component name",
                type="text"
            ),
        ], width=7),
        dbc.Col([
            dcc.Dropdown(
                id={'type': f'phase{phase}-comp-icon', 'index': index},
                options=AVAILABLE_ICONS,
                value=default_icon,
                clearable=False
            ),
        ], width=5),
    ], className="mb-2")


def create_architecture_component_row(comp_type, index, default_name="", default_icon="default"):
    """Create a component input row for architecture"""
    return dbc.Row([
        dbc.Col([
            dbc.Input(
                id={'type': f'{comp_type}-name', 'index': index},
                value=default_name,
                placeholder="Component name",
                type="text"
            ),
        ], width=7),
        dbc.Col([
            dcc.Dropdown(
                id={'type': f'{comp_type}-icon', 'index': index},
                options=AVAILABLE_ICONS,
                value=default_icon,
                clearable=False
            ),
        ], width=5),
    ], className="mb-2")


# App Layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("🎨 Professional Agentic AI Architecture Generator",
                   className="text-center mt-4 mb-2",
                   style={'color': '#1B3139'}),
            html.P("Create professional diagrams and presentations for ANY company",
                  className="text-center text-muted mb-4"),
            html.P("✓ Professional swim lanes  ✓ Real arrows  ✓ Databricks 2025 style  ✓ No code required",
                  className="text-center text-muted mb-4", style={'fontSize': '14px'}),
        ])
    ]),

    # Tabs for different sections
    dbc.Tabs([
        # Tab 1: Company & Journey Configuration
        dbc.Tab(label="1. Journey Configuration", tab_id="tab-1", children=[
            dbc.Container([
                html.H3("Company Information", className="mt-4 mb-3"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Company Name *", style={'fontWeight': 'bold'}),
                        dbc.Input(id="company-name", placeholder="e.g., Energy Australia", type="text", value="Energy Australia"),
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Subtitle", style={'fontWeight': 'bold'}),
                        dbc.Input(id="company-subtitle", placeholder="e.g., Agentic AI Transformation Roadmap", type="text",
                                 value="Agentic AI Transformation Roadmap"),
                    ], width=6),
                ]),

                html.Hr(className="my-4"),

                html.H3("Journey Phases (4 Phases)", className="mb-3"),
                html.P("Configure each phase of the Agentic AI journey", className="text-muted"),

                # Phase 1
                html.Div([
                    html.H5("Phase 1: Traditional", className="mt-3", style={'color': '#666'}),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Phase Title"),
                            dbc.Input(id="phase1-title", value="Traditional Analytics", type="text"),
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Timeline"),
                            dbc.Input(id="phase1-timeline", value="Current State", type="text"),
                        ], width=6),
                    ]),
                    html.Div(id="phase1-components", children=[
                        create_component_row(1, 0, "Historical Data", "delta_lake"),
                        create_component_row(1, 1, "BI Dashboards", "tableau"),
                        create_component_row(1, 2, "Basic ML", "mlflow"),
                    ]),
                ], style={'background-color': '#f8f9fa', 'padding': '15px', 'border-radius': '5px', 'margin-bottom': '15px'}),

                # Phase 2
                html.Div([
                    html.H5("Phase 2: Predictive AI", className="mt-3", style={'color': '#1B5162'}),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Phase Title"),
                            dbc.Input(id="phase2-title", value="Predictive AI", type="text"),
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Timeline"),
                            dbc.Input(id="phase2-timeline", value="Q1-Q2 2025", type="text"),
                        ], width=6),
                    ]),
                    html.Div(id="phase2-components", children=[
                        create_component_row(2, 0, "Delta Lake", "delta_lake"),
                        create_component_row(2, 1, "MLflow", "mlflow"),
                        create_component_row(2, 2, "Model Serving", "workflows"),
                    ]),
                ], style={'background-color': '#f0f8ff', 'padding': '15px', 'border-radius': '5px', 'margin-bottom': '15px'}),

                # Phase 3
                html.Div([
                    html.H5("Phase 3: Augmented AI", className="mt-3", style={'color': '#618794'}),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Phase Title"),
                            dbc.Input(id="phase3-title", value="Augmented AI", type="text"),
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Timeline"),
                            dbc.Input(id="phase3-timeline", value="Q3-Q4 2025", type="text"),
                        ], width=6),
                    ]),
                    html.Div(id="phase3-components", children=[
                        create_component_row(3, 0, "Unity Catalog", "unity_catalog"),
                        create_component_row(3, 1, "Mosaic AI", "mosaic_ai"),
                        create_component_row(3, 2, "GenAI Chatbot", "mosaic_ai"),
                    ]),
                ], style={'background-color': '#f0ffff', 'padding': '15px', 'border-radius': '5px', 'margin-bottom': '15px'}),

                # Phase 4
                html.Div([
                    html.H5("Phase 4: Agentic AI", className="mt-3", style={'color': '#FF3621'}),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Phase Title"),
                            dbc.Input(id="phase4-title", value="Agentic AI", type="text"),
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Timeline"),
                            dbc.Input(id="phase4-timeline", value="2026", type="text"),
                        ], width=6),
                    ]),
                    html.Div(id="phase4-components", children=[
                        create_component_row(4, 0, "AI Agents", "mosaic_ai"),
                        create_component_row(4, 1, "MCP Protocol", "workflows"),
                        create_component_row(4, 2, "Autonomous Systems", "mosaic_ai"),
                    ]),
                ], style={'background-color': '#fff5f5', 'padding': '15px', 'border-radius': '5px', 'margin-bottom': '15px'}),

            ], className="mt-3"),
        ]),

        # Tab 2: Architecture Configuration
        dbc.Tab(label="2. Architecture Configuration", tab_id="tab-2", children=[
            dbc.Container([
                html.H3("Platform Architecture", className="mt-4 mb-3"),
                html.P("Configure the 4-lane architecture: Data Sources → Platform → AI Agents → Applications",
                      className="text-muted"),

                # Data Sources
                html.Div([
                    html.H5("Data Sources", className="mt-3"),
                    html.Div(id="data-sources", children=[
                        create_architecture_component_row("source", 0, "Smart Meters", "kafka"),
                        create_architecture_component_row("source", 1, "CRM System", "azure_blob"),
                        create_architecture_component_row("source", 2, "Cloud Storage", "s3"),
                    ]),
                ], style={'background-color': '#f8f9fa', 'padding': '15px', 'border-radius': '5px', 'margin-bottom': '15px'}),

                # Platform Components
                html.Div([
                    html.H5("Databricks Platform Components", className="mt-3"),
                    html.Div(id="platform-components", children=[
                        create_architecture_component_row("platform", 0, "AutoLoader", "autoloader"),
                        create_architecture_component_row("platform", 1, "Delta Lake", "delta_lake"),
                        create_architecture_component_row("platform", 2, "Unity Catalog", "unity_catalog"),
                        create_architecture_component_row("platform", 3, "Mosaic AI", "mosaic_ai"),
                    ]),
                ], style={'background-color': '#f0f8ff', 'padding': '15px', 'border-radius': '5px', 'margin-bottom': '15px'}),

                # AI Agents
                html.Div([
                    html.H5("AI Agents", className="mt-3"),
                    html.Div(id="ai-agents", children=[
                        create_architecture_component_row("agent", 0, "Customer Service Agent", "mosaic_ai"),
                        create_architecture_component_row("agent", 1, "Operations Agent", "mosaic_ai"),
                        create_architecture_component_row("agent", 2, "Analytics Agent", "mosaic_ai"),
                    ]),
                ], style={'background-color': '#fff5f5', 'padding': '15px', 'border-radius': '5px', 'margin-bottom': '15px'}),

                # Applications
                html.Div([
                    html.H5("Applications", className="mt-3"),
                    html.Div(id="applications", children=[
                        create_architecture_component_row("app", 0, "Web Portal", "tableau"),
                        create_architecture_component_row("app", 1, "Mobile App", "powerbi"),
                    ]),
                ], style={'background-color': '#f8f9fa', 'padding': '15px', 'border-radius': '5px', 'margin-bottom': '15px'}),

            ], className="mt-3"),
        ]),

        # Tab 3: Generate & Download
        dbc.Tab(label="3. Generate & Download", tab_id="tab-3", children=[
            dbc.Container([
                html.H3("Generate Professional Diagrams & Presentation", className="mt-4 mb-3"),

                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H5("📊 Journey Diagram", className="card-title"),
                                html.P("4-phase journey with swim lanes and arrows", className="card-text"),
                                dbc.Button("Generate Journey Diagram", id="generate-journey", color="primary", className="w-100"),
                                html.Div(id="journey-status", className="mt-2"),
                                html.Div(id="journey-preview", className="mt-3"),
                            ])
                        ], className="mb-3"),
                    ], width=6),

                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H5("🏗️ Architecture Diagram", className="card-title"),
                                html.P("Full platform architecture with swim lanes", className="card-text"),
                                dbc.Button("Generate Architecture Diagram", id="generate-architecture", color="primary", className="w-100"),
                                html.Div(id="architecture-status", className="mt-2"),
                                html.Div(id="architecture-preview", className="mt-3"),
                            ])
                        ], className="mb-3"),
                    ], width=6),
                ]),

                html.Hr(className="my-4"),

                dbc.Card([
                    dbc.CardBody([
                        html.H5("📄 Complete PowerPoint Presentation", className="card-title"),
                        html.P("Generate a complete presentation with both diagrams, business case, ROI, and timeline",
                              className="card-text"),
                        dbc.Button("Generate Complete Presentation", id="generate-pptx", color="success", size="lg", className="w-100"),
                        html.Div(id="pptx-status", className="mt-3"),
                    ])
                ]),

                html.Hr(className="my-4"),

                html.H4("Download Files", className="mt-4 mb-3"),
                html.Div(id="download-links"),

            ], className="mt-3 mb-5"),
        ]),

        # Tab 4: Help & Examples
        dbc.Tab(label="Help & Examples", tab_id="tab-4", children=[
            dbc.Container([
                html.H3("How to Use", className="mt-4 mb-3"),

                dbc.Alert([
                    html.H5("Quick Start Guide", className="alert-heading"),
                    html.Hr(),
                    html.P("1️⃣ Go to 'Journey Configuration' and enter your company name and journey phases"),
                    html.P("2️⃣ Go to 'Architecture Configuration' and configure your platform components"),
                    html.P("3️⃣ Go to 'Generate & Download' and click the generate buttons"),
                    html.P("4️⃣ Download your professional diagrams and presentation!"),
                ], color="info"),

                html.H4("What Gets Generated", className="mt-4 mb-3"),
                html.Ul([
                    html.Li("📊 Journey Diagram: Shows 4-phase transformation"),
                    html.Li("🏗️ Architecture Diagram: Shows platform layers"),
                    html.Li("📄 PowerPoint: Complete professional presentation"),
                    html.Li("✓ Professional swim-lane layout"),
                    html.Li("✓ Real arrows with arrowheads"),
                    html.Li("✓ Authentic Databricks 112x112 icons"),
                    html.Li("✓ Modern 2025 Databricks styling"),
                ]),

                html.H4("Available Icons", className="mt-4 mb-3"),
                dbc.Row([
                    dbc.Col([
                        html.H6("Product Icons"),
                        html.Ul([
                            html.Li("Databricks SQL"),
                            html.Li("Delta Lake"),
                            html.Li("AutoLoader"),
                            html.Li("MLflow"),
                            html.Li("Unity Catalog"),
                            html.Li("Mosaic AI"),
                            html.Li("Feature Store"),
                            html.Li("Workflows"),
                        ])
                    ], width=4),
                    dbc.Col([
                        html.H6("Cloud Services"),
                        html.Ul([
                            html.Li("AWS S3"),
                            html.Li("Azure Blob Storage"),
                            html.Li("Apache Kafka"),
                        ])
                    ], width=4),
                    dbc.Col([
                        html.H6("BI Tools"),
                        html.Ul([
                            html.Li("Tableau"),
                            html.Li("Power BI"),
                            html.Li("Default (Databricks logo)"),
                        ])
                    ], width=4),
                ]),

            ], className="mt-3 mb-5"),
        ]),
    ], id="tabs", active_tab="tab-1"),

    # Hidden div to store generated file paths
    dcc.Store(id='generated-files', data={'journey': None, 'architecture': None, 'pptx': None}),

], fluid=True, style={'maxWidth': '1400px'})


# Callback: Generate Journey Diagram
@app.callback(
    [Output('journey-status', 'children'),
     Output('journey-preview', 'children'),
     Output('generated-files', 'data', allow_duplicate=True)],
    Input('generate-journey', 'n_clicks'),
    [State('company-name', 'value'),
     State('phase1-title', 'value'),
     State('phase1-timeline', 'value'),
     State({'type': 'phase1-comp-name', 'index': ALL}, 'value'),
     State({'type': 'phase1-comp-icon', 'index': ALL}, 'value'),
     State('phase2-title', 'value'),
     State('phase2-timeline', 'value'),
     State({'type': 'phase2-comp-name', 'index': ALL}, 'value'),
     State({'type': 'phase2-comp-icon', 'index': ALL}, 'value'),
     State('phase3-title', 'value'),
     State('phase3-timeline', 'value'),
     State({'type': 'phase3-comp-name', 'index': ALL}, 'value'),
     State({'type': 'phase3-comp-icon', 'index': ALL}, 'value'),
     State('phase4-title', 'value'),
     State('phase4-timeline', 'value'),
     State({'type': 'phase4-comp-name', 'index': ALL}, 'value'),
     State({'type': 'phase4-comp-icon', 'index': ALL}, 'value'),
     State('generated-files', 'data')],
    prevent_initial_call=True
)
def generate_journey_diagram(n_clicks, company_name,
                             p1_title, p1_timeline, p1_names, p1_icons,
                             p2_title, p2_timeline, p2_names, p2_icons,
                             p3_title, p3_timeline, p3_names, p3_icons,
                             p4_title, p4_timeline, p4_names, p4_icons,
                             generated_files):
    if not n_clicks or not company_name:
        return "", "", generated_files

    try:
        # Build journey config
        journey_config = {
            "Phase 1": {
                "title": p1_title or "Traditional",
                "timeline": p1_timeline or "",
                "components": [{"name": name, "icon": icon}
                              for name, icon in zip(p1_names, p1_icons) if name]
            },
            "Phase 2": {
                "title": p2_title or "Predictive AI",
                "timeline": p2_timeline or "",
                "components": [{"name": name, "icon": icon}
                              for name, icon in zip(p2_names, p2_icons) if name]
            },
            "Phase 3": {
                "title": p3_title or "Augmented AI",
                "timeline": p3_timeline or "",
                "components": [{"name": name, "icon": icon}
                              for name, icon in zip(p3_names, p3_icons) if name]
            },
            "Phase 4": {
                "title": p4_title or "Agentic AI",
                "timeline": p4_timeline or "",
                "components": [{"name": name, "icon": icon}
                              for name, icon in zip(p4_names, p4_icons) if name]
            }
        }

        # Generate diagram
        gen = ProfessionalAgenticAIGenerator()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"journey_{company_name.replace(' ', '_')}_{timestamp}.png"
        gen.generate_journey_diagram(company_name, journey_config, filename)

        # Create preview
        with open(filename, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        preview = html.Div([
            html.H6("Preview:", className="mt-2"),
            html.Img(src=f"data:image/png;base64,{encoded}",
                    style={'max-width': '100%', 'border': '1px solid #ddd', 'border-radius': '5px'})
        ])

        # Update stored files
        generated_files['journey'] = filename

        status = dbc.Alert(f"✅ Journey diagram generated: {filename}", color="success")
        return status, preview, generated_files

    except Exception as e:
        status = dbc.Alert(f"❌ Error: {str(e)}", color="danger")
        return status, "", generated_files


# Callback: Generate Architecture Diagram
@app.callback(
    [Output('architecture-status', 'children'),
     Output('architecture-preview', 'children'),
     Output('generated-files', 'data', allow_duplicate=True)],
    Input('generate-architecture', 'n_clicks'),
    [State('company-name', 'value'),
     State({'type': 'source-name', 'index': ALL}, 'value'),
     State({'type': 'source-icon', 'index': ALL}, 'value'),
     State({'type': 'platform-name', 'index': ALL}, 'value'),
     State({'type': 'platform-icon', 'index': ALL}, 'value'),
     State({'type': 'agent-name', 'index': ALL}, 'value'),
     State({'type': 'agent-icon', 'index': ALL}, 'value'),
     State({'type': 'app-name', 'index': ALL}, 'value'),
     State({'type': 'app-icon', 'index': ALL}, 'value'),
     State('generated-files', 'data')],
    prevent_initial_call=True
)
def generate_architecture_diagram(n_clicks, company_name,
                                 source_names, source_icons,
                                 platform_names, platform_icons,
                                 agent_names, agent_icons,
                                 app_names, app_icons,
                                 generated_files):
    if not n_clicks or not company_name:
        return "", "", generated_files

    try:
        # Build architecture config
        architecture_config = {
            "data_sources": [{"name": name, "icon": icon}
                           for name, icon in zip(source_names, source_icons) if name],
            "platform_components": [{"name": name, "icon": icon}
                                   for name, icon in zip(platform_names, platform_icons) if name],
            "ai_agents": [{"name": name, "icon": icon}
                         for name, icon in zip(agent_names, agent_icons) if name],
            "applications": [{"name": name, "icon": icon}
                           for name, icon in zip(app_names, app_icons) if name]
        }

        # Generate diagram
        gen = ProfessionalAgenticAIGenerator()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"architecture_{company_name.replace(' ', '_')}_{timestamp}.png"
        gen.generate_full_architecture(company_name, architecture_config, filename)

        # Create preview
        with open(filename, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        preview = html.Div([
            html.H6("Preview:", className="mt-2"),
            html.Img(src=f"data:image/png;base64,{encoded}",
                    style={'max-width': '100%', 'border': '1px solid #ddd', 'border-radius': '5px'})
        ])

        # Update stored files
        generated_files['architecture'] = filename

        status = dbc.Alert(f"✅ Architecture diagram generated: {filename}", color="success")
        return status, preview, generated_files

    except Exception as e:
        status = dbc.Alert(f"❌ Error: {str(e)}", color="danger")
        return status, "", generated_files


# Callback: Generate PPTX
@app.callback(
    [Output('pptx-status', 'children'),
     Output('generated-files', 'data', allow_duplicate=True)],
    Input('generate-pptx', 'n_clicks'),
    [State('company-name', 'value'),
     State('company-subtitle', 'value'),
     State('generated-files', 'data')],
    prevent_initial_call=True
)
def generate_pptx(n_clicks, company_name, subtitle, generated_files):
    if not n_clicks or not company_name:
        return "", generated_files

    try:
        # Check if diagrams exist
        if not generated_files.get('journey') or not generated_files.get('architecture'):
            return dbc.Alert("⚠️ Please generate both diagrams first before creating the presentation!",
                           color="warning"), generated_files

        # Generate PPTX
        pptx_gen = AgenticAIPPTXGenerator()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{company_name.replace(' ', '_')}_Agentic_AI_{timestamp}.pptx"

        pptx_config = {
            "subtitle": subtitle or "Agentic AI Transformation Roadmap",
            "slides": [
                {
                    "type": "diagram",
                    "title": "Agentic AI Journey - 4 Phase Transformation",
                    "image": generated_files['journey'],
                    "subtitle": "Traditional → Predictive → Augmented → Agentic"
                },
                {
                    "type": "content",
                    "title": "Journey Phases",
                    "content": [
                        "• Phase 1: Traditional Analytics",
                        "  - Historical data analysis",
                        "  - Static BI dashboards",
                        "",
                        "• Phase 2: Predictive AI",
                        "  - Advanced ML models",
                        "  - Automated forecasting",
                        "",
                        "• Phase 3: Augmented AI",
                        "  - GenAI capabilities",
                        "  - Human-in-loop workflows",
                        "",
                        "• Phase 4: Agentic AI",
                        "  - Autonomous agents",
                        "  - Self-improving systems"
                    ]
                },
                {
                    "type": "diagram",
                    "title": "Complete Platform Architecture",
                    "image": generated_files['architecture'],
                    "subtitle": "End-to-end Agentic AI platform"
                },
                {
                    "type": "content",
                    "title": "Business Impact",
                    "content": [
                        "• Cost Reduction: 50-70%",
                        "• Process Automation: 70%+",
                        "• Response Time: 50% faster",
                        "• 24/7 Autonomous Operations",
                        "",
                        "• Expected ROI: 180% (3 years)",
                        "• Payback Period: 12-18 months"
                    ]
                }
            ]
        }

        pptx_gen.generate_presentation(company_name, pptx_config, filename)

        # Update stored files
        generated_files['pptx'] = filename

        status = dbc.Alert([
            html.H5("✅ PowerPoint Presentation Generated!", className="alert-heading"),
            html.Hr(),
            html.P(f"File: {filename}"),
            html.P(f"Slides: {len(pptx_config['slides']) + 1} (including title slide)"),
        ], color="success")

        return status, generated_files

    except Exception as e:
        status = dbc.Alert(f"❌ Error: {str(e)}", color="danger")
        return status, generated_files


# Callback: Update download links
@app.callback(
    Output('download-links', 'children'),
    Input('generated-files', 'data')
)
def update_download_links(generated_files):
    if not any(generated_files.values()):
        return dbc.Alert("No files generated yet. Generate diagrams and presentation above.", color="info")

    links = []

    if generated_files.get('journey'):
        with open(generated_files['journey'], 'rb') as f:
            encoded = base64.b64encode(f.read()).decode()
        links.append(dbc.Card([
            dbc.CardBody([
                html.H6("📊 Journey Diagram"),
                html.P(generated_files['journey'], className="text-muted small"),
                html.A(
                    dbc.Button("Download", color="primary", size="sm"),
                    href=f"data:image/png;base64,{encoded}",
                    download=generated_files['journey']
                )
            ])
        ], className="mb-2"))

    if generated_files.get('architecture'):
        with open(generated_files['architecture'], 'rb') as f:
            encoded = base64.b64encode(f.read()).decode()
        links.append(dbc.Card([
            dbc.CardBody([
                html.H6("🏗️ Architecture Diagram"),
                html.P(generated_files['architecture'], className="text-muted small"),
                html.A(
                    dbc.Button("Download", color="primary", size="sm"),
                    href=f"data:image/png;base64,{encoded}",
                    download=generated_files['architecture']
                )
            ])
        ], className="mb-2"))

    if generated_files.get('pptx'):
        with open(generated_files['pptx'], 'rb') as f:
            encoded = base64.b64encode(f.read()).decode()
        links.append(dbc.Card([
            dbc.CardBody([
                html.H6("📄 PowerPoint Presentation"),
                html.P(generated_files['pptx'], className="text-muted small"),
                html.A(
                    dbc.Button("Download", color="success", size="sm"),
                    href=f"data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,{encoded}",
                    download=generated_files['pptx']
                )
            ])
        ], className="mb-2"))

    return html.Div(links)


if __name__ == '__main__':
    print("=" * 80)
    print("🎨 PROFESSIONAL AGENTIC AI ARCHITECTURE GENERATOR")
    print("=" * 80)
    print("\n🌐 Starting Dash web application...")
    print("📍 Open your browser and go to: http://localhost:8050")
    print("\n✨ Features:")
    print("   • Configure company & journey phases via GUI")
    print("   • Configure architecture layers via GUI")
    print("   • Generate professional diagrams with one click")
    print("   • Generate complete PowerPoint presentations")
    print("   • Download all generated files")
    print("\n🚀 NO CODE EDITING REQUIRED - Everything in the GUI!")
    print("=" * 80)
    print("\nPress Ctrl+C to stop the server\n")

    app.run_server(debug=True, host='0.0.0.0', port=8050)
