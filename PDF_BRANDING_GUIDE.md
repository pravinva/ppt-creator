# PDF Branding & Content Extraction - Feature Guide

## Overview

The Databricks Presentation Creator now supports three powerful PDF-related features:

1. **Content PDF Upload** - Convert existing PDFs to PowerPoint
2. **Branding PDF Upload** - Extract visual branding from sample PDFs
3. **Custom Logo Upload** - Add customer/partner logos to presentations

## Features

### 1. Content PDF to PowerPoint Conversion

**Use Case**: You have a PDF document (whitepaper, report, proposal) that you want to convert to a PowerPoint presentation.

**How It Works**:
- Upload a source PDF file
- The system extracts:
  - Title from first page
  - Headings (identified by larger font sizes)
  - Bullet points (•, -, *, numbered lists)
  - Paragraphs and text blocks
  - Images (preserved where possible)
- Content is automatically structured into slides
- You can modify the extracted content using prompts

**Example Workflow**:
```
1. Upload PDF: "Q4_Business_Report.pdf"
2. System extracts 8 slides of content
3. Prompt: "Make it more customer-facing, add executive summary slide,
   remove technical jargon, emphasize ROI points"
4. Generate modified PowerPoint
```

**Supported PDF Types**:
- Business reports and whitepapers
- Proposal documents
- Technical documentation
- Slide deck PDFs (converted back to editable)
- Research papers

### 2. Branding Extraction from PDF

**Use Case**: You have a customer's branded document and want to match their visual style.

**What's Extracted**:
- **Colors**:
  - Primary color (main brand color)
  - Secondary color (supporting color)
  - Accent color (highlights)
  - Text color
  - Background color

- **Fonts**:
  - Font families used
  - Font sizes (title, heading, body)

- **Layout Patterns**:
  - Margins and spacing
  - Visual hierarchy

**How To Use**:
1. Upload a sample PDF with the target branding
2. System analyzes first 3 pages
3. Extracts color palette and typography
4. Applies to generated presentation

**Example**:
```
Input PDF: Acme_Corp_Deck.pdf
Extracted Branding:
  - Primary: #1E88E5 (Blue)
  - Secondary: #424242 (Dark Gray)
  - Accent: #FFC107 (Amber)
  - Fonts: Montserrat, Open Sans
  - Title: 42pt, Heading: 32pt, Body: 18pt
```

### 3. Customer Logo Upload

**Use Case**: Co-brand presentations with customer or partner logos.

**Features**:
- Upload logo images (PNG, JPG, SVG)
- Automatic placement options:
  - Top-right corner
  - Bottom-right corner
  - Title slide only
  - All slides
  - Custom position

- Logo alongside Databricks branding
- Automatic sizing and positioning
- Maintains aspect ratio

**Supported Formats**:
- PNG (recommended - transparent background)
- JPG/JPEG
- SVG (vector graphics)

**Best Practices**:
- Use high-resolution logos (300 DPI minimum)
- Transparent backgrounds (PNG) work best
- Square or horizontal logos preferred
- Keep file size under 5MB

## Complete Workflow Examples

### Example 1: Customer-Branded Technical Presentation

**Scenario**: Create a Databricks migration presentation for Acme Corp

**Steps**:
1. **Upload Branding PDF**: `Acme_Corp_Template.pdf`
   - Extracts Acme's blue/gray color scheme
   - Montserrat font family

2. **Upload Customer Logo**: `Acme_Logo.png`
   - Placed in top-right corner

3. **Enter Prompt**:
   ```
   Create a presentation about migrating from Snowflake to Databricks
   for Acme Corp. Include TCO analysis, migration timeline, and
   architecture diagrams. Emphasize cost savings and performance.
   ```

4. **Configure**:
   - Slides: 10
   - Sections: Executive Summary, Migration Approach, Architecture, Timeline, ROI
   - Web Search: Enabled (for latest Databricks features)

