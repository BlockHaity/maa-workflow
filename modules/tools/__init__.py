import locale
import sys

from .logging import Logging
from .i18n import I18N

if sys.platform != "win32":
    i18n = I18N(language=locale.getdefaultlocale()[0])
else:
    i18n = I18N(language="zh_CN")

#TODO: 将windows返回的locale字符串转换为标准语言代码,如Chinese (Simplified)_China.936 --> zh_CN

from .aria2 import aria2
from .config import Config