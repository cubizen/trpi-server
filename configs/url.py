# ========================================================================
#
# * WARNING * Changing the content of this file at will may cause a crash.
#
# ========================================================================

from configs import setting
from modules.http_server.view import PackagesExplorer, API

ALLOWED_URL = {
    "": PackagesExplorer.main,
    "/download": PackagesExplorer.download,
    "/api": API.search,
}

ALLOWED_URL = {"/" + setting.ROOT_URL + t: ALLOWED_URL[t] for t in ALLOWED_URL}
