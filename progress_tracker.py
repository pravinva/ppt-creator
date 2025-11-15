"""
Progress Tracker for Presentation Generation
Manages progress state for real-time feedback during generation
"""
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class ProgressStep:
    """Represents a single progress step"""
    name: str
    status: str  # 'pending', 'running', 'complete', 'error'
    progress: float  # 0-100
    message: str
    details: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class ProgressTracker:
    """Track progress through presentation generation steps"""

    # Progress step weights (total = 100%)
    STEPS = {
        'auth': {'name': 'Databricks Authentication', 'weight': 5},
        'web_search': {'name': 'Web Research', 'weight': 10},
        'url_fetch': {'name': 'URL Content Fetching', 'weight': 10},
        'pdf_extract': {'name': 'PDF Content Extraction', 'weight': 10},
        'pptx_extract': {'name': 'PowerPoint Content Extraction', 'weight': 10},
        'ai_generation': {'name': 'AI Content Generation', 'weight': 30},
        'slide_creation': {'name': 'Creating Slides', 'weight': 15},
        'diagram_generation': {'name': 'Generating Diagrams', 'weight': 5},
        'branding': {'name': 'Applying Branding', 'weight': 3},
        'logo': {'name': 'Adding Logo', 'weight': 2},
        'export': {'name': 'Exporting PowerPoint', 'weight': 5},
    }

    def __init__(self):
        """Initialize progress tracker"""
        self.steps: Dict[str, ProgressStep] = {}
        self.current_step: Optional[str] = None
        self.overall_progress: float = 0.0
        self.start_time: float = time.time()
        self.completed_steps: List[str] = []
        self.error: Optional[str] = None

        # Initialize all steps as pending
        for step_id, step_config in self.STEPS.items():
            self.steps[step_id] = ProgressStep(
                name=step_config['name'],
                status='pending',
                progress=0.0,
                message='Waiting...'
            )

    def start_step(self, step_id: str, message: str = None):
        """
        Start a progress step

        Args:
            step_id: Step identifier (e.g., 'auth', 'web_search')
            message: Optional custom message
        """
        if step_id not in self.STEPS:
            raise ValueError(f"Unknown step: {step_id}")

        self.current_step = step_id
        step = self.steps[step_id]
        step.status = 'running'
        step.start_time = time.time()
        step.message = message or f"Starting {step.name}..."

        # Calculate overall progress (sum of completed steps)
        self._update_overall_progress()

    def update_step(self, step_id: str, message: str, details: str = None, progress: float = None):
        """
        Update current step with progress

        Args:
            step_id: Step identifier
            message: Status message
            details: Optional detailed information
            progress: Optional progress within step (0-100)
        """
        if step_id not in self.STEPS:
            raise ValueError(f"Unknown step: {step_id}")

        step = self.steps[step_id]
        step.message = message
        if details:
            step.details = details
        if progress is not None:
            step.progress = progress

        self._update_overall_progress()

    def complete_step(self, step_id: str, message: str = None):
        """
        Mark a step as complete

        Args:
            step_id: Step identifier
            message: Optional completion message
        """
        if step_id not in self.STEPS:
            raise ValueError(f"Unknown step: {step_id}")

        step = self.steps[step_id]
        step.status = 'complete'
        step.end_time = time.time()
        step.progress = 100.0
        step.message = message or f"{step.name} complete"

        if step_id not in self.completed_steps:
            self.completed_steps.append(step_id)

        self.current_step = None
        self._update_overall_progress()

    def skip_step(self, step_id: str):
        """
        Skip a step (mark as complete without running)

        Args:
            step_id: Step identifier
        """
        if step_id not in self.STEPS:
            return

        step = self.steps[step_id]
        step.status = 'complete'
        step.progress = 100.0
        step.message = 'Skipped'

        if step_id not in self.completed_steps:
            self.completed_steps.append(step_id)

        self._update_overall_progress()

    def error_step(self, step_id: str, error_message: str):
        """
        Mark a step as errored

        Args:
            step_id: Step identifier
            error_message: Error description
        """
        if step_id not in self.STEPS:
            raise ValueError(f"Unknown step: {step_id}")

        step = self.steps[step_id]
        step.status = 'error'
        step.end_time = time.time()
        step.message = error_message

        self.error = error_message
        self.current_step = None

    def _update_overall_progress(self):
        """Calculate overall progress based on completed steps"""
        total_progress = 0.0

        for step_id, step_config in self.STEPS.items():
            step = self.steps[step_id]
            weight = step_config['weight']

            if step.status == 'complete':
                # Full weight for completed steps
                total_progress += weight
            elif step.status == 'running':
                # Partial weight for running step
                total_progress += (weight * step.progress / 100.0)

        self.overall_progress = min(total_progress, 100.0)

    def get_state(self) -> Dict[str, Any]:
        """
        Get current progress state

        Returns:
            Dictionary with all progress information
        """
        elapsed_time = time.time() - self.start_time

        # Get steps in order
        steps_list = []
        for step_id in self.STEPS.keys():
            step = self.steps[step_id]
            step_dict = step.to_dict()
            step_dict['id'] = step_id
            step_dict['weight'] = self.STEPS[step_id]['weight']
            steps_list.append(step_dict)

        # Get completed steps
        completed = [
            {
                'id': step_id,
                'name': self.steps[step_id].name,
                'message': self.steps[step_id].message,
                'duration': (self.steps[step_id].end_time - self.steps[step_id].start_time)
                           if self.steps[step_id].start_time and self.steps[step_id].end_time
                           else None
            }
            for step_id in self.completed_steps
        ]

        # Get current step info
        current_step_info = None
        if self.current_step:
            step = self.steps[self.current_step]
            current_step_info = {
                'id': self.current_step,
                'name': step.name,
                'message': step.message,
                'details': step.details,
                'progress': step.progress
            }

        # Get pending steps
        pending = [
            {'id': step_id, 'name': self.steps[step_id].name}
            for step_id in self.STEPS.keys()
            if self.steps[step_id].status == 'pending'
        ]

        return {
            'overall_progress': round(self.overall_progress, 1),
            'elapsed_time': round(elapsed_time, 1),
            'current_step': current_step_info,
            'completed_steps': completed,
            'pending_steps': pending,
            'all_steps': steps_list,
            'error': self.error,
            'is_complete': self.overall_progress >= 100.0,
            'timestamp': datetime.now().isoformat()
        }

    def to_json(self) -> str:
        """Convert state to JSON string"""
        return json.dumps(self.get_state())


# Global progress tracker instance (for sharing between callbacks)
_current_tracker: Optional[ProgressTracker] = None


def get_tracker() -> ProgressTracker:
    """Get or create global tracker instance"""
    global _current_tracker
    if _current_tracker is None:
        _current_tracker = ProgressTracker()
    return _current_tracker


def reset_tracker():
    """Reset global tracker"""
    global _current_tracker
    _current_tracker = ProgressTracker()
    return _current_tracker


def clear_tracker():
    """Clear global tracker"""
    global _current_tracker
    _current_tracker = None
