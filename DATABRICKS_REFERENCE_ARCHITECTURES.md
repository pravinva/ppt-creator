# Databricks Reference Architecture Patterns

This document catalogs common Databricks architecture patterns to use as references for diagram generation.

## Standard Lakehouse Architecture

### Core Swim Lanes (Left to Right)

```
SOURCE → INGEST → TRANSFORM → QUERY/PROCESS → SERVE → ANALYSIS
                    ↓
                 STORAGE (spans bottom)
```

### 1. Source Layer
**Components:**
- Enterprise Applications (Salesforce, SAP, Oracle)
- Operational Databases (PostgreSQL, MySQL, SQL Server, MongoDB)
- Streaming Sources (Kafka, Event Hub, Kinesis, Pub/Sub)
- File Systems (S3, ADLS, GCS)
- APIs and Web Services

### 2. Ingest Layer
**Components:**
- **Lakeflow Connect**: Built-in connectors for enterprise apps
- **Partner Tools**: Fivetran, Airbyte for batch ingestion
- **Structured Streaming**: For real-time event ingestion
- **AutoLoader**: Incremental file ingestion
- **COPY INTO**: Batch file loading

**Patterns:**
- Batch ETL from enterprise systems
- Streaming ingestion from event streams
- File-based ingestion from cloud storage

### 3. Transform Layer (Medallion Architecture)
**Components:**
- **Bronze Layer**: Raw data ingestion (as-is copy)
- **Silver Layer**: Cleansed, validated, enriched data
- **Gold Layer**: Aggregated, business-level data

**Technologies:**
- Delta Lake / Apache Iceberg tables
- Unity Catalog for governance
- Workflows for orchestration
- Data Quality Monitoring

### 4. Query/Process Layer
**Components:**
- **Databricks SQL**: BI and analytics queries
- **Machine Learning**: MLflow, Mosaic AI
- **Data Science Notebooks**: Interactive analysis
- **Serverless Compute**: On-demand query processing

### 5. Serve Layer
**Components:**
- **REST APIs**: Model serving, data APIs
- **BI Connectors**: JDBC/ODBC for BI tools
- **Delta Sharing**: Secure data sharing
- **Real-time Features**: Feature Store serving

### 6. Analysis Layer
**Consumer Tools:**
- **BI Tools**: Tableau, Power BI, Looker
- **SQL Clients**: DBeaver, DataGrip
- **Notebooks**: Jupyter, Databricks notebooks
- **Custom Applications**: Via APIs

### 7. Storage Layer (Foundation)
**Components:**
- **Cloud Storage**: S3, ADLS Gen2, GCS
- **Delta Lake**: ACID transactions on storage
- **Unity Catalog**: Metadata and governance
- **External Tables**: Query external data

### 8. Governance Layer (Spans All)
**Components:**
- **Unity Catalog**: Unified governance and security
- **Data Quality**: Lakehouse Monitoring
- **Lineage**: Automatic data lineage tracking
- **Access Control**: Fine-grained permissions

## Common Architecture Patterns

### Pattern 1: Real-Time Streaming Analytics

```
Streaming Sources → Kafka/Event Hub → AutoLoader/Structured Streaming
                                            ↓
                                    Delta Lake (Bronze)
                                            ↓
                                    Stream Processing (Silver)
                                            ↓
                                    Aggregations (Gold)
                                            ↓
                                    Databricks SQL + BI Tools
```

**Use Cases:**
- IoT sensor data processing
- Clickstream analytics
- Financial transaction monitoring
- Real-time dashboards

### Pattern 2: Batch ETL Data Warehouse

```
Enterprise Apps → Lakeflow Connect/Fivetran → Delta Lake Bronze
Databases                                           ↓
Files                                          Silver (Cleansed)
                                                    ↓
                                               Gold (Aggregated)
                                                    ↓
                                           Databricks SQL Warehouse
                                                    ↓
                                               BI Tools (Tableau, Power BI)
```

**Use Cases:**
- Data warehouse modernization
- Enterprise reporting
- Historical analysis
- Regulatory reporting

### Pattern 3: AI/ML Platform

```
Data Sources → Ingestion → Delta Lake (Bronze/Silver/Gold)
                                ↓
                        Feature Engineering
                                ↓
                        ML Training (MLflow)
                                ↓
                        Model Registry
                                ↓
                    Model Serving (REST APIs)
                                ↓
                        Applications
```

**Use Cases:**
- Predictive analytics
- Recommendation engines
- Fraud detection
- Customer churn prediction

### Pattern 4: Data Mesh Architecture

```
Domain 1                Domain 2                Domain 3
  |                       |                       |
  ├─ Bronze              ├─ Bronze              ├─ Bronze
  ├─ Silver              ├─ Silver              ├─ Silver
  └─ Gold                └─ Gold                └─ Gold
        \                    |                    /
         \                   |                   /
          \                  |                  /
           ──────────────────┴─────────────────
                             |
                    Unity Catalog (Central Governance)
                             |
                    Delta Sharing (Cross-domain)
```

