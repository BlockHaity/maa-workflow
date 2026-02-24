import json
from . import Logging

class I18N():
    """
    I18N模块，用于处理多语言翻译
    """
    def __init__(self,language="zh_CN"):
        self.language = language
        self.i18n_dict_dir = "DATA/i18n"
        self._cache = {}
        
    def file(self,key):
        """从字典文件中提取"""
        if self.language not in self._cache:
            try:
                with open(f"{self.i18n_dict_dir}/{self.language}.json", "r", encoding="utf-8") as f:
                    self._cache[self.language] = json.load(f)
            except FileNotFoundError:
                Logging.error(f"i18n file {self.language}.json not found")
                return None
        
        i18n_dict = self._cache[self.language]
        if key in i18n_dict:
            return i18n_dict[key]
        else:
            Logging.error(f"i18n key {key} not found in {self.language}.json")
            return None

    def dict(self,i18n_dict):
        """从给与的字典中提取"""
        return i18n_dict[self.language]
