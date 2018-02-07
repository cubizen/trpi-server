import base64
import random
import shutil
import string

import time

import os


def main(q):
    for i in range(q):
        # Create Random licenses
        package_name = "TestPackage_" + ''.join(random.sample(string.ascii_letters, 5))
        author = ''.join(random.sample(string.ascii_letters, 5))
        license_randomcode = ''.join(random.sample(string.ascii_letters, 8))
        licenses = "%s:%s:%s" % (package_name, author, license_randomcode)
        licenses = base64.b64encode(licenses.encode()).decode()

        print("Creating License: " + licenses)

        # Create license directory
        os.mkdir("./packages_save/" + licenses)

        # Create license_info.xml
        license_info = """
    <package>
        <name>%s</name>
        <author>%s</author>
        <license>%s</license>
    </package>""" % (package_name, author, licenses)

        f = open("./packages_save/" + licenses + "/license_info.xml", "w")
        f.write(license_info)
        f.close()

        # Create Random Package
        for i in range(random.randint(1, 5)):
            now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            md5 = ''.join(random.sample(string.ascii_letters, 28))

            package_xml = """
    <package>
        <name>%s</name>
        <author>%s</author>
        <type>plugins</type>
        <version>V0.0.%d</version>
        <createtime>%s</createtime>
        <application>Bukkit</application>
        <application>pe</application>
        <application>pc</application>
        <license>%s</license>
        <md5>%s</md5>
        <tag>维护</tag>
        <tag>测试</tag>
    </package>
    """ % (package_name, author, i, now_time, licenses, md5)

            print("    -" + md5)

            # Create Package directory
            package_path = "./packages_save/%s/%s" % (licenses, md5)

            # Save package
            os.mkdir(package_path)

            f = open(package_path + "/package.xml", "w")
            f.write(package_xml)
            f.close()

            shutil.copyfile("./demo/cover_picture.jpg", package_path + "/cover_picture.jpg")
            shutil.copyfile("./demo/README.md", package_path + "/README.md")
            shutil.copyfile("./demo/TestPackage.zip", package_path + "/TestPackage.zip")


if __name__ == '__main__':
    print("how many do you want?")
    q = input()
    main(int(q))
