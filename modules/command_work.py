from configs import setting

from modules.http_server import http_server


class CommandWork:
    def __init__(self, argv):
        self.argv = argv

    def help(self):
        f = open("data/command_help.txt", "r")
        print(f.read())
        f.close()
        return True

    def update(self):
        pass

    def start(self):
        http_server.run_server(server_address=(setting.LISTEN_IP, setting.LISTEN_PORT))

    def config(self):
        pass
