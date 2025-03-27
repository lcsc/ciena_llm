"""
Configuration loader for Ciena LLM.
"""

import os
import sys
from typing import Optional, Dict, Any, List, Tuple

import yaml


class ConfigLoader:
    """
    Load configuration from YAML files and merge them.
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        override_config_path: Optional[str] = None,
    ) -> None:
        """
        Initialize ConfigLoader with optional config file paths.

        :param config_path: Path to the default configuration file.
        :param override_config_path: Path to the override configuration file.
        """
        if config_path is None:
            current_dir = os.path.dirname(__file__)
            config_path = os.path.join(current_dir, "config.yaml")

        # Load the default configuration
        self.config = self.load_config(config_path)

        # Merge with override configuration if provided
        if override_config_path:
            override_config = self.load_config(override_config_path)
            self.config = self.merge_configs(self.config, override_config)

        # Convert pipeline from dictionary to a list of tuples for ordered processing
        self.pipeline = self.get_ordered_pipeline()

    def load_config(self, path: str) -> Dict[str, Any]:
        """
        Load configuration from a YAML file.

        :param path: Path to the YAML configuration file.
        :return: Configuration dictionary.
        """
        with open(path, "r", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)
        return config

    def merge_configs(
        self, base_config: Dict[str, Any], override_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Recursively merge two configurations.

        :param base_config: Base configuration dictionary.
        :param override_config: Override configuration dictionary.
        :return: Merged configuration dictionary.
        """
        for key, value in override_config.items():
            if isinstance(value, dict) and key in base_config:
                base_config[key] = self.merge_configs(base_config.get(key, {}), value)
            else:
                base_config[key] = value
        return base_config

    def get_ordered_pipeline(self) -> List[Tuple[str, Dict[str, Any]]]:
        """
        Get ordered pipeline steps based on order.

        :return: Ordered list of pipeline steps.
        """
        pipeline_items = self.config.get("pipeline", {})
        pipeline_items_enabled = {
            key: item
            for key, item in pipeline_items.items()
            if item.get("enable", False)
        }
        ordered_pipeline = sorted(
            pipeline_items_enabled.items(),
            key=lambda x: x[1].get("order", sys.maxsize),
            reverse=False,
        )
        return ordered_pipeline

    def get_pipeline_order(self) -> List[str]:
        """
        Get the order of pipeline steps.

        :return: List of pipeline step names in order of execution.
        """
        return [step_name for step_name, _ in self.pipeline]

    def save_config(self, path: str) -> None:
        """
        Save the current configuration to a YAML file.

        :param path: Path to the YAML configuration file.
        """
        with open(path, "w", encoding="utf-8") as config_file:
            yaml.safe_dump(self.config, config_file, default_flow_style=False)
