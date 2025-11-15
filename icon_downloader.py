"""
Download and cache custom icons for Databricks diagrams
Supports Databricks, Delta Lake, and medallion architecture icons
"""
from urllib.request import urlretrieve
import os
from pathlib import Path


class IconDownloader:
    """Download and manage custom icons for architecture diagrams"""

    def __init__(self, icon_dir="custom_icons"):
        self.icon_dir = Path(icon_dir)
        self.icon_dir.mkdir(exist_ok=True)

        # Icon URLs (using publicly available sources)
        self.icon_urls = {
            # Databricks icons
            "databricks": "https://cdn.brandfetch.io/idZVoMqUWL/theme/dark/symbol.svg?c=1dxbfHSJFAPEGdCLU4o5B",
            "databricks_logo": "https://cdn.brandfetch.io/idZVoMqUWL/w/400/h/400/icon?c=1dxbfHSJFAPEGdCLU4o5B",

            # Delta Lake
            "delta_lake": "https://docs.delta.io/latest/_static/delta-lake-logo.png",

            # Apache Spark
            "spark": "https://spark.apache.org/images/spark-logo-trademark.png",

            # Medallion layers (will create programmatically if needed)
            "bronze_medal": "https://www.svgrepo.com/download/530440/bronze-medal.svg",
            "silver_medal": "https://www.svgrepo.com/download/530441/silver-medal.svg",
            "gold_medal": "https://www.svgrepo.com/download/530442/gold-medal.svg",
        }

    def download_icon(self, name: str, force=False) -> Path:
        """
        Download an icon if it doesn't exist locally

        Args:
            name: Icon name from icon_urls
            force: Force re-download even if exists

        Returns:
            Path to the downloaded icon file
        """
        if name not in self.icon_urls:
            raise ValueError(f"Unknown icon: {name}. Available: {list(self.icon_urls.keys())}")

        url = self.icon_urls[name]
        extension = url.split('.')[-1].split('?')[0]  # Extract extension before query params

        # Handle SVG vs PNG
        if 'svg' in extension.lower():
            extension = 'svg'
        elif 'png' in extension.lower() or 'icon' in url:
            extension = 'png'

        filename = f"{name}.{extension}"
        filepath = self.icon_dir / filename

        if not filepath.exists() or force:
            try:
                print(f"Downloading {name} icon from {url}...")
                urlretrieve(url, filepath)
                print(f"✓ Saved to {filepath}")
            except Exception as e:
                print(f"Warning: Failed to download {name}: {e}")
                return None

        return filepath

    def download_all(self, force=False):
        """Download all icons"""
        print("Downloading custom icons for Databricks diagrams...")
        downloaded = {}

        for name in self.icon_urls:
            filepath = self.download_icon(name, force=force)
            if filepath:
                downloaded[name] = str(filepath)

        print(f"\n✅ Downloaded {len(downloaded)} icons to {self.icon_dir}/")
        return downloaded

    def get_icon_path(self, name: str) -> str:
        """Get path to icon, download if needed"""
        for ext in ['svg', 'png', 'jpg']:
            filepath = self.icon_dir / f"{name}.{ext}"
            if filepath.exists():
                return str(filepath)

        # Icon doesn't exist, download it
        filepath = self.download_icon(name)
        return str(filepath) if filepath else None


if __name__ == "__main__":
    downloader = IconDownloader()
    icons = downloader.download_all()

    print("\nAvailable icons:")
    for name, path in icons.items():
        print(f"  {name}: {path}")
