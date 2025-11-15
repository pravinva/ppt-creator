"""
Gantt Chart Generator for Project Planning and Timeline Visualization
Creates professional project timeline diagrams for PowerPoint presentations
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from PIL import Image
import io


class GanttGenerator:
    """Generate Gantt charts for project timelines and phases"""

    # Databricks brand colors
    COLORS = {
        'databricks_red': '#FF3621',
        'databricks_dark': '#1B3139',
        'databricks_blue': '#00A4E4',
        'databricks_green': '#00C853',
        'bronze': '#CD7F32',
        'silver': '#C0C0C0',
        'gold': '#FFD700',
        'purple': '#9C27B0',
        'orange': '#FF9800',
    }

    # Phase color mapping
    PHASE_COLORS = {
        'discovery': COLORS['databricks_blue'],
        'design': COLORS['purple'],
        'development': COLORS['databricks_green'],
        'testing': COLORS['orange'],
        'deployment': COLORS['databricks_red'],
        'maintenance': COLORS['silver'],
        'planning': COLORS['databricks_dark'],
        'bronze': COLORS['bronze'],
        'silver': COLORS['silver'],
        'gold': COLORS['gold'],
    }

    def __init__(self, figsize: Tuple[int, int] = (14, 8), dpi: int = 300):
        """
        Initialize Gantt chart generator

        Args:
            figsize: Figure size (width, height) in inches
            dpi: Resolution for output image
        """
        self.figsize = figsize
        self.dpi = dpi

    def generate_project_timeline(
        self,
        tasks: List[Dict[str, Any]],
        title: str = "Project Timeline",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Image.Image:
        """
        Generate a Gantt chart from task list

        Args:
            tasks: List of task dictionaries with:
                   - name: Task name
                   - start: Start date (datetime or string 'YYYY-MM-DD')
                   - duration: Duration in days
                   - phase: Optional phase name for coloring
                   - dependencies: Optional list of dependent task names
            title: Chart title
            start_date: Optional project start date override
            end_date: Optional project end date override

        Returns:
            PIL Image object

        Example tasks:
            [
                {'name': 'Discovery & Planning', 'start': '2024-01-01', 'duration': 30, 'phase': 'discovery'},
                {'name': 'Architecture Design', 'start': '2024-01-15', 'duration': 45, 'phase': 'design'},
                {'name': 'Bronze Layer Implementation', 'start': '2024-02-01', 'duration': 60, 'phase': 'bronze'},
            ]
        """
        # Parse dates
        parsed_tasks = self._parse_tasks(tasks)

        # Calculate date range
        if not start_date:
            start_date = min(t['start'] for t in parsed_tasks)
        if not end_date:
            end_date = max(t['end'] for t in parsed_tasks)

        # Create figure
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        # Plot tasks
        y_pos = 0
        task_positions = {}

        for i, task in enumerate(parsed_tasks):
            task_name = task['name']
            start = task['start']
            duration = task['duration']
            phase = task.get('phase', 'planning').lower()

            # Get color for phase
            color = self.PHASE_COLORS.get(phase, self.COLORS['databricks_blue'])

            # Draw bar
            ax.barh(
                y_pos,
                duration,
                left=start,
                height=0.6,
                color=color,
                edgecolor='black',
                linewidth=0.5,
                alpha=0.8
            )

            # Add task name
            ax.text(
                start + timedelta(days=duration/2),
                y_pos,
                task_name,
                va='center',
                ha='center',
                color='white' if phase in ['development', 'deployment', 'planning'] else 'black',
                fontweight='bold',
                fontsize=10
            )

            task_positions[task_name] = y_pos
            y_pos += 1

        # Format x-axis (dates)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        # Set labels and title
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Tasks', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=16, fontweight='bold', color=self.COLORS['databricks_dark'], pad=20)

        # Set y-axis
        ax.set_yticks(range(len(parsed_tasks)))
        ax.set_yticklabels([])  # Task names are on the bars
        ax.set_ylim(-0.5, len(parsed_tasks) - 0.5)

        # Add grid
        ax.grid(axis='x', alpha=0.3, linestyle='--')

        # Invert y-axis (top to bottom)
        ax.invert_yaxis()

        # Add legend for phases
        unique_phases = list(set(t.get('phase', 'planning').lower() for t in parsed_tasks))
        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, fc=self.PHASE_COLORS.get(phase, self.COLORS['databricks_blue']),
                         edgecolor='black', label=phase.capitalize())
            for phase in sorted(unique_phases)
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

        # Tight layout
        plt.tight_layout()

        # Convert to PIL Image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        plt.close(fig)

        return img

    def generate_phase_timeline(
        self,
        phases: List[Dict[str, Any]],
        title: str = "Implementation Phases"
    ) -> Image.Image:
        """
        Generate a simplified phase timeline (for high-level overview)

        Args:
            phases: List of phase dictionaries with name, start, duration
            title: Chart title

        Returns:
            PIL Image object
        """
        # Use the standard timeline with simplified styling
        return self.generate_project_timeline(phases, title)

    def generate_medallion_timeline(
        self,
        project_name: str = "Databricks Lakehouse Implementation"
    ) -> Image.Image:
        """
        Generate a standard medallion architecture implementation timeline

        Args:
            project_name: Name of the project

        Returns:
            PIL Image object with standard medallion phases
        """
        # Standard medallion implementation phases
        tasks = [
            {'name': 'Discovery & Requirements', 'start': '2024-01-01', 'duration': 30, 'phase': 'discovery'},
            {'name': 'Architecture Design', 'start': '2024-01-15', 'duration': 45, 'phase': 'design'},
            {'name': 'Infrastructure Setup', 'start': '2024-02-01', 'duration': 30, 'phase': 'planning'},
            {'name': 'Bronze Layer - Raw Ingestion', 'start': '2024-02-15', 'duration': 45, 'phase': 'bronze'},
            {'name': 'Silver Layer - Data Cleansing', 'start': '2024-03-15', 'duration': 45, 'phase': 'silver'},
            {'name': 'Gold Layer - Feature Engineering', 'start': '2024-04-15', 'duration': 45, 'phase': 'gold'},
            {'name': 'Integration Testing', 'start': '2024-05-01', 'duration': 30, 'phase': 'testing'},
            {'name': 'UAT & Performance Testing', 'start': '2024-05-20', 'duration': 25, 'phase': 'testing'},
            {'name': 'Production Deployment', 'start': '2024-06-10', 'duration': 15, 'phase': 'deployment'},
            {'name': 'Monitoring & Optimization', 'start': '2024-06-20', 'duration': 30, 'phase': 'maintenance'},
        ]

        return self.generate_project_timeline(tasks, f"{project_name} - Timeline")

    def _parse_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse task dates and calculate end dates"""
        parsed = []

        for task in tasks:
            task_copy = task.copy()

            # Parse start date
            start = task['start']
            if isinstance(start, str):
                start = datetime.strptime(start, '%Y-%m-%d')
            task_copy['start'] = start

            # Calculate end date
            duration = task['duration']
            task_copy['end'] = start + timedelta(days=duration)

            parsed.append(task_copy)

        return parsed

    def save_chart(self, image: Image.Image, filepath: str):
        """Save Gantt chart to file"""
        image.save(filepath, 'PNG')

    def get_image_bytes(self, image: Image.Image) -> bytes:
        """Convert image to bytes for embedding in PowerPoint"""
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr


