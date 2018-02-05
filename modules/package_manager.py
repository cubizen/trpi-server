import base64
import os

import time

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

PACKAGES_SAVE_PATH = "./packages_save/"


# noinspection PyTypeChecker
class PackageManager:
    def __init__(self, licenses=None, name=None, md5=None):
        self.name = name
        self.license = licenses
        self.md5 = md5

    def get_package_info(self):
        xml_path = PACKAGES_SAVE_PATH + self.license + "/" + self.md5 + "/package.xml"
        xml_root = ET.ElementTree(file=xml_path).getroot()

        return {
            "name": xml_root.find('name').text,
            "author": xml_root.find('author').text,
            "type": xml_root.find('type').text,
            "version": xml_root.find('version').text,
            "createtime": xml_root.find('createtime').text,
            "md5": self.md5,
            "application": xml_root.find('application').text,
        }

    def get_versions(self):
        package_list = os.listdir(PACKAGES_SAVE_PATH + self.license)

        # find latest version at date
        version_index = []
        for file in package_list:
            file_path = "%s%s/%s/package.xml" % (PACKAGES_SAVE_PATH, self.license, file)
            # print("walking xml: " + file_path)

            # xml resolution
            try:
                xml_root = ET.ElementTree(file=file_path).getroot()
            except NotADirectoryError:
                continue

            # get create time
            create_time = xml_root.find('createtime').text
            create_time = time.mktime(time.strptime(create_time, '%Y-%m-%d %H:%M:%S'))

            # sort new > old
            try:

                if create_time < version_index[-1][0]:
                    version_index.append((create_time, file))
                else:
                    version_index.insert(-1, (create_time, file, "b"))
            except IndexError:
                version_index.append((create_time, file))

        # insert version info
        versions = []
        for value in version_index:
            pi = PackageManager(licenses=self.license, md5=value[1]).get_package_info()
            versions.append(pi)

        print(versions)
        return versions

    # Get package license
    def get_license(self):
        package_list = PackageManager.get_list()

        for package in package_list:
            if package["name"] == self.name:
                return package["license"]
            else:
                return None

    def get_readme(self):
        readme_path = "./packages_save/%s/%s/README.md" % (self.license, self.md5)
        print(readme_path)
        try:
            f = open(readme_path, "r")
            readme = f.read()
            f.close()
            return readme
        except:
            return "No README"

    @staticmethod
    def get_list():
        # Get package library list
        package_list = os.listdir(PACKAGES_SAVE_PATH)
        for i in range(len(package_list)):
            # Get license info
            debase64 = base64.b64decode(package_list[i]).decode()
            license_info = debase64.split(":")
            # Get latest package info

            info = {
                "name": license_info[0],
                "author": license_info[1],
                "license": package_list[i],
                "updatadate": "",
                "latest": ""
            }

            package_list[i] = info

        return package_list

    @staticmethod
    def search_package(keyword):
        package_list = PackageManager.get_list()

        search_result = []
        for i in range(len(package_list)):
            lower_name = package_list[i]['name'].lower()
            lower_keyword = keyword.lower()

            if lower_keyword in lower_name:
                # add readme data

                md5s = "PwHLHfHuuFyTiiaOVpwYdtOzKabz"
                pm = PackageManager(licenses=package_list[i]['license'], md5=md5s)
                readme = pm.get_readme()
                package_list[i]["readme"] = base64.b64encode(readme.encode("utf-8")).decode("utf-8")

                search_result.append(package_list[i])

        return search_result
