from modules.http_server.http_server import TemplatesRender


class PackagesExplorer:
    @staticmethod
    def main():
        s = TemplatesRender.r(
            "packages_explorer.html",
            path="/",
            test="test",
        )
        return s
