from __future__ import annotations

import json
import os
from enum import Enum
from typing import Dict


class SystemEnvironment(Enum):
    """Enumerations for configurations."""
    TESTING = 'test'
    PROD = 'prod'
    DEV = 'dev'
    QA = 'qa'
    INT = 'int'


class Config:
    """Utility class for easy handling or configuration."""

    _config: Dict[str, dict] = {}

    @classmethod
    def get_env(cls) -> SystemEnvironment:
        """Get the current environment of the worker."""
        env = os.environ.get('COMPONENT_ENV', 'dev')
        return SystemEnvironment(env)

    @classmethod
    def get_raw(cls) -> Dict[str, dict]:
        """Get the current configuration dict. This function will reaload the config always if the current environment is DEV."""
        if not cls._config or cls.get_env() is SystemEnvironment.DEV:
            cls._config = cls._load_config()
        return cls._config

    @classmethod
    def get(cls, key) -> Dict[str, dict]:
        """Get the configuration for a key for the current ENV."""
        config = cls.get_raw()[key]
        env = cls.get_env()
        return config[env._value_]

    @classmethod
    def _config_path(cls):
        config_path = os.environ.get('CONFIG_FILE')
        if not config_path:
            module_file = os.path.abspath(__file__)
            config_path = os.path.join(
                os.path.dirname(module_file), 'config.json')
        return config_path

    @classmethod
    def _load_config(cls):
        fp = open(cls._config_path())
        config = json.load(fp)
        fp.close()
        return config
