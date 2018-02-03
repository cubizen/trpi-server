from modules.http_server.httpserver import TemplatesRender


class PackagesExplorer:
    @staticmethod
    def main(request):
        package_list = [  # test data
            {"name": "Test1", "id": "1", "author": "Hateful_Carre1", "version": "0.8.4", "updatadate": "2018-02-01"},
            {"name": "Test2", "id": "2", "author": "Hateful_Carre1", "version": "0.1.9", "updatadate": "2018-01-30"},
            {"name": "Test3", "id": "3", "author": "Jerry", "version": "1.0.9", "updatadate": "2018-01-14"},
        ]
        return TemplatesRender.r(
            "packages_explorer.html",
            package_list=package_list,
        )

    @staticmethod
    def download(request):
        f = open("./packagesLibrary/street cctv camera record.mp4", "rb")
        return f.read()


class API:
    @staticmethod
    def search(request):
        return "api"
