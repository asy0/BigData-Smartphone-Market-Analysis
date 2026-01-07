"""
Big Data Analytics Project - Source Modules
This package contains all Python modules for the project.
"""

__version__ = "1.0.0"

# Import main modules for easier access
from . import data_sources
from . import db_connect
from . import mongodb_connect
from . import spark_processing
from . import ml_models
from . import mobile_api_example

__all__ = [
    'data_sources',
    'db_connect',
    'mongodb_connect',
    'spark_processing',
    'ml_models',
    'mobile_api_example'
]
