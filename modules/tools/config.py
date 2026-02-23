import yaml
import os
from pathlib import Path
from typing import Any, Optional

#WARNING: AI CODEDING
class Config:
    """配置管理类，支持嵌套访问、默认值、环境变量覆盖"""

    _instance: Optional['Config'] = None
    _data: dict = {}

    def __new__(cls, config_path: str = "config.yml") -> 'Config':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config(config_path)
        return cls._instance

    def _load_config(self, config_path: str) -> None:
        """加载配置文件"""
        path = Path(config_path)
        if not path.exists():
            self._data = {}
            return

        with open(path, "r", encoding="utf-8") as f:
            self._data = yaml.safe_load(f) or {}

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项，支持点号分隔的嵌套键

        Examples:
            config.get("aria2.threads")  # 返回 16
            config.get("aria2.max_speed", 0)  # 返回默认值 0
        """
        keys = key.split(".")
        value = self._data

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        # 支持环境变量覆盖（环境变量名格式：MAA_ARIA2_THREADS）
        env_key = f"MAA_{'_'.join(keys).upper()}"
        if env_key in os.environ:
            return self._convert_env_value(os.environ[env_key])

        return value

    @staticmethod
    def _convert_env_value(value: str) -> Any:
        """转换环境变量值的类型"""
        if value.lower() in ("true", "yes"):
            return True
        if value.lower() in ("false", "no"):
            return False
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass
        return value

    def reload(self) -> None:
        """重新加载配置文件"""
        self.__class__._instance = None