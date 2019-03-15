import pkg_resources
from distutils.version import LooseVersion

try:
    # if in py2
    from urllib import quote as urllib_quote
    PY2_VERSION = True
except ImportError:
    # else (aka in py3)
    from urllib.parse import quote as urllib_quote  # noqa: F401
    PY2_VERSION = False


django_version = pkg_resources.get_distribution('django').version


DJANGO_ONE_SIX = (
    LooseVersion(django_version) < LooseVersion("1.7.0") and
    LooseVersion(django_version) > LooseVersion("1.5.12")
)
