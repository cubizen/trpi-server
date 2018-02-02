ALLOWED_HOSTNAME = ['*']

# Debug mode
DEBUG = True

LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 8081

# The banned commands
BANNED_COMMANDS = ['']

# How often to check for a updates. (x Min/once)
CHECK_UPDATE_TIME = 5

# Not recommended change the root url
ROOT_URL = "/tritium"

CONTENT_TYPES = {
    "_default": "text/html",
    "html": "text/html",
    "htm": "text/html",
    "css": "text/css",
    "jpg": "image/jpeg",
    "png": "image/png",
    "svg": "text/xml",
    "js": "application/x-javascript",
    "ico": "image/x-icon",
    "tri": "application/*",
}