if __name__ == "__main__":
    print("Testing Gantt Chart Generator...\n")

    generator = GanttGenerator()

    # Test 1: Standard medallion timeline
    print("1. Generating medallion architecture timeline...")
    img1 = generator.generate_medallion_timeline()
    generator.save_chart(img1, "gantt_medallion_timeline.png")
    print("   ✓ Saved: gantt_medallion_timeline.png\n")

    # Test 2: Custom project timeline
    print("2. Generating custom project timeline...")
    custom_tasks = [
        {'name': 'Project Kickoff', 'start': '2024-01-01', 'duration': 5, 'phase': 'planning'},
        {'name': 'Data Source Analysis', 'start': '2024-01-06', 'duration': 20, 'phase': 'discovery'},
        {'name': 'Lakehouse Architecture Design', 'start': '2024-01-20', 'duration': 30, 'phase': 'design'},
        {'name': 'Bronze Layer Development', 'start': '2024-02-15', 'duration': 45, 'phase': 'bronze'},
        {'name': 'Silver Layer Development', 'start': '2024-03-20', 'duration': 40, 'phase': 'silver'},
        {'name': 'Gold Layer Development', 'start': '2024-04-20', 'duration': 35, 'phase': 'gold'},
        {'name': 'Go-Live', 'start': '2024-06-01', 'duration': 10, 'phase': 'deployment'},
    ]

    img2 = generator.generate_project_timeline(
        custom_tasks,
        title="Databricks Data Platform Implementation"
    )
    generator.save_chart(img2, "gantt_custom_project.png")
    print("   ✓ Saved: gantt_custom_project.png\n")

    # Test 3: Phase-based timeline
    print("3. Generating phase timeline...")
    phases = [
        {'name': 'Phase 1: Foundation', 'start': '2024-Q1-01', 'duration': 90, 'phase': 'planning'},
        {'name': 'Phase 2: Build', 'start': '2024-04-01', 'duration': 90, 'phase': 'development'},
        {'name': 'Phase 3: Deploy', 'start': '2024-07-01', 'duration': 60, 'phase': 'deployment'},
    ]

    # Convert Q1 to actual date
    phases[0]['start'] = '2024-01-01'

    img3 = generator.generate_phase_timeline(phases, "Project Phases")
    generator.save_chart(img3, "gantt_phases.png")
    print("   ✓ Saved: gantt_phases.png\n")

    print("✅ All Gantt charts generated successfully!")
    print("\nYou can now embed these in PowerPoint presentations for project planning.")
