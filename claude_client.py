"""
Claude Client for Databricks Foundation Models
Connects to Claude Sonnet 4.5 via Databricks Foundation Model endpoint
"""
import requests
import json
from typing import List, Dict, Any, Optional
import re
from urllib.parse import urlparse


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
        sections: List[str] = None,
        enable_web_search: bool = False,
        urls: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate presentation content using Claude with optional web research

        Args:
            prompt: User prompt describing the presentation
            num_slides: Number of slides to generate
            sections: Optional list of section names
            enable_web_search: Whether to perform web searches for topics
            urls: Optional list of URLs to fetch information from

        Returns:
            Dictionary containing structured presentation content
        """

        # Gather web research if requested
        research_context = ""
        if enable_web_search or urls:
            research_context = self._gather_web_research(prompt, urls)

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
Make content clear, technical, and actionable.
Use the latest information from web research when provided."""

        # Build user prompt
        user_prompt = f"""Create a Databricks solutions architect presentation with {num_slides} slides.

Topic/Requirements: {prompt}
"""

        if sections:
            user_prompt += f"\nOrganize into these sections: {', '.join(sections)}\n"

        if research_context:
            user_prompt += f"\n\nWeb Research Context:\n{research_context}\n"

        user_prompt += "\nReturn ONLY valid JSON with no additional text."

        # Call Claude API via Databricks
        try:
            response = self._call_claude_api(system_prompt, user_prompt)
            return response
        except Exception as e:
            # Fallback to sample structure if API fails
            print(f"API call failed: {e}. Using fallback structure.")
            return self._generate_fallback_content(prompt, num_slides, sections, research_context)

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

    def _gather_web_research(self, prompt: str, urls: Optional[List[str]] = None) -> str:
        """
        Gather information from web searches and URLs

        Args:
            prompt: User prompt to extract search queries from
            urls: Optional list of URLs to fetch

        Returns:
            Formatted research context string
        """
        research_parts = []

        # Extract URLs from prompt if any
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        found_urls = re.findall(url_pattern, prompt)

        if urls:
            found_urls.extend(urls)

        # Fetch content from URLs
        for url in found_urls:
            try:
                content = self._fetch_url_content(url)
                if content:
                    research_parts.append(f"Information from {url}:\n{content}\n")
            except Exception as e:
                print(f"Failed to fetch {url}: {e}")

        # Perform web searches for key topics mentioned in prompt
        search_terms = self._extract_search_terms(prompt)
        for term in search_terms:
            try:
                search_results = self._web_search(term)
                if search_results:
                    research_parts.append(f"Web search for '{term}':\n{search_results}\n")
            except Exception as e:
                print(f"Web search failed for '{term}': {e}")

        return "\n---\n".join(research_parts) if research_parts else ""

    def _extract_search_terms(self, prompt: str) -> List[str]:
        """Extract key search terms from prompt"""
        # Look for specific product names, technologies mentioned
        terms = []

        # Common Databricks and data engineering terms to search for
        keywords = [
            'genie mcp', 'zerobus', 'delta live tables', 'unity catalog',
            'mlflow', 'databricks sql', 'delta lake', 'lakehouse',
            'auto loader', 'photon', 'serverless'
        ]

        prompt_lower = prompt.lower()
        for keyword in keywords:
            if keyword in prompt_lower:
                terms.append(keyword)

        # Limit to top 3 most relevant searches
        return terms[:3]

    def _fetch_url_content(self, url: str) -> str:
        """Fetch and summarize content from a URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # For simplicity, return first 2000 chars of content
            # In production, you'd want to parse HTML and extract meaningful content
            content = response.text[:2000]

            # Clean up HTML tags (basic)
            content = re.sub(r'<[^>]+>', ' ', content)
            content = re.sub(r'\s+', ' ', content).strip()

            return content[:1500]  # Limit size
        except Exception as e:
            return f"Could not fetch content: {str(e)}"

    def _web_search(self, query: str) -> str:
        """
        Perform web search for a query
        Note: This is a placeholder. In production, integrate with a real search API
        """
        # Placeholder for web search functionality
        # In production, you would integrate with:
        # - Google Custom Search API
        # - Bing Search API
        # - SerpAPI
        # - Or use the search capabilities if available in your environment

        return f"[Web search results for '{query}' would appear here]"

    def _generate_fallback_content(
        self,
        prompt: str,
        num_slides: int,
        sections: List[str] = None,
        research_context: str = ""
    ) -> Dict[str, Any]:
        """Generate fallback content structure when API is unavailable"""

        slides = []

        # Analyze prompt for specific topics
        prompt_lower = prompt.lower()
        has_genie = 'genie' in prompt_lower
        has_zerobus = 'zerobus' in prompt_lower
        has_mcp = 'mcp' in prompt_lower

        # Title slide
        title = "Databricks Modern Data Stack"
        if has_zerobus and has_genie:
            title = "ZeroBus Ingestion with Genie MCP Integration"
        elif has_zerobus:
            title = "ZeroBus for Lakehouse Ingestion"
        elif has_genie:
            title = "Genie MCP for Agent Integration"

        slides.append({
            "title": title,
            "content": [
                "Modern data ingestion and AI integration",
                "Leveraging latest Databricks innovations",
                "Scalable, production-ready architecture"
            ],
            "section": None,
            "diagram_type": "none",
            "diagram_description": None
        })

        # ZeroBus ingestion slide
        if has_zerobus and num_slides > 1:
            slides.append({
                "title": "ZeroBus: Real-Time Lakehouse Ingestion",
                "content": [
                    "Zero-latency data ingestion framework",
                    "Seamless integration with Databricks Lakehouse",
                    "Auto-scaling and fault-tolerant architecture",
                    "Support for multiple data sources and formats",
                    "Built-in schema evolution and validation"
                ],
                "section": sections[0] if sections else None,
                "diagram_type": "architecture",
                "diagram_description": "ZeroBus ingestion architecture"
            })

        # Medallion architecture with ZeroBus
        if num_slides > 2:
            slides.append({
                "title": "ZeroBus Medallion Architecture",
                "content": [
                    "Bronze: ZeroBus ingests raw data in real-time",
                    "Silver: Transformation and quality validation",
                    "Gold: Business-ready analytics tables",
                    "Delta Lake ensures ACID transactions",
                    "Unity Catalog for governance"
                ],
                "section": sections[1] if sections and len(sections) > 1 else None,
                "diagram_type": "medallion",
                "diagram_description": "ZeroBus medallion architecture flow"
            })

        # Genie MCP slide
        if has_genie and has_mcp and num_slides > 3:
            slides.append({
                "title": "Genie MCP: Model Context Protocol",
                "content": [
                    "Simplifies AI agent integration with Databricks",
                    "Standard protocol for context sharing",
                    "Enables seamless agent-to-lakehouse connectivity",
                    "Built-in authentication and authorization",
                    "Supports multiple agent frameworks"
                ],
                "section": sections[2] if sections and len(sections) > 2 else None,
                "diagram_type": "architecture",
                "diagram_description": "Genie MCP integration architecture"
            })

        # Integration slide
        if has_genie and has_zerobus and num_slides > 4:
            slides.append({
                "title": "End-to-End Integration",
                "content": [
                    "ZeroBus ingests data into Lakehouse",
                    "Data flows through medallion layers",
                    "Genie MCP exposes data to AI agents",
                    "Agents query and analyze with natural language",
                    "Real-time insights and automated actions"
                ],
                "section": sections[3] if sections and len(sections) > 3 else None,
                "diagram_type": "architecture",
                "diagram_description": "Complete integration flow"
            })

        # Benefits slide
        if num_slides > 5:
            slides.append({
                "title": "Key Benefits",
                "content": [
                    "Reduced time-to-insight with real-time ingestion",
                    "Simplified AI integration via standard protocols",
                    "Enterprise-grade governance and security",
                    "Scalable architecture for any data volume",
                    "Lower TCO with unified platform"
                ],
                "section": sections[4] if sections and len(sections) > 4 else None,
                "diagram_type": "none",
                "diagram_description": None
            })

        # Fill remaining slides with implementation details
        for i in range(len(slides), num_slides):
            section = sections[i % len(sections)] if sections else None
            slides.append({
                "title": f"Implementation Step {i - len(slides) + 1}",
                "content": [
                    "Configure data sources and connections",
                    "Set up ZeroBus ingestion pipelines",
                    "Deploy medallion architecture layers",
                    "Enable Genie MCP endpoints",
                    "Test and validate integration"
                ],
                "section": section,
                "diagram_type": "none",
                "diagram_description": None
            })

        return {
            "title": title,
            "slides": slides[:num_slides]
        }
