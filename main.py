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
import simplejson


config = ConfigParser.ConfigParser()
config.read("config.ini")
uid_start = config.getint("settings", "uid_start")
uid_end = config.getint("settings", "uid_end")
pass_length = config.getint("settings", "pass_length")


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

def read_version(directory, cms_type):
    if cms_type=="Joomla":
        script_php = "joomla_version.php"
        if os.path.isfile(directory + "/libraries/joomla/version.php"):
            directory = directory + "/libraries/joomla/"
        elif os.path.isfile(directory + "/libraries/cms/version/version.php"):
            directory = directory + "/libraries/cms/version/"

    elif cms_type == "Wordpress":
        script_php = "wordpress_version.php"
        if os.path.isfile(directory + "/wp-includes/version.php"):
            directory = directory + "/wp-includes/"

    else:
        return {'RELEASE': 'Unknown', 'DEV_LEVEL': 'Unknown'}

    php_process = Popen(["php", script_php, directory], stdout=PIPE)
    values = simplejson.loads(php_process.communicate()[0])
    php_process.stdout.close()
    print values

def change_pass(user, password):
    pass

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
        if configuration:
            password = generate_password(pass_length)
            print configuration['db']
            print configuration['dbprefix']
            print configuration['user']
            print configuration['password']
            data.append([user, password])
            #if change_pass(user, password):
            #    data.append([user, password])
    write_csv(data)

if __name__ == "__main__":
    main()
