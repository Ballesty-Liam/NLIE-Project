import yaml
import os
from typing import Dict, Any, Optional

class ConfigHandler:
    def __init__(self, config_path: str = "../config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            if not os.path.exists(self.config_path):
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file)

            return config
        except Exception as e:
            raise Exception(f"Error loading configuration: {str(e)}")

    def get_api_key(self, service: str) -> str:
        """Get API key for specified service."""
        try:
            return self.config['api_keys'][service]['key']
        except KeyError:
            raise KeyError(f"API key not found for service: {service}")

    def get_model_name(self, service: str) -> str:
        """Get model name for specified service."""
        try:
            return self.config['api_keys'][service]['model']
        except KeyError:
            raise KeyError(f"Model name not found for service: {service}")

    def get_base_url(self, service: str) -> Optional[str]:
        """Get base URL for specified service if it exists."""
        try:
            return self.config['api_keys'][service].get('base_url')
        except KeyError:
            return None

    def get_model_settings(self) -> Dict[str, Any]:
        """Get general model settings."""
        return self.config.get('model_settings', {})

    def get_analysis_settings(self, analysis_type: str) -> Dict[str, Any]:
        """Get settings for specific analysis type."""
        try:
            return self.config['analysis_settings'][analysis_type]
        except KeyError:
            return {}

    def get_output_settings(self) -> Dict[str, Any]:
        """Get output configuration settings."""
        return self.config.get('output_settings', {})

    def validate_config(self) -> bool:
        """Validate the configuration file has all required fields."""
        required_fields = [
            'api_keys',
            'model_settings',
            'analysis_settings',
            'output_settings'
        ]

        required_api_fields = ['key', 'model']

        try:
            # Check main sections exist
            for field in required_fields:
                if field not in self.config:
                    raise KeyError(f"Missing required section: {field}")

            # Check API configurations
            for service in ['claude', 'openai', 'sonar', 'xai']:
                if service not in self.config['api_keys']:
                    raise KeyError(f"Missing API configuration for: {service}")

                for field in required_api_fields:
                    if field not in self.config['api_keys'][service]:
                        raise KeyError(f"Missing {field} for {service}")

            return True

        except Exception as e:
            print(f"Configuration validation failed: {str(e)}")
            return False



# Usage example:
if __name__ == "__main__":
    try:
        config = ConfigHandler()

        # Validate configuration
        if not config.validate_config():
            print("Configuration validation failed!")
            exit(1)

        # Example usage
        print(f"Claude API Key: {config.get_api_key('claude')}")
        print(f"OpenAI Model: {config.get_model_name('openai')}")
        print(f"Sonar Base URL: {config.get_base_url('sonar')}")
        print(f"Model Settings: {config.get_model_settings()}")

    except Exception as e:
        print(f"Error: {str(e)}")