5. **Result**:
   - 10-slide deck with Acme's branding
   - Acme logo on every slide
   - Databricks + Acme co-branding
   - Custom color scheme
   - Professional and on-brand

### Example 2: Converting PDF Report to Presentation

**Scenario**: Transform a 20-page PDF report into a concise presentation

**Steps**:
1. **Upload Content PDF**: `Annual_Data_Platform_Report.pdf`
   - System extracts 15 potential slides

2. **Review Extraction**:
   - Shows summary of extracted content
   - 15 slides identified from headings and bullets

3. **Modify with Prompt**:
   ```
   Condense to 8 slides focused on key findings and recommendations.
   Add an executive summary slide. Make language less technical.
   Emphasize action items and next steps.
   ```

4. **Generate**:
   - AI refines and condenses content
   - Creates 8 focused slides
   - Maintains Databricks branding

5. **Result**:
   - Clean, focused presentation
   - Key insights highlighted
   - Ready for stakeholder review

### Example 3: Multi-Brand Co-Presentation

**Scenario**: Joint presentation with partner company

**Steps**:
1. **Upload Partner Branding**: `Partner_Brand_Guide.pdf`
   - Extracts partner colors and fonts

2. **Upload Both Logos**:
   - Databricks logo (left)
   - Partner logo (right)

3. **Hybrid Branding**:
   - Merge Databricks red with partner colors
   - Use complementary fonts
   - Co-branded title slide

4. **Generate Presentation**:
   - Professional co-branded deck
   - Both companies represented
   - Unified visual identity

## Technical Implementation

### PDF Content Extraction

```python
from pdf_content_extractor import PDFContentExtractor

extractor = PDFContentExtractor()
content = extractor.extract_content("document.pdf")

# Returns:
{
  "title": "Document Title",
  "slides": [
    {
      "title": "Slide Title",
      "content": ["Bullet 1", "Bullet 2", ...],
      "section": "Section Name",
      "diagram_type": "none",
      "diagram_description": None
    },
    ...
  ]
}
```

### Branding Extraction

```python
from pdf_branding_analyzer import BrandingExtractor

extractor = BrandingExtractor()
branding = extractor.analyze_pdf("sample.pdf")

# Returns:
{
  "primary_color": (30, 136, 229),  # RGB tuple
  "secondary_color": (66, 66, 66),
  "accent_color": (255, 193, 7),
  "fonts": ["Montserrat", "Open Sans"],
  "font_sizes": {
    "title": 42,
    "heading": 32,
    "body": 18
  }
}
```

### PowerPoint Generation with Custom Branding

```python
from ppt_generator import PPTGenerator

# With custom branding
ppt_gen = PPTGenerator(custom_branding=branding)
ppt_gen.create_presentation(content)
ppt_gen.save_presentation("output.pptx")
```

## UI Components

### Content PDF Upload

```
┌─────────────────────────────────────────┐
│ Source PDF for Content (Optional)      │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  📄 Upload PDF Content            │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ✓ Content extracted from report.pdf  │
│    Found 12 potential slides            │
└─────────────────────────────────────────┘
```

### Branding PDF Upload

```
┌─────────────────────────────────────────┐
│ Branding PDF (Optional)                 │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  🎨 Upload Branding Sample        │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ✓ Branding extracted from template.pdf│
│    [View branding details ▼]            │
│    Primary: #1E88E5                     │
│    Fonts: Montserrat, Open Sans         │
└─────────────────────────────────────────┘
```

### Logo Upload

```
┌─────────────────────────────────────────┐
│ Customer Logo (Optional)                │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  🏢 Upload Customer Logo          │ │
│  └───────────────────────────────────┘ │
│                                         │
│  Logo Placement: [Top Right ▼]         │
│  □ Title slide only                    │
│  ✓ All slides                          │
│                                         │
│  ✓ Logo uploaded: acme_logo.png        │
│    Size: 245KB, Dimensions: 500x500     │
└─────────────────────────────────────────┘
```

## Configuration Options

### Branding Mode

