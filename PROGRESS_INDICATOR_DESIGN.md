# Progress Indicator Design for Presentation Generation

## User Feedback Requirement

**Need**: Real-time feedback showing what's happening during generation:
- Getting information from web/URLs
- Generating content with AI
- Creating specific slides (e.g., "Producing ZeroBus slide...")
- Generating diagrams
- Applying branding
- Finalizing presentation

**UI Elements**: Progress bar, circular meter, or step-by-step status

---

## Implementation Design

### Option 1: Step-by-Step Progress Bar (RECOMMENDED)

```
┌─────────────────────────────────────────────────────┐
│  Generating Your Presentation...                   │
│                                                     │
│  ██████████████░░░░░░░░░░░░░░  60% Complete        │
│                                                     │
│  ✓ Authenticated with Databricks                   │
│  ✓ Fetching web content...                        │
│  ⟳ Generating slides with Claude AI...            │
│  ○ Creating diagrams...                           │
│  ○ Applying branding...                           │
│  ○ Finalizing PowerPoint...                       │
└─────────────────────────────────────────────────────┘
```

**Features**:
- Linear progress bar (0-100%)
- Check marks (✓) for completed steps
- Spinner (⟳) for current step
- Empty circles (○) for pending steps
- Real-time step descriptions

### Option 2: Circular Progress Meter

```
        ┌─────────────────┐
        │                 │
        │      ⟳ 60%      │
        │                 │
        │  Creating       │
        │  Diagrams...    │
        └─────────────────┘

  Steps:
  ✓ Web Research
  ✓ AI Generation
  ⟳ Diagrams
  ○ Branding
  ○ Finalize
```

**Features**:
- Circular progress indicator
- Current step highlighted
- Percentage completion
- Step checklist below

### Option 3: Detailed Task List (Most Informative)

```
┌─────────────────────────────────────────────────────┐
│  Presentation Generation Progress                  │
├─────────────────────────────────────────────────────┤
│  1. Databricks Authentication         ✓ Done       │
│  2. Web Research                       ✓ Done       │
│     • Searching for 'genie mcp'...     ✓           │
│     • Searching for 'zerobus'...       ✓           │
│     • Fetching URL content...          ✓           │
│  3. AI Content Generation              ⟳ Running   │
│     • Generating slide structure...    ⟳ 45s       │
│  4. Slide Creation                     ○ Pending   │
│  5. Diagram Generation                 ○ Pending   │
│  6. Branding Application               ○ Pending   │
│  7. PowerPoint Export                  ○ Pending   │
└─────────────────────────────────────────────────────┘
```

**Features**:
- Detailed task breakdown
- Sub-task visibility
- Time estimates
- Most transparent

---

## Recommended: Hybrid Approach

Combine progress bar with step details:

```
┌─────────────────────────────────────────────────────┐
│  Creating Your Presentation                         │
│  ████████████░░░░░░░░░░░░░░  60%                   │
│                                                     │
│  Current Step: Generating Slides                   │
│  Processing: ZeroBus Architecture (Slide 3/7)      │
│                                                     │
│  Completed Steps:                                  │
│  ✓ Databricks authentication                       │
│  ✓ Web research (2 topics found)                   │
│  ✓ Fetched 1 URL                                   │
│  ✓ Claude AI content generation (12 seconds)       │
│                                                     │
│  In Progress:                                      │
│  ⟳ Creating slide 3: ZeroBus Architecture          │
│  ⟳ Generating medallion diagram...                 │
│                                                     │
│  Upcoming:                                         │
│  ○ Create slides 4-7                               │
│  ○ Apply Databricks branding                       │
│  ○ Generate PowerPoint file                        │
└─────────────────────────────────────────────────────┘
```

---

## Implementation Steps

### 1. Add Progress State Management

```python
# In app.py
import time
from dash import dcc

# Add progress store
dcc.Store(id='progress-store')

# Progress states
PROGRESS_STEPS = {
    'auth': {'name': 'Databricks Authentication', 'weight': 5},
    'web_search': {'name': 'Web Research', 'weight': 10},
    'url_fetch': {'name': 'URL Content Fetching', 'weight': 10},
    'pdf_extract': {'name': 'PDF Content Extraction', 'weight': 10},
    'ai_generation': {'name': 'AI Content Generation', 'weight': 30},
    'slide_creation': {'name': 'Creating Slides', 'weight': 15},
    'diagram_generation': {'name': 'Generating Diagrams', 'weight': 10},
    'branding': {'name': 'Applying Branding', 'weight': 5},
    'export': {'name': 'Exporting PowerPoint', 'weight': 5},
}
```

### 2. Update UI Components

```python
# Add progress display area
html.Div([
    html.Div(id='progress-container', style={'display': 'none'}, children=[
        html.H5("Generating Your Presentation", className="mb-3"),

        # Progress bar
        dbc.Progress(
            id='progress-bar',
            value=0,
            striped=True,
            animated=True,
            className="mb-3"
        ),

        # Current step
        html.Div(id='current-step', className="mb-3"),

        # Step details
        html.Div(id='step-details', className="mb-3"),

        # Completed steps
        html.Div([
            html.H6("Completed:", className="text-success"),
            html.Ul(id='completed-steps', className="list-unstyled")
        ]),

        # Current operations
        html.Div([
            html.H6("In Progress:", className="text-primary"),
            html.Ul(id='in-progress-steps', className="list-unstyled")
        ]),
    ])
])
```

### 3. Add Progress Updates in Callback

