"""
DAST Configuration - reads from input.json and manages test parameters
"""
import json
import os
from typing import Dict, Optional

class DastConfig:
    def __init__(self):
        self.load_config()

    def load_config(self):
        """Load configuration from input.json"""
        config_file = os.path.join(os.path.dirname(__file__), '..', 'input.json')

        with open(config_file, 'r') as f:
            config = json.load(f)

        self.base_url = config.get('baseUrl', 'http://localhost:8000')
        self.user_email = config.get('user_email', '')
        self.admin_token = config.get('admin', None)

        # Enforce scope - only allow localhost/127.0.0.1
        if 'localhost' not in self.base_url and '127.0.0.1' not in self.base_url:
            raise ValueError(f"SECURITY: Only localhost allowed. Got: {self.base_url}")

    def get_base_url(self) -> str:
        return self.base_url

    def get_user_email(self) -> str:
        return self.user_email

# Global config
CONFIG = DastConfig()

