import jinja2

from configs import setting
from modules import bottle
from modules.bottle import route, static_file, request
from modules.package_manager import PackageManager

R = setting.ROOT_URL


class TemplatesRender:
    @staticmethod
    def r(template, **kwargs):
        template_file = open("./templates/" + template, "r")
        template = jinja2.Template(template_file.read())
        template_file.close()

        return template.render(**kwargs)


def run():
    bottle.run(
        host=setting.LISTEN_IP,
        port=setting.LISTEN_PORT,
        debug=setting.DEBUG,
        reloader=True,
    )


""" Views """


@route(R)
def packages_explorer():
    return TemplatesRender.r("packages_explorer.html",
                             package_list=PackageManager.get_list(),
                             )


@route(R + "/<package_license>")
def package_info(package_license):
    versions = PackageManager(package_license).get_versions()
    return TemplatesRender.r("packages_information.html",
                             versions=PackageManager(package_license).get_versions(),
                             package_license=package_license,
                             readme="README"
                             )


@route(R + '/static/:path#.+#')
def static(path):
    return static_file(path, root='./static')


""" APIs """


# Open packages library
@route(R + "/get/package/:path#.+#")
def package_download(path):
    return static_file(path, root="./packages_save")


# Search Package API
@route(R + '/api/search', method="POST")
def api_search():
    keyword = request.forms.get('keyword')
    return str(PackageManager.search_package(keyword))


# Get Package Info API
@route(R + '/api/package/info', method="POST")
def api_package_info():
    licenses = request.forms.get('license')
    md5 = request.forms.get('md5')
    flag = PackageManager(licenses=licenses, md5=md5).get_package_info()
    return str(flag)


# Get Versions
@route(R + '/api/package/versions', method="POST")
def api_package_versions():
    licenses = request.forms.get('license')
    flag = PackageManager(licenses=licenses).get_versions()
    return str(flag)


# Get License by package name
@route(R + '/api/package/get-license', method="POST")
def api_package_versions():
    name = request.forms.get('name')
    flag = PackageManager(name=name).get_license()
    return str(flag)
