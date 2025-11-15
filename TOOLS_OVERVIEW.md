# Databricks Tools Overview

You now have **3 different web apps** for creating Databricks content:

## 1. 📄 Databricks Presentation Maker (app.py)

**Port:** 8070
**Use For:** Creating complete presentations with Claude AI

```bash
python app.py
# Opens at http://localhost:8070
```

### Features:
- AI-powered content generation using Claude Sonnet 4.5
- Upload PowerPoint or PDF for modification
- Web search for technologies
- Custom branding from PDF
- Logo placement
- Solutions architecture diagrams
- Medallion architecture diagrams
- Full presentation generation

### When to Use:
✅ Need AI to write presentation content
✅ Want to modify existing PowerPoint files
✅ Need research/web search for technologies
✅ Want complete end-to-end presentation with multiple slides
✅ Need custom branding from company PDF

---

## 2. 🎨 Agentic AI Architecture Generator (agentic_ai_app.py)

**Port:** 8050
**Use For:** Agentic AI journey and platform diagrams

```bash
python agentic_ai_app.py
# Opens at http://localhost:8050
```

### Features:
- 4-phase Agentic AI journey diagrams (Traditional → Predictive → Augmented → Agentic)
- Platform architecture diagrams (Data Sources → Platform → AI Agents → Applications)
- PowerPoint generation with business case
- Professional swim lanes with real arrows
- Works for ANY company (not just Energy Australia)

### When to Use:
✅ Creating Agentic AI transformation roadmap
✅ Showing AI agent architecture
✅ Presenting Agentic AI journey to executives
✅ Need 4-phase transformation diagram
✅ Building Agentic AI platforms

---

## 3. 🏗️ Databricks Architecture Generator (databricks_architecture_app.py)

**Port:** 8051
**Use For:** General Databricks solution architecture diagrams

```bash
python databricks_architecture_app.py
# Opens at http://localhost:8051
```

### Features:
- Multiple architecture templates:
  - **Medallion Architecture** (Bronze/Silver/Gold)
  - **Real-time Streaming** (Kafka, AutoLoader, Delta Live Tables)
  - **ML/MLOps** (Training, Registry, Serving)
  - **Lakehouse** (Unified analytics platform)
  - **Custom** (Define your own)
- Professional swim-lane diagrams
- Modern Databricks 2025 styling
- Download as PNG

### When to Use:
✅ Creating Medallion architecture diagrams
✅ Showing streaming data pipelines
✅ ML/MLOps architecture documentation
✅ Lakehouse platform diagrams
✅ Standard Databricks solution patterns

---

## Quick Decision Guide

### I want to...

**Create a presentation about a new technology**
→ Use **Tool 1** (app.py)
→ It will research and write content with AI

**Show our Agentic AI transformation journey**
→ Use **Tool 2** (agentic_ai_app.py)
→ Specialized for Agentic AI roadmaps

**Document our Medallion architecture**
→ Use **Tool 3** (databricks_architecture_app.py)
→ Has Medallion template built-in

**Modify an existing PowerPoint**
→ Use **Tool 1** (app.py)
→ Upload PPTX and let AI modify it

**Create streaming architecture diagram**
→ Use **Tool 3** (databricks_architecture_app.py)
→ Has streaming template

**Build ML/MLOps architecture**
→ Use **Tool 3** (databricks_architecture_app.py)
→ Has MLOps template

---

## Comparison Table

