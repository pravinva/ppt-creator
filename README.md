# Databricks Presentation Creator

An interactive Dash web application that creates professional Databricks-branded presentations using Claude Sonnet 4.5 AI and Databricks Foundation Models.

## Features

- **AI-Powered Content Generation**: Leverages Claude Sonnet 4.5 via Databricks Foundation Models to generate intelligent, contextual presentation content
- **Databricks Branding**: Professional slides with authentic Databricks colors, fonts, and design patterns
- **Medallion Architecture Diagrams**: Automatically generates beautiful diagrams illustrating bronze, silver, and gold layer architecture
- **Interactive Web Interface**: Easy-to-use Dash application with real-time feedback
- **Databricks CLI Integration**: Seamlessly authenticates using your existing Databricks CLI configuration
- **Customizable Presentations**: Specify number of slides, sections, and detailed requirements
- **One-Click Download**: Generate and download PowerPoint files instantly

## Architecture Diagrams

The application can generate several types of Databricks-style diagrams:

- **Medallion Architecture**: Three-tier data lakehouse architecture (Bronze → Silver → Gold)
- **Architecture Building Blocks**: Component-based system diagrams
- Custom diagrams based on your presentation requirements

## Prerequisites

- Python 3.8+
- Databricks CLI configured with workspace credentials
- Access to Databricks Foundation Models endpoint (Claude Sonnet 4.5)

## Installation

1. **Clone the repository**:
   ```bash
   cd ppt-creator
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Databricks CLI**:
   ```bash
   databricks configure --token
   ```

   You'll need to provide:
   - Databricks workspace URL (e.g., `https://your-workspace.cloud.databricks.com`)
   - Personal access token (generate from User Settings → Access Tokens)

## Usage

### Starting the Application

Run the Dash application:

```bash
python app.py
```

The application will start on `http://localhost:8050`

### Creating a Presentation

1. **Check Connection Status**: Ensure the Databricks connection is successful (green status indicator)

2. **Configure Presentation**:
   - **Number of Slides**: Set how many slides you want (1-20)
   - **Sections** (optional): Comma-separated section names (e.g., "Introduction, Architecture, Implementation")
   - **Prompt**: Describe your presentation requirements in detail

3. **Example Prompts**:
   ```
   Create a presentation about real-time data processing using Databricks for a retail customer.
   Include medallion architecture, Delta Live Tables, and MLOps best practices.
   ```

   ```
   Solutions architecture for a financial services data platform using Databricks.
   Cover data governance, security, compliance, and streaming analytics.
   ```

   ```
   Migration strategy from traditional data warehouse to Databricks Lakehouse Platform.
   Include cost analysis, architecture patterns, and implementation roadmap.
   ```

4. **Generate**: Click "Generate Presentation" and wait for Claude AI to create your content

5. **Download**: Click the download button to save your PowerPoint file

## Project Structure

```
ppt-creator/
├── app.py                      # Main Dash application
├── databricks_auth.py          # Databricks CLI authentication
├── claude_client.py            # Claude Sonnet 4.5 API integration
├── diagram_generator.py        # Databricks-style diagram generation
├── ppt_generator.py            # PowerPoint creation with branding
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore patterns
└── README.md                   # This file
```

## Configuration

### Databricks Foundation Models Endpoint

The application attempts to connect to Claude Sonnet 4.5 via Databricks Foundation Models. The endpoint URL is constructed based on your workspace configuration.

If you need to customize the endpoint, edit `claude_client.py`:

```python
# Update the endpoint pattern in ClaudeClient.__init__()
self.api_endpoint = f"{self.host}/serving-endpoints/your-endpoint-name/invocations"
```

### Databricks Branding Colors

The application uses official Databricks brand colors:

- **Databricks Red**: `#FF3621`
- **Databricks Dark**: `#1B3139`
- **Bronze**: `#CD7F32`
- **Silver**: `#C0C0C0`
- **Gold**: `#FFD700`

## Customization

### Adding Custom Diagram Types

Edit `diagram_generator.py` to add new diagram types:

```python
def generate_custom_diagram(self, description: str) -> Image.Image:
    # Your custom diagram logic
    pass
```

### Modifying Slide Layouts

Edit `ppt_generator.py` to customize slide layouts and styling:

```python
def _add_custom_slide(self, title: str, content: List[str]):
    # Your custom slide layout
    pass
```

## Troubleshooting

### Authentication Issues

```
Error: Failed to authenticate with Databricks
```

**Solution**: Run `databricks configure --token` and ensure your credentials are correct.

### API Endpoint Issues

```
Error: All endpoint attempts failed
```

**Solution**:
1. Verify your workspace has access to Databricks Foundation Models
2. Check if the endpoint name matches your configuration
3. Ensure your token has appropriate permissions

### Font Issues

```
Warning: Cannot open font
```

**Solution**: The application uses DejaVu fonts. On Linux, install:
```bash
sudo apt-get install fonts-dejavu
```

## Development

### Running in Development Mode

The application runs in debug mode by default, enabling hot-reload:

```bash
python app.py
```

### Testing Locally

To test without Databricks connection, the application includes fallback content generation that creates sample presentations.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is provided as-is for Databricks Solutions Architects and partners.

## Security

- Never commit `.databrickscfg` or tokens to version control
- The `.gitignore` file is configured to exclude sensitive files
- Tokens are stored in memory only and never written to disk by the application

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Databricks Foundation Models documentation
3. Ensure your Databricks CLI is properly configured

## Roadmap

Future enhancements:
- [ ] Additional diagram types (Unity Catalog, Workflows, etc.)
- [ ] Custom branding options
- [ ] Template library
- [ ] Export to PDF
- [ ] Slide preview before download
- [ ] Multi-workspace support
- [ ] Batch presentation generation

---

Built with ❤️ for Databricks Solutions Architects
