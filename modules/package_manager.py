import base64
import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

PACKAGES_SAVE_PATH = "./packages_save/"


class PackageManager:
    def __init__(self, licenses=None, name=None):
        self.name = name
        self.license = licenses

    def get_info(self):
        xml_path = PACKAGES_SAVE_PATH + self.license + "/package.xml"
        xml_root = ET.ElementTree(file=xml_path).getroot()

        return {
            "name": xml_root.find('name').text,
            "author": xml_root.find('author').text,
            "type": xml_root.find('type').text,
            "version": xml_root.find('version').text,
            "application": xml_root.find('application').text,
        }

    @staticmethod
    def get_list():
        # Get package library list
        package_list = os.listdir(PACKAGES_SAVE_PATH)
        for i in range(len(package_list)):
            # Get license info
            debase64 = base64.b64decode(package_list[i]).decode()
            license_info = debase64.split(":")
            info = {
                "name": license_info[0],
                "author": license_info[1],
                "updatadate": "",
                "latest": ""
            }

            package_list[i] = info

        return package_list


if __name__ == '__main__':
    print(PackageManager().get_list())
