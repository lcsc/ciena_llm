import os
import sys
from dataclasses import dataclass
from typing import Optional, Union, Dict, Any, List, Tuple

import yaml


@dataclass
class ModelConfig:
    name: str
    source: str
    size: Optional[int] = None
    base: Optional[str] = None


class SeqiaConfigurationException(Exception):
    """Custom exception for configuration errors."""

    pass


def get_package_root(levels_up=4) -> str:
    path = os.path.abspath(__file__)
    for _ in range(levels_up):
        path = os.path.dirname(path)
    return path


class ConfigLoader:
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

    def load_config(self, path: str) -> Dict[str, Any]:
        """
        Load configuration from a YAML file.

        :param path: Path to the YAML configuration file.
        :return: Configuration dictionary.
        """
        with open(path, "r") as config_file:
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
            if key == "pipeline":
                # Override entire pipeline section
                base_config[key] = value
            elif isinstance(value, dict) and key in base_config:
                base_config[key] = self.merge_configs(base_config.get(key, {}), value)
            else:
                base_config[key] = value
        return base_config
