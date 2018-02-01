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
        pass

    def stop(self):
        pass

    def restart(self):
        pass

    def config(self):
        pass