```python
@app.callback(
    [Output('progress-bar', 'value'),
     Output('current-step', 'children'),
     Output('completed-steps', 'children'),
     Output('in-progress-steps', 'children')],
    Input('generate-btn', 'n_clicks'),
    [State('num-slides', 'value'),
     State('prompt', 'value'),
     # ... other states
    ],
    prevent_initial_call=True
)
def generate_with_progress(n_clicks, num_slides, prompt, ...):
    """Generate presentation with progress updates"""

    # Show progress container
    progress_visible = True

    # Step 1: Authentication (5%)
    update_progress(5, 'auth', 'Authenticating with Databricks...')
    db_auth = DatabricksAuth()

    # Step 2: Web Research (15%)
    if enable_web_search:
        update_progress(15, 'web_search', f'Searching for technologies...')
        # Perform searches

    # Step 3: URL Fetching (25%)
    if urls:
        update_progress(25, 'url_fetch', f'Fetching content from {len(urls)} URLs...')
        # Fetch URLs

    # Step 4: AI Generation (55%)
    update_progress(55, 'ai_generation', 'Generating content with Claude AI...')
    content = claude_client.generate_presentation_content(...)

    # Step 5: Creating Slides (70%)
    update_progress(70, 'slide_creation', f'Creating {num_slides} slides...')
    for i, slide in enumerate(content['slides']):
        update_progress(
            70 + (i / num_slides) * 15,
            'slide_creation',
            f'Creating slide {i+1}/{num_slides}: {slide["title"]}'
        )

    # Step 6: Diagrams (85%)
    diagram_count = count_diagrams(content)
    if diagram_count > 0:
        update_progress(85, 'diagram_generation', f'Generating {diagram_count} diagrams...')
        # Generate diagrams

    # Step 7: Branding (90%)
    update_progress(90, 'branding', 'Applying Databricks branding...')
    ppt_gen = PPTGenerator(custom_branding)

    # Step 8: Export (95%)
    update_progress(95, 'export', 'Finalizing PowerPoint file...')
    ppt_gen.save_presentation(filepath)

    # Step 9: Complete (100%)
    update_progress(100, 'complete', 'Presentation ready!')

    return presentation_data
```

### 4. Use Dash Interval for Real-Time Updates

```python
# Add interval component for polling
dcc.Interval(
    id='progress-interval',
    interval=500,  # Update every 500ms
    n_intervals=0,
    disabled=True
)

# Callback to update progress display
@app.callback(
    Output('progress-display', 'children'),
    Input('progress-interval', 'n_intervals'),
    State('progress-store', 'data')
)
def update_progress_display(n, progress_data):
    """Update progress display in real-time"""
    if not progress_data:
        return None

    return create_progress_ui(progress_data)
```

---

## Specific Status Messages for Each Step

### 1. Authentication
```
⟳ Authenticating with Databricks...
✓ Connected as user@databricks.com
```

### 2. Web Research
```
⟳ Searching for 'genie mcp'...
✓ Found 3 relevant results

⟳ Searching for 'zerobus'...
✓ Found 2 relevant results
```

### 3. URL Fetching
```
⟳ Fetching content from https://databricks.com/blog/...
✓ Extracted 1,200 words

⟳ Fetching content from https://docs.databricks.com/...
✓ Extracted 800 words
```

### 4. PDF Extraction
```
⟳ Extracting content from customer_deck.pdf...
✓ Found 12 slides
✓ Extracted 450 words

⟳ Analyzing branding from sample.pdf...
✓ Detected colors: #1E88E5, #424242
✓ Detected fonts: Montserrat, Open Sans
```

### 5. AI Generation
```
⟳ Generating presentation with Claude AI...
  Processing 2,500 tokens of context...
✓ Generated 7 slides in 18 seconds
```

### 6. Slide Creation
```
⟳ Creating slide 1: ZeroBus Ingestion Overview
✓ Slide 1 complete

⟳ Creating slide 2: ZeroBus Architecture
✓ Slide 2 complete

⟳ Creating slide 3: Medallion Architecture
  ⟳ Generating medallion diagram...
✓ Slide 3 complete (with diagram)
```

### 7. Diagram Generation
```
⟳ Generating medallion architecture diagram...
✓ Created 1280x720 HD diagram

⟳ Generating architecture building blocks...
✓ Created integration flow diagram
```

### 8. Branding
```
⟳ Applying Databricks branding...
  • Setting Databricks Red (#FF3621)
  • Configuring fonts (Arial, 20-54pt)
  • Adding accent bars
✓ Branding applied to all slides
```

### 9. Export
```
⟳ Generating PowerPoint file...
  • Writing slides...
  • Embedding diagrams...
  • Finalizing...
✓ PowerPoint file created (96 KB)
```

### 10. Complete
```
✓ Presentation ready!
  • 7 slides created
  • 4 diagrams embedded
  • Databricks branding applied
  • File size: 96 KB

→ Click below to download
```

---

## Visual Design

### Colors for Status

```css
.status-pending {
    color: #999999;
    opacity: 0.5;
}

.status-in-progress {
    color: #00A4E4;  /* Databricks blue */
    animation: pulse 1.5s infinite;
}

.status-complete {
    color: #00C853;  /* Success green */
}

.status-error {
    color: #FF3621;  /* Databricks red */
}
```

### Icons

```
✓ - Complete (green)
⟳ - In Progress (blue, spinning)
○ - Pending (gray)
⚠ - Warning (orange)
✗ - Error (red)
```

---

## Benefits

1. **Transparency**: Users know exactly what's happening
2. **Trust**: Shows the system is working, not frozen
3. **Engagement**: Interesting to watch the process
4. **Debugging**: Easy to see where issues occur
5. **Time Estimation**: Users know roughly how long it takes

---

## Next Steps

1. Implement progress state management
2. Add progress UI components
3. Update generate callback with progress updates
4. Test with various scenarios
5. Add time estimates per step
6. Polish animations and transitions

---

**This will make the app feel much more professional and responsive!** 🎯
