import re
import jinja2

from http.server import BaseHTTPRequestHandler, HTTPServer

from configs import setting
from configs import url


class TemplatesRender:
    @staticmethod
    def r(template, **kwargs):
        template_file = open("./templates/" + template, "r")
        template = jinja2.Template(template_file.read())
        template_file.close()

        return template.render(**kwargs)


class CharsProcessing:
    def __init__(self, text):
        self.text = text

    def strpath2listpath(self):
        listpath = self.text.split('/')
        # Delete null value
        for text in listpath:
            if text == '':
                listpath.remove(text)

        # Delete root path
        if listpath[0] == setting.ROOT_URL:
            listpath.remove(setting.ROOT_URL)

        return listpath

    @staticmethod
    def get_content_type(filename):
        # Get extension name
        extension_name = re.findall("\.([^.]*)$", filename)[0]

        if extension_name in setting.CONTENT_TYPES:
            content_type = setting.CONTENT_TYPES[extension_name]
        else:
            content_type = setting.CONTENT_TYPES["_default"]

        return content_type


class HTTPServerRequest(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        list_path = CharsProcessing(self.path).strpath2listpath()

        if self.path in url.ALLOWED_URL:
            content = url.ALLOWED_URL[self.path]()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
            return

        # Return the static files request
        if list_path[0] == "static":
            try:
                file_path = "./" + '/'.join(list_path)

                f = open(file_path, "rb")
                message = f.read()
                f.close()
                self.send_response(200)
                self.send_header('Content-type', CharsProcessing.get_content_type(list_path[-1]))
                self.end_headers()
                self.wfile.write(message)
            except Exception as e:
                print(e)

                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                f = open("./templates/404.html")
                self.wfile.write(bytes(f.read(), "utf8"))
                f.close()
                return


def run_server(server_address):
    httpd = HTTPServer(server_address, HTTPServerRequest)
    print('Running TrIP server in http://%s:%d' % server_address)
    httpd.serve_forever()


if __name__ == '__main__':
    run_server(server_address=('127.0.0.1', 8082))
