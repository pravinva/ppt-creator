"""
Databricks Authentication Module
Uses Databricks CLI configuration to get workspace credentials
"""
from databricks.sdk import WorkspaceClient
from databricks.sdk.core import Config
import os


class DatabricksAuth:
    """Handle Databricks authentication using CLI configuration"""

    def __init__(self):
        """Initialize Databricks workspace client using CLI config"""
        try:
            # This will automatically use the Databricks CLI configuration
            # from ~/.databrickscfg or environment variables
            self.workspace_client = WorkspaceClient()
            self.config = self.workspace_client.config
            self.host = self.config.host
            self.token = self.config.token
        except Exception as e:
            raise Exception(f"Failed to authenticate with Databricks: {str(e)}")

    def get_credentials(self):
        """Get workspace credentials"""
        return {
            'host': self.host,
            'token': self.token
        }

    def test_connection(self):
        """Test the connection to Databricks workspace"""
        try:
            current_user = self.workspace_client.current_user.me()
            return True, f"Connected as {current_user.user_name}"
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
