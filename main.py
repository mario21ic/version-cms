#!/usr/bin/env python

import ConfigParser
import pwd
import string
from random import choice
import os
import subprocess
from subprocess import PIPE,Popen
import csv
import ConfigParser


config = ConfigParser.ConfigParser()
config.read("config.ini")
uid_start = config.getint("settings", "uid_start")
uid_end = config.getint("settings", "uid_end")


def list_users():
    users = []
    for p in pwd.getpwall():
        if (p.pw_uid in range(uid_start, uid_end)) \
                and "/home/" in p.pw_dir:
            users.append(p.pw_name)
    return users

def cms_type(directory):
    if os.path.isfile(directory + "/configuration.php"):
        return "Joomla"
    elif os.path.isfile(directory + "/wp-config.php"):
        return "Wordpress"
    return "Other"

def read_version(directory, cms):
    if cms =="Joomla":
        script_php = "joomla_version.php"
        if os.path.isfile(directory + "/libraries/joomla/version.php"):
            directory = directory + "/libraries/joomla/"
        elif os.path.isfile(directory + "/libraries/cms/version/version.php"):
            directory = directory + "/libraries/cms/version/"
        elif os.path.isfile(directory + "/includes/version.php"):
            directory = directory + "/includes/"

    elif cms == "Wordpress":
        script_php = "wordpress_version.php"
        if os.path.isfile(directory + "/wp-includes/version.php"):
            directory = directory + "/wp-includes/"

    else:
        return 'Unknown'

    php_process = Popen(["php", script_php, directory], stdout=PIPE)
    version = php_process.communicate()[0]
    php_process.stdout.close()
    return version

def write_csv(data):
    with open('report.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for line in data:
            writer.writerow(line)


def main():
    data = []
    for user in list_users():
        directory = '/home/' + user + "/public_html/"
        cms = cms_type(directory)
        version = read_version(directory, cms)
        data.append([user, cms, version])
    write_csv(data)

if __name__ == "__main__":
    main()
