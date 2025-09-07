# evidently_materializer.py
import os
from typing import Type, Any

from zenml.materializers.base_materializer import BaseMaterializer
from zenml.enums import ArtifactType, VisualizationType  # Make sure VisualizationType is imported
from evidently.report import Report
from pathlib import Path

class EvidentlyReportMaterializer(BaseMaterializer):
    """
    Custom Materializer for Evidently Report objects.

    This materializer saves the report as an HTML file for visualization
    and a JSON file for data extraction.
    """
    ASSOCIATED_TYPES = (Report,)

    def load(self, data_type: Type[Any]) -> Report:
        """Load is not implemented for this example."""
        print(
            "Warning: The `load` method of the custom EvidentlyReportMaterializer "
            "is not implemented."
        )
        return None

    def save(self, report: Report) -> None:
        """Save the Evidently Report to the artifact store."""
        html_path = os.path.join(self.uri, "report.html")
        json_path = os.path.join(self.uri, "report.json")
        
        report.save_html(html_path)
        report.save_json(json_path)

    def save_visualizations(self, report: Report): # Return type hint removed for simplicity
        """Saves a visualization and returns a dictionary pointing to it."""
        visualization_path = os.path.join(self.uri, "report.html")
        report.save_html(visualization_path)
        
        # This return statement is the crucial fix
        return {visualization_path: VisualizationType.HTML}