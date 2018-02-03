import json
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

    @staticmethod
    def remove_url_args(text):
        try:
            text = text.replace(re.findall("(\?.*)$", text)[0], "")
        except IndexError:
            pass

        return text

    @staticmethod
    def get_url_args(text):
        try:
            args = re.findall("\?(.*)$", text)[0]

            # Regular expressions are too hard to use, LOL
            str_json = '{"%s"}' % args.replace('=', '":"').replace('&', '","')

            args_list = json.loads(str_json)
        except:
            args_list = {}

        return args_list

    @staticmethod
    def strpath2listpath(text):
        listpath = text.split('/')
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
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

        self.args = CharsProcessing.get_url_args(self.path)

    # GET
    def do_GET(self):
        list_path = self.path
        list_path = CharsProcessing.remove_url_args(list_path)
        list_path = CharsProcessing.strpath2listpath(list_path)

        if CharsProcessing.remove_url_args(self.path) in url.ALLOWED_URL:
            path = CharsProcessing.remove_url_args(self.path)
            content = url.ALLOWED_URL[path](self)
            self.send_response(200)
            self.send_header('Content-type', CharsProcessing.get_content_type(list_path[-1]))
            self.end_headers()

            try:
                self.wfile.write(content.encode("utf-8"))
            except AttributeError:
                self.wfile.write(content)

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
    run_server(("localhost", 8080))
