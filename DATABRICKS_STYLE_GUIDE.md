# Databricks Architecture Diagram Style Guide

This guide documents the modern Databricks architecture diagram style extracted from official templates.

## Color Palette

### Primary Colors
```
#1B3139 - Dark Navy (near-black) - Primary text and borders
#1B5162 - Medium Blue - Secondary elements
#618794 - Light Blue - Tertiary elements
```

### Accent Colors
```
#FF3621 - Orange - Key highlights and CTAs
#FFAB00 - Yellow - Warnings or special attention
#00A972 - Green - Success states or data flow
#98102A - Red - Errors or critical items
#0078D4 - Azure Blue - Cloud services
```

### Neutral Colors
```
#FFFFFF - White - Background (always)
#F9F7F4 - Off-white - Subtle backgrounds
#EFEFEF - Light gray - Disabled states
#D9D9D9 - Gray - Borders and dividers
#B7B7B7 - Medium gray - Secondary text
#666666 - Dark gray - Supporting text
#505050 - Darker gray
#434343 - Very dark gray
```

### Special Colors
```
#D9EAD3 - Light green - Success background
```

## Typography

### Fonts
- **Primary**: DM Sans (normal weight)
- **Code**: DM Mono
- **Sizes**: 10-16pt (stick to this range)
- **Color**: #1B3139 (near-black) for most labels

### Font Guidelines
- Main font should render at roughly same size as article body font
- Make sure smallest font is readable when rendered on doc site
- Scale should be consistent throughout a given article
- Use color to imply meaning or relationships, not just decoration

## Diagram Specifications

### Size Constraints
- **Maximum**: 1000px width OR height (never exceed)
- **Scale**: Consistent throughout an article
- **Related diagrams**: Should be same width in a given article

### Background & Fill
- **Background**: Always white, NEVER transparent
- **Shape fill**: Never transparent (breaks dark mode)
- **Reasoning**: Transparent backgrounds render unreadable in dark mode

## Design Elements

### Shapes
- **Primary**: Simple rectangles
- **Sizing**: Same-sized shapes for similar concepts/objects/terms
- **Grouping**: Dotted lines or filled shapes to group related objects
- **De-emphasis**: More transparent shapes/borders/fill for less important items

### Flow & Layout
- **Primary flow**: Left-to-right (works well with slide format)
- **Alternative**: Top-down for shorter flows
- **Connectors**: Always 1px width
- **Arrows**: Use only when showing directional flow
- **Connection style**: Use purple targets when connecting shapes

### Connections
- **Width**: 1px connectors to imply connection or flow
- **Endpoints**: Arrow endpoints ONLY for flow direction
- **No arrows**: For non-directional relationships

### Icons
- **Source**: Databricks corporate icons (112x112 PNG)
- **Consistency**: All icons in diagram should use same line weight
- **Sizing**: All icons roughly same size (unless showing hierarchy)
- **Location**: Available via Digital Asset Chrome Plugin
- **Fallback**: Can borrow from internet, but maintain line weight consistency

### Alignment & Grouping
- **Vertical/Horizontal**: Always align shapes properly
- **Tools**: Use centering and alignment tools
- **Grouping**: Right-click > group for objects that move together
- **Visual grouping**: Use borders or filled shapes
- **Subtle grouping**: Dotted-line borders for visual grouping

### Titles
- **Rule**: Don't use titles in the diagram itself
- **Location**: Add descriptive title ABOVE the diagram

## Best Practices Summary

1. **Light feeling**: Use color and transparency to tell your story
2. **Don't overdo it**: Group related objects, de-emphasize some, but keep it clean
3. **Avoid bright blue**: Use Databricks Theme colors but skip the bright blue
4. **Custom colors OK**: If needed, but prefer theme colors
5. **Same throughout**: Keep scale and style consistent in article
6. **Readability first**: Ensure smallest font is readable on doc site

## Icon Categories

From the template, icons are organized into:

### Databricks Services (Slide 24)
- All 112x112 PNG format
- Available in orange (#FF3621) and other brand colors
- Includes: SQL, Delta Lake, AutoLoader, MLflow, Unity Catalog, etc.

### Cloud Service Logos (Slide 26)
Categories:
- **Ingest**: Data ingestion services
- **Storage**: Cloud storage solutions
- **Serve**: Serving and delivery services

### Partner Logos (Slide 27)
- Third-party integration logos
- Business intelligence tools
- Data platforms

## Technical Implementation Notes

### For Python/Diagrams Library
- Use PIL/Pillow for custom icon insertion
- Export at max 1000px dimension
- Ensure white background (not transparent)
- Use #1B3139 for primary shapes
- Use #FF3621 for accent/highlights
- Implement 1px stroke width for connectors

### For PowerPoint Generation
- Set slide size: 10" x 7.5" standard
- DM Sans font (install if needed)
- Apply theme colors from template
- Use layout templates from corporate deck

## Asset Locations

All extracted assets stored in:
- `databricks_assets/` - All icons and images (985 total)
- `databricks_assets/catalog.json` - Complete asset catalog
- Icon files named: `template_s{slide}_i{index}.{ext}`
- Docs examples: `docs_s{slide}_i{index}.{ext}`

## Key Template Slides

- **Slide 6**: AI Models & Tools architecture example
- **Slides 9-13**: Complete platform diagrams with icons
- **Slide 17**: Applied layout with icons (AutoLoader, SQL, Quality Monitoring)
- **Slide 19**: Federation and 3rd party integration example
- **Slide 23**: Databricks logos collection
- **Slide 24**: Databricks icons with color codes
- **Slide 25**: Icon overview in orange
- **Slide 26**: Cloud service logos
- **Slide 27**: Partner logos

## Comparison: Old vs New Style

### Old Style (AWS/Azure docs)
- Gray rectangles
- Generic service icons
- Text-heavy swimlanes
- Traditional layout

### New Style (Databricks 2025)
- Modern flat design
- Branded Databricks icons
- Clean typography (DM Sans)
- Navy + orange color scheme
- Rounded corners and shadows
- Grid-based layouts
- Professional spacing
