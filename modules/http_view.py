import jinja2

from modules import bottle
from modules.bottle import route, static_file

from configs import setting

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
    package_list = [  # test data
        {"name": "Test1", "id": "1", "author": "Hateful_Carre1", "version": "0.8.4", "updatadate": "2018-02-01"},
        {"name": "Test2", "id": "2", "author": "Hateful_Carre1", "version": "0.1.9", "updatadate": "2018-01-30"},
        {"name": "Test3", "id": "3", "author": "Jerry", "version": "1.0.9", "updatadate": "2018-01-14"},
    ]
    return TemplatesRender.r("packages_explorer.html",
                             package_list=package_list,
                             )


@route(R + '/static/:path#.+#')
def static(path):
    return static_file(path, root='./static')