| Feature | Tool 1<br/>(Presentation Maker) | Tool 2<br/>(Agentic AI) | Tool 3<br/>(Architecture) |
|---------|---------|---------|---------|
| **Port** | 8070 | 8050 | 8051 |
| **AI Content Generation** | ✅ Claude AI | ❌ | ❌ |
| **Web Search** | ✅ | ❌ | ❌ |
| **Upload Existing PPTX** | ✅ | ❌ | ❌ |
| **Custom Branding** | ✅ | ❌ | ❌ |
| **Agentic AI Diagrams** | ❌ | ✅ | ❌ |
| **Medallion Diagrams** | ✅ | ❌ | ✅ |
| **Streaming Diagrams** | ❌ | ❌ | ✅ |
| **ML/MLOps Diagrams** | ❌ | ❌ | ✅ |
| **Lakehouse Diagrams** | ❌ | ❌ | ✅ |
| **Professional Arrows** | ✅ | ✅ | ✅ |
| **PowerPoint Output** | ✅ | ✅ | ❌ (PNG only) |
| **Multiple Slides** | ✅ | ✅ | ❌ (single diagram) |
| **Templates** | ❌ | 1 (Agentic AI) | 4+ (Medallion, etc.) |

---

## File Structure

```
ppt-creator/
│
├── app.py                                 # Tool 1: Presentation Maker (port 8070)
├── agentic_ai_app.py                      # Tool 2: Agentic AI Generator (port 8050)
├── databricks_architecture_app.py         # Tool 3: Architecture Generator (port 8051)
│
├── professional_agentic_ai_generator.py   # Backend for Tool 2
├── professional_architect_diagram_generator.py  # Backend for Tool 3
├── agentic_ai_pptx_generator.py           # PPTX generator for Tool 2
│
├── databricks_auth.py                     # Auth for Tool 1
├── claude_client.py                       # Claude AI for Tool 1
├── ppt_generator.py                       # PPT generator for Tool 1
│
└── databricks_assets/                     # Icons (used by all tools)
```

---

## Common Workflows

### Workflow 1: Create Agentic AI Presentation

1. Use **Tool 2** (agentic_ai_app.py) to generate journey + architecture diagrams
2. Download PNG files
3. Use **Tool 1** (app.py) to create full presentation
4. Upload the PNG diagrams as part of the presentation

### Workflow 2: Medallion Architecture Documentation

1. Use **Tool 3** (databricks_architecture_app.py) with Medallion template
2. Customize layers and components
3. Generate professional diagram
4. Download PNG
5. Optionally: Use **Tool 1** to create full presentation around it

### Workflow 3: Technology Research Presentation

1. Use **Tool 1** (app.py) exclusively
2. Enable web search
3. Let Claude AI research and create content
4. Get complete presentation with diagrams

---

## Tips & Best Practices

1. **Use the Right Tool**: Don't try to create Medallion diagrams in the Agentic AI app - use the Architecture app instead

2. **Combine Tools**: Generate diagrams in specialized tools (2 or 3), then use Tool 1 for full presentations

3. **Templates**: Tool 3 has the most architecture templates - use it for standard Databricks patterns

4. **AI Content**: Only Tool 1 has AI content generation - use it when you need Claude to write slide content

5. **Professional Quality**: All tools generate professional diagrams with swim lanes and real arrows

---

## Installation & Dependencies

All tools share the same dependencies:

```bash
pip install dash dash-bootstrap-components pillow python-pptx anthropic
```

**For Tool 1 only (Presentation Maker):**
- Databricks CLI configured (`databricks configure`)
- Valid Databricks workspace access

**For Tools 2 & 3:**
- No special authentication required
- Just need the databricks_assets folder

---

## Ports Summary

Make sure these ports are available:

- **8070** - Databricks Presentation Maker
- **8050** - Agentic AI Generator
- **8051** - Architecture Generator

You can run all three simultaneously!

---

## Support Files

- `PROFESSIONAL_GENERATOR_GUIDE.md` - Technical documentation for diagram generators
- `README_AGENTIC_AI_APP.md` - User guide for Agentic AI app
- `SOLUTION_SUMMARY.md` - Complete solution overview
- `TOOLS_OVERVIEW.md` - This file!

---

## Which Tool Should I Use Right Now?

Ask yourself:

1. **Do I need AI to write content?** → Tool 1
2. **Am I creating an Agentic AI roadmap?** → Tool 2
3. **Am I documenting a standard Databricks architecture?** → Tool 3

Still not sure? Start with **Tool 1** (app.py) - it's the most comprehensive!

---

**All tools are production-ready and require NO code editing!** 🎉
