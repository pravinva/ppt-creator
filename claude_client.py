"""
Claude Client for Databricks Foundation Models
Connects to Claude Sonnet 4.5 via Databricks Foundation Model endpoint
"""
import requests
import json
from typing import List, Dict, Any


class ClaudeClient:
    """Client for interacting with Claude Sonnet 4.5 via Databricks Foundation Models"""

    def __init__(self, host: str, token: str):
        """
        Initialize Claude client

        Args:
            host: Databricks workspace host URL
            token: Databricks access token
        """
        self.host = host.rstrip('/')
        self.token = token
        self.model = "claude-sonnet-4-5"

        # Databricks Foundation Model API endpoint
        self.api_endpoint = f"{self.host}/serving-endpoints/databricks-meta-llama-3-1-405b-instruct/invocations"
        # Note: Adjust endpoint based on your Databricks workspace setup
        # Common patterns:
        # - /serving-endpoints/<endpoint-name>/invocations
        # - /api/2.0/serving-endpoints/<endpoint-name>/invocations

    def generate_presentation_content(
        self,
        prompt: str,
        num_slides: int,
        sections: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate presentation content using Claude

        Args:
            prompt: User prompt describing the presentation
            num_slides: Number of slides to generate
            sections: Optional list of section names

        Returns:
            Dictionary containing structured presentation content
        """

        # Build the system prompt
        system_prompt = """You are a Databricks Solutions Architect creating technical presentations.
Generate presentation content in JSON format with the following structure:
{
  "title": "Presentation Title",
  "slides": [
    {
      "title": "Slide Title",
      "content": ["Bullet point 1", "Bullet point 2", ...],
      "section": "Section Name (optional)",
      "diagram_type": "medallion|architecture|none",
      "diagram_description": "Description for diagram generation if applicable"
    }
  ]
}

Focus on Databricks solutions, best practices, and technical architecture.
Include medallion architecture concepts where relevant.
Make content clear, technical, and actionable."""

        # Build user prompt
        user_prompt = f"""Create a Databricks solutions architect presentation with {num_slides} slides.

Topic/Requirements: {prompt}
"""

        if sections:
            user_prompt += f"\nOrganize into these sections: {', '.join(sections)}\n"

        user_prompt += "\nReturn ONLY valid JSON with no additional text."

        # Call Claude API via Databricks
        try:
            response = self._call_claude_api(system_prompt, user_prompt)
            return response
        except Exception as e:
            # Fallback to sample structure if API fails
            print(f"API call failed: {e}. Using fallback structure.")
            return self._generate_fallback_content(prompt, num_slides, sections)

    def _call_claude_api(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """
        Make API call to Claude via Databricks Foundation Models

        Args:
            system_prompt: System instructions
            user_prompt: User query

        Returns:
            Parsed JSON response
        """
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        # For Databricks Foundation Models API using Claude-style messages
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "max_tokens": 4096,
            "temperature": 0.7
        }

        # Try multiple endpoint patterns
        endpoints = [
            f"{self.host}/serving-endpoints/databricks-claude-sonnet-4-5/invocations",
            f"{self.host}/api/2.0/serving-endpoints/databricks-claude-sonnet-4-5/invocations",
            f"{self.host}/serving-endpoints/claude-sonnet-4-5/invocations",
        ]

        last_error = None
        for endpoint in endpoints:
            try:
                response = requests.post(
                    endpoint,
                    headers=headers,
                    json=payload,
                    timeout=120
                )

                if response.status_code == 200:
                    result = response.json()

                    # Parse response - handle different response formats
                    if 'choices' in result:
                        content = result['choices'][0]['message']['content']
                    elif 'content' in result:
                        content = result['content']
                    elif isinstance(result, list) and len(result) > 0:
                        content = result[0].get('content', str(result))
                    else:
                        content = str(result)

                    # Extract JSON from content
                    json_str = self._extract_json(content)
                    return json.loads(json_str)

            except Exception as e:
                last_error = e
                continue

        raise Exception(f"All endpoint attempts failed. Last error: {last_error}")

    def _extract_json(self, text: str) -> str:
        """Extract JSON from text that might contain markdown or other formatting"""
        # Remove markdown code blocks if present
        text = text.strip()
        if text.startswith('```json'):
            text = text[7:]
        if text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        return text.strip()

    def _generate_fallback_content(
        self,
        prompt: str,
        num_slides: int,
        sections: List[str] = None
    ) -> Dict[str, Any]:
        """Generate fallback content structure when API is unavailable"""

        slides = []

        # Title slide
        slides.append({
            "title": f"Databricks Solution: {prompt[:50]}",
            "content": [
                "Solutions Architecture Overview",
                "Best Practices and Patterns",
                "Implementation Roadmap"
            ],
            "section": None,
            "diagram_type": "none",
            "diagram_description": None
        })

        # Medallion architecture slide
        if num_slides > 2:
            slides.append({
                "title": "Medallion Architecture",
                "content": [
                    "Bronze Layer: Raw data ingestion",
                    "Silver Layer: Cleaned and conformed data",
                    "Gold Layer: Business-level aggregates"
                ],
                "section": sections[0] if sections else None,
                "diagram_type": "medallion",
                "diagram_description": "Three-tier medallion architecture"
            })

        # Fill remaining slides
        for i in range(len(slides), num_slides):
            section = sections[i % len(sections)] if sections else None
            slides.append({
                "title": f"Key Point {i}",
                "content": [
                    f"Technical consideration {i}.1",
                    f"Best practice {i}.2",
                    f"Implementation guidance {i}.3"
                ],
                "section": section,
                "diagram_type": "none",
                "diagram_description": None
            })

        return {
            "title": f"Databricks Solution: {prompt[:50]}",
            "slides": slides[:num_slides]
        }
