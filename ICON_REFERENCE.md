# Databricks Icon Reference

## Standard Databricks Product Icons

All standard Databricks product icons are **112x112 PNG** format.

### Icon Files (Slide 24)
Located in `databricks_assets/`:

```
template_s024_i00.png - 112x112 - Databricks product icon
template_s024_i01.png - 112x112 - Databricks product icon
template_s024_i02.png - 112x112 - Databricks product icon
template_s024_i03.png - 112x112 - Databricks product icon
template_s024_i04.png - 112x112 - Databricks product icon
template_s024_i05.png - 112x112 - Databricks product icon
template_s024_i06.png - 112x112 - Databricks product icon
template_s024_i07.png - 112x112 - Databricks product icon
template_s024_i08.png - 112x112 - Databricks product icon
template_s024_i09.png - 112x112 - Databricks product icon
template_s024_i10.png - 112x112 - Databricks product icon
template_s024_i11.png - 112x112 - Databricks product icon
template_s024_i12.png - 112x112 - Databricks product icon
template_s024_i13.png - 112x112 - Databricks product icon
```

### Icon Overview
- **File**: `template_s025_i00.png` (2048x1044)
- **Description**: Complete overview of all Databricks icons in orange
- **Use**: Reference for all available icon types

### Common Databricks Services (typical icons)
Based on text found in slides:
- **Databricks SQL**: Query and BI workloads
- **Delta Lake**: Storage layer
- **AutoLoader**: Incremental data ingestion
- **MLflow**: ML lifecycle management
- **Unity Catalog**: Unified governance
- **Mosaic AI**: AI/ML capabilities
- **Quality Monitoring**: Data quality checks

## Databricks Logos (Slide 23)

Various Databricks logo formats and sizes:

```
template_s023_i00.png - 2500x396  - Wide logo format
template_s023_i01.png - 2500x396  - Wide logo format
template_s023_i02.png - 2500x396  - Wide logo format
template_s023_i03.png - 2500x396  - Wide logo format
template_s023_i04.png - 1902x2048 - Vertical logo
template_s023_i05.png - 1902x2048 - Vertical logo
template_s023_i06.png - 1902x2048 - Vertical logo
template_s023_i07.png - 1902x2048 - Vertical logo
template_s023_i08.png - 1387x720  - Medium horizontal
template_s023_i09.png - 1387x720  - Medium horizontal
template_s023_i10.png - 1655x604  - Wide format
template_s023_i11.png - 1657x603  - Wide format
template_s023_i12.png - 1134x881  - Square-ish format
template_s023_i13.png - 1134x881  - Square-ish format
template_s023_i14.png - 1412x1268 - Large square
template_s023_i15.png - 1412x1268 - Large square
template_s023_i16.png - 246x150   - Small logo
template_s023_i17.png - 246x150   - Small logo
```

## Cloud Service Logos (Slide 26)

### Categories: Ingest, Storage, Serve

```
template_s026_i00.png - 301x180 - Cloud service
template_s026_i01.png - 421x339 - Cloud service
template_s026_i02.png - 400x400 - Cloud service (square)
template_s026_i03.png - 128x128 - Cloud service (small square)
template_s026_i04.png - 255x325 - Cloud service (vertical)
template_s026_i05.png - 36x36   - Cloud service (icon)
template_s026_i06.png - 36x36   - Cloud service (icon)
template_s026_i07.png - 36x36   - Cloud service (icon)
template_s026_i08.png - 36x36   - Cloud service (icon)
template_s026_i09.png - 70x63   - Cloud service (small)
template_s026_i10.png - 71x71   - Cloud service (small square)
template_s026_i11.png - 180x180 - Cloud service (medium square)
```

Common cloud services typically include:
- AWS S3, Glue, Kinesis, Lambda
- Azure Blob Storage, Event Hubs, Functions
- Google Cloud Storage, Pub/Sub, Cloud Functions
- Kafka, Spark, Delta Lake

## Partner Logos (Slide 27)

```
template_s027_i00.png - 301x180   - Partner logo
template_s027_i01.png - 651x125   - Partner logo (wide)
template_s027_i02.png - 1076x132  - Partner logo (very wide)
template_s027_i03.png - 360x140   - Partner logo
template_s027_i04.png - 501x140   - Partner logo
template_s027_i05.png - 554x301   - Partner logo
template_s027_i06.png - 570x140   - Partner logo
template_s027_i07.png - 979x140   - Partner logo (wide)
template_s027_i08.png - 2048x359  - Partner logo (very wide)
template_s027_i09.png - 421x339   - Partner logo (square-ish)
template_s027_i10.png - 400x400   - Partner logo (square)
template_s027_i11.png - 1364x400  - Partner logo (wide)
template_s027_i12.png - 1141x400  - Partner logo (wide)
template_s027_i13.png - 1568x400  - Partner logo (wide)
template_s027_i14.png - 1147x374  - Partner logo (wide)
template_s027_i15.png - 264x60    - Partner logo (small)
template_s027_i16.png - 220x50    - Partner logo (small)
```

Common partners include:
- Tableau, Power BI, Looker (BI tools)
- Fivetran, dbt (data integration/transformation)
- Snowflake, Redshift (data warehouses)
- Various enterprise software vendors

## Icon Usage Guidelines

### Sizing
- **Standard**: Use 112x112 as base size for product icons
- **Scaling**: Scale proportionally for diagrams
- **Consistency**: All icons in a diagram should be roughly same size
- **Hierarchy**: Only vary size to show hierarchy or importance

### Line Weight
- All icons in a single diagram must use same line weight
- Maintain consistency when mixing Databricks and third-party icons

### Color Variations
Icons are available in multiple colors:
- **Orange** (#FF3621): Primary/highlighted state
- **Navy** (#1B3139): Default state
- **Light Blue** (#618794, #1B5162): Secondary states
- **Other brand colors**: As needed for specific meanings

### In Diagrams
- Position icons above or beside text labels
- Align icons in grid layouts
- Use consistent spacing between icons
- Group related icons visually

## Example Architecture Icon Layout

```
[Ingest Layer]          [Process Layer]        [Serve Layer]
  S3/Blob     →→→      Delta Lake    →→→     Databricks SQL
  Kafka       →→→      AutoLoader            PowerBI/Tableau
  Event Hub   →→→      Unity Catalog         REST APIs

[Governance Layer - spans all]
         Unity Catalog + Quality Monitoring
```

## Python Usage Example

```python
from PIL import Image

# Load a Databricks icon
icon = Image.open('databricks_assets/template_s024_i00.png')
# Resize if needed (maintain aspect ratio)
icon = icon.resize((80, 80), Image.Resampling.LANCZOS)

# For diagrams library - you'd need to implement custom nodes
# with these icons embedded
```

## Asset Catalog

Full catalog available in: `databricks_assets/catalog.json`

This JSON file contains:
- Slide number for each asset
- Slide title/context
- Filename
- Original dimensions
- Asset type (template vs docs example)

Total assets extracted: **985 images**
- Template assets: 109
- Docs example diagrams: 876
