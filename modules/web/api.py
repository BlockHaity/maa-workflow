"""
# API端点文件
所有webapi相关的端点都应该在这个文件中定义，并通过蓝图注册到Flask应用中。
"""

from flask import Blueprint

api_bp = Blueprint('api', __name__)

