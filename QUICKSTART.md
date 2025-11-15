# Quick Start Guide

Get your Databricks Presentation Creator running in 5 minutes!

## 1. Prerequisites Check

Ensure you have:
- [ ] Python 3.8 or higher installed
- [ ] Databricks workspace access
- [ ] Personal access token from Databricks

## 2. Install & Configure

### Step 1: Install Dependencies

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Configure Databricks CLI

```bash
# Install Databricks CLI (if not already installed)
pip install databricks-cli

# Configure with your workspace
databricks configure --token
```

When prompted, enter:
- **Host**: Your workspace URL (e.g., `https://your-workspace.cloud.databricks.com`)
- **Token**: Your personal access token

To get a token:
1. Log into your Databricks workspace
2. Click your profile icon → Settings
3. Go to "Developer" → "Access tokens"
4. Click "Generate new token"
5. Copy the token (you won't see it again!)

## 3. Launch the Application

### Option A: Using the launch script (Linux/Mac)

```bash
./run.sh
```

### Option B: Direct Python execution

```bash
python app.py
```

The application will start on `http://localhost:8050`

## 4. Create Your First Presentation

1. **Open Browser**: Navigate to `http://localhost:8050`

2. **Verify Connection**: Check that the status shows "Connected as [your-email]"

3. **Configure**:
   - Number of Slides: `5`
   - Sections: `Introduction, Architecture, Implementation`
   - Prompt:
     ```
     Create a presentation about building a real-time analytics platform
     using Databricks for an e-commerce company. Include medallion
     architecture, streaming data ingestion, and ML model deployment.
     ```

4. **Generate**: Click "Generate Presentation"

5. **Download**: Click the download button to save your PowerPoint file

## 5. Troubleshooting

### Issue: "Databricks CLI not configured"

**Fix**:
```bash
databricks configure --token
```

### Issue: "Connection failed"

**Check**:
- Your workspace URL is correct (should include `https://`)
- Your token hasn't expired
- You have network access to the workspace

### Issue: "Cannot import databricks.sdk"

**Fix**:
```bash
pip install databricks-sdk
```

### Issue: Fonts not rendering in diagrams

**Fix (Ubuntu/Debian)**:
```bash
sudo apt-get install fonts-dejavu fonts-dejavu-core fonts-dejavu-extra
```

**Fix (Mac)**:
Fonts should be pre-installed. If issues persist, install via Homebrew:
```bash
brew install font-dejavu
```

## 6. Next Steps

- Try different prompts and topics
- Experiment with different slide counts
- Add custom sections for your use cases
- Review the generated content and iterate

## Example Prompts

### Data Platform Migration
```
Create a presentation for migrating from Snowflake to Databricks Lakehouse.
Include TCO analysis, migration strategy, and architecture comparison.
Emphasize Delta Lake benefits and Unity Catalog for governance.
```

### ML Platform
```
Present an end-to-end MLOps platform on Databricks for a financial
services company. Cover feature engineering, model training, deployment,
and monitoring. Include MLflow integration and model governance.
```

### Real-time Analytics
```
Design a real-time customer analytics solution using Databricks for
a retail company. Include streaming ingestion with Auto Loader,
medallion architecture, and Delta Live Tables pipelines.
```

## Tips for Best Results

1. **Be Specific**: The more detailed your prompt, the better the output
2. **Use Databricks Terminology**: Mention specific products (Delta Lake, Unity Catalog, etc.)
3. **Define Sections**: Help organize the presentation logically
4. **Iterate**: Generate multiple versions and pick the best slides

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review the Databricks Foundation Models documentation
- Ensure your Databricks CLI is properly configured

---

Happy presenting! 🎉
