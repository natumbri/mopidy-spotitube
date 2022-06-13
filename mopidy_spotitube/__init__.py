import logging
import pathlib

import pkg_resources
from mopidy import config, ext

__version__ = pkg_resources.get_distribution("Mopidy-SpotiTube").version

logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = "Mopidy-SpotiTube"
    ext_name = "spotitube"
    version = __version__

    def get_default_config(self):
        return config.read(pathlib.Path(__file__).parent / "ext.conf")

    def get_config_schema(self):
        schema = super().get_config_schema()
        schema["spotify_users"] = config.List()
        return schema

    def setup(self, registry):
        from .backend import SpotiTubeBackend

        registry.add("backend", SpotiTubeBackend)