- **Databricks Only** (default)
- **Custom Only** (from uploaded PDF)
- **Hybrid** (merge Databricks + custom)

### Logo Placement

- Top-left corner
- Top-right corner (default)
- Bottom-left corner
- Bottom-right corner
- Title slide only
- Content slides only
- All slides

### Content Modification

When uploading a content PDF, you can:
- **Keep original structure** - Minimal changes
- **Moderate editing** - Clean up and refine
- **Major restructuring** - Complete transformation
- **Custom prompt** - Specific modifications

## Best Practices

### For Content PDFs

1. **Use Clean PDFs**: PDFs with clear structure extract better
2. **Check Extraction**: Review the extracted slide count before generating
3. **Provide Clear Prompts**: Be specific about modifications needed
4. **Iterate**: Generate, review, refine with new prompts

### For Branding PDFs

1. **Use Recent Materials**: Ensure branding is current
2. **Multiple Pages**: Upload multi-page PDFs for better analysis
3. **Consistent Formatting**: PDFs with consistent styling extract better
4. **Review Extraction**: Check extracted colors and fonts match expectations

### For Logos

1. **High Resolution**: Use 300 DPI or higher
2. **Transparent Backgrounds**: PNG format recommended
3. **Proper Sizing**: Logos should be 500x500 to 1000x1000 pixels
4. **Color Mode**: RGB color mode for digital presentations

## Limitations & Considerations

### PDF Content Extraction

- **Complex Layouts**: Multi-column layouts may not extract perfectly
- **Images**: Image extraction is basic, may need manual adjustment
- **Tables**: Complex tables may not convert well
- **Formatting**: Some formatting may be lost in conversion

### Branding Extraction

- **Color Accuracy**: Colors are estimated, may need manual adjustment
- **Font Matching**: Exact fonts may not be available, similar fonts substituted
- **Limited Analysis**: Analyzes first 3 pages only
- **PDF Quality**: Poor quality PDFs yield poor extraction

### Logo Upload

- **File Size**: Maximum 10MB per logo
- **Formats**: Limited to PNG, JPG, SVG
- **Positioning**: Automated positioning may need manual adjustment
- **Resolution**: Low-res logos may appear pixelated

## Troubleshooting

### "Failed to extract content from PDF"

**Solutions**:
- Ensure PDF is not password-protected
- Try a different PDF or export with different settings
- Check PDF is not scanned image-only (needs text layer)

### "Branding colors look wrong"

**Solutions**:
- Try a PDF with more consistent branding
- Manually specify colors in future update
- Use hybrid mode to mix with Databricks defaults

### "Logo appears too large/small"

**Solutions**:
- Upload logo with different dimensions
- Use square or horizontal logo format
- Resize logo before uploading

## Future Enhancements

Planned features:
- [ ] Manual color picker for branding
- [ ] Logo size and position customization
- [ ] Template library with preset brandings
- [ ] Batch PDF processing
- [ ] Advanced table conversion
- [ ] Chart and diagram extraction
- [ ] Multiple logo support (co-branding)
- [ ] Brand kit upload (logo + colors + fonts in one package)

## API Reference

### BrandingExtractor

```python
class BrandingExtractor:
    def analyze_pdf(pdf_path: str) -> Dict[str, Any]
    def get_branding_summary(branding: Dict) -> str
    def merge_with_databricks_branding(custom: Dict) -> Dict
```

### PDFContentExtractor

```python
class PDFContentExtractor:
    def extract_content(pdf_path: str) -> Dict[str, Any]
    def merge_with_prompt_modifications(content: Dict, prompt: str) -> str
```

### PPTGenerator

```python
class PPTGenerator:
    def __init__(custom_branding: Optional[Dict] = None)
    def create_presentation(content: Dict) -> Presentation
    def add_logo(logo_path: str, position: str = "top-right")
    def save_presentation(filepath: str)
```

---

**Version**: 3.0
**Last Updated**: 2025-11-15
**Status**: Ready for Testing
