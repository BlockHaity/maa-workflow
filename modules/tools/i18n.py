import json
from . import logging as log

class I18N():
    """
    I18N模块，用于处理多语言翻译
    """
    def __init__(self,language="zh_CN"):
        self.language = language
        self.i18n_dict_dir = "DATA/i18n"
        
    def file(self,key):
        """从字典文件中提取"""
        i18n_dict = json.load(open(f"{self.i18n_dict_dir}/{self.language}.json", "r", encoding="utf-8"))
        if key in i18n_dict:
            return i18n_dict[key]
        else:
            log.error(f"i18n key {key} not found in {self.language}.json")
            return None

    def dict(self,i18n_dict):
        """从给与的字典中提取"""
        return i18n_dict[self.language]