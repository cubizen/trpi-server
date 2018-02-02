import jinja2

from configs import setting
from modules import bottle
from modules.bottle import route, static_file
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
    return TemplatesRender.r("packages_information.html",
                             versions=PackageManager(package_license).get_versions(),
                             package_license=package_license,
                             readme="README"
                             )


@route(R + "/download/<license>/<package_md5>")
def package_info(package, package_md5):
    return


@route(R + '/static/:path#.+#')
def static(path):
    return static_file(path, root='./static')