**Use Cases:**
- Decentralized data ownership
- Domain-driven design
- Large enterprise data platforms
- Multi-tenant architectures

### Pattern 5: Lakehouse Federation

```
External Sources              Databricks Lakehouse
─────────────────             ───────────────────
Snowflake        ←→           Unity Catalog
PostgreSQL       ←→           Federation Layer
MySQL            ←→                 ↓
BigQuery         ←→           Delta Lake Tables
S3 Buckets       ←→                 ↓
                              Unified Query Layer
                                    ↓
                              BI & Applications
```

**Use Cases:**
- Multi-cloud data integration
- Hybrid data architectures
- Data product aggregation
- Unified analytics layer

### Pattern 6: Data Science & GenAI

```
Data Lake (Bronze/Silver/Gold)
        ↓
Feature Store
        ↓
    ┌───────┴───────┐
    ↓               ↓
ML Models      LLM/GenAI
(MLflow)     (Mosaic AI)
    ↓               ↓
    └───────┬───────┘
            ↓
    Model Serving
            ↓
    Applications & APIs
```

**Use Cases:**
- LLM fine-tuning
- RAG (Retrieval Augmented Generation)
- Predictive + Generative AI
- AI-powered applications

## Visual Design Guidelines for Each Pattern

### Layout
- **Horizontal Flow**: Left to right (source → consumption)
- **Vertical Layers**: Stack related components
- **Swim Lanes**: Organize by functional layer
- **Grouping**: Dotted boxes for logical groupings

### Color Coding
- **Ingest**: Light blue (#618794)
- **Storage**: Medium blue (#1B5162)
- **Processing**: Dark navy (#1B3139)
- **Governance**: Orange (#FF3621)
- **Serving**: Green (#00A972)
- **External Systems**: Gray (#666666)

### Icon Usage
- Use 112x112 Databricks icons for products
- Use cloud service logos for AWS/Azure/GCP services
- Use partner logos for third-party tools
- Keep consistent sizing within each diagram

### Connectors
- **1px solid arrows**: Data flow
- **1px dotted lines**: Loose coupling or grouping
- **Bidirectional arrows**: Federation or sync
- **Color-coded flows**: Match source/destination colors

## Common Component Combinations

### Streaming Stack
```
Kafka/Event Hub + AutoLoader + Structured Streaming + Delta Lake
```

### Batch Stack
```
Lakeflow Connect/Fivetran + Delta Lake + Workflows + SQL Warehouse
```

### ML Stack
```
Delta Lake + Feature Store + MLflow + Model Serving
```

### Governance Stack
```
Unity Catalog + Lakehouse Monitoring + Audit Logs + Lineage
```

### BI Stack
```
SQL Warehouse + Databricks SQL + BI Tools (Tableau/Power BI)
```

## Medallion Architecture Details

### Bronze Layer
- **Purpose**: Raw data ingestion
- **Schema**: Schema-on-read, flexible
- **Format**: Delta/Iceberg tables
- **Retention**: Long-term raw data storage
- **Use**: Audit trail, reprocessing

### Silver Layer
- **Purpose**: Cleansed and validated data
- **Schema**: Defined schema, enforced quality
- **Format**: Delta/Iceberg with constraints
- **Retention**: Medium to long-term
- **Use**: Analytics, ML feature engineering

### Gold Layer
- **Purpose**: Business-level aggregations
- **Schema**: Star/snowflake schema optimized
- **Format**: Delta tables with optimization
- **Retention**: Based on business needs
- **Use**: BI, reporting, dashboards

## Download Links

Official reference architectures available for download:
- **AWS**: https://docs.databricks.com/aws/en/lakehouse-architecture/reference
- **Azure**: https://learn.microsoft.com/en-us/azure/databricks/lakehouse-architecture/reference
- **GCP**: https://docs.databricks.com/gcp/en/lakehouse-architecture/reference

Format: 11 x 17 (A3) PDF diagrams

## Implementation Notes

When generating diagrams:
1. Start with swim lane structure
2. Add components left to right
3. Add storage layer at bottom
4. Add governance layer spanning top or bottom
5. Connect components with 1px arrows
6. Add icons for each component
7. Label clearly with DM Sans font
8. Keep max width/height at 1000px
9. Export with white background
10. Validate all text is readable

## Example Architecture Titles

For slide titles or diagram headers:
- "Databricks Lakehouse Reference Architecture"
- "Real-Time Streaming Analytics on Databricks"
- "Modern Data Warehouse with Delta Lake"
- "End-to-End ML Platform Architecture"
- "Multi-Cloud Data Mesh with Unity Catalog"
- "GenAI Application Architecture"
- "Data Lakehouse with External Federation"
