import os

from . import courier, exception, tracking, notification    # noqa


with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../VERSION')) as f:
    __version__ = f.read().strip()


api_key = None
