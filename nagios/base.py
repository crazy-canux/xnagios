#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Copyright (C) 2015 Canux CHENG               #
# All rights reserved                                                #
# Name: base.py
# Author: Canux canuxcheng@gmail.com                                 #
# Version: V1.0                                                      #
# Time: Tue 11 Aug 2015 04:28:53 AM EDT
######################################################################
# Description:
######################################################################

import logging
import argparse
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import nagios


class NagiosAuto(object):

    """This is the base class for this project."""

    def __init__(self, name=None, version='', description=''):
        # Init the basic information.
        self.name = os.path.basename(sys.argv[0]) if not name else name
        self.version = nagios.__version__
        self.description = nagios.__description__
        self.user = os.getenv("USER")
        self.path = "/home/%s/GIT/gearman/faurecia-nagios-configuration" % self.user

        # Init the logger.
        logging.basicConfig(format='[%(levelname)s] (%(module)s) %(message)s')
        self.logger = logging.getLogger("NagiosAuto")
        self.logger.setLevel(logging.INFO)

        # Init the arguments.
        self.__define_module_options()
        self.define_options()
        self.__parse_options()

        if self.args.debug:
            self.logger.setLevel(logging.DEBUG)
        self.logger.debug("==== BEGIN DEBUG ====")
        self.logger.debug("name: %s", self.name)
        self.logger.debug("version: %s", self.version)
        self.logger.debug("description: %s", self.description)

        # Get the path.
        self.cur = "/".join(os.getcwd().split("/")[:-1])
        self.conf = self.cur + "/etc"
        self.logger.debug("self.path = {}".format(self.path))
        self.logger.debug("self.cur = {}".format(self.cur))
        self.logger.debug("self.conf = {}".format(self.conf))

        if self.__class__.__name__ == "NagiosAuto":
            self.logger.debug("==== END DEBUG ====")

    def __define_module_options(self):
        """Define common arguments for all class."""
        self.parser = argparse.ArgumentParser(description=self.description)
        # Define the basic options here.
        self.parser.add_argument("-V", "--version",
                                 action="version",
                                 version="%s %s" % (self.name, self.version),
                                 help="Show version.")
        self.parser.add_argument("-D", "--debug",
                                 action="store_true",
                                 required=False,
                                 help="Show debug information.",
                                 dest="debug")
        self.group_parser = self.parser.add_argument_group('Alternatives',
                                                           'If not define, use default value.')
        self.group_parser.add_argument("-P", "--path",
                                       default=self.path,
                                       required=False,
                                       help='Default is %(default)s',
                                       dest="path")
        self.group_parser.add_argument("-F", "--force",
                                       action="store_true",
                                       required=False,
                                       help="If file exist, use this to rewrite it.",
                                       dest="force")

    def define_options(self):
        self.action_parser = self.parser.add_argument_group("Action options",
                                                            "Choose the action.")
        self.deploy_parser = self.parser.add_argument_group("Deploy options",
                                                            "Options for deploy to remote server.")
        self.app_parser = self.parser.add_argument_group("Application options",
                                                         "Options for applications")
        self.host_parser = self.parser.add_argument_group("Host options",
                                                          "Options for host")
        self.service_parser = self.parser.add_argument_group("Service options",
                                                             "Options for services")

    def __parse_options(self):
        try:
            self.args = self.parser.parse_args()
        except Exception as e:
            self.error("__parse_options : %s" % e)

    def input(self, tips):
        """Used for choice your options."""
        positive = ["Y", "y", "yes", "YES"]
        negtive = ["N", "n", "no", "NO"]
        choice = raw_input(tips)
        if choice in positive:
            return 0
        elif choice in negtive:
            return 1
        else:
            self.error("input: please use regular char.")

    def error(self, msg):
        """When error print some message and exit the program."""
        raise NagiosAutoError(msg)

    def not_exist(self, msg):
        """When remove file and it's not exist take a warning."""
        comment = "--------------------------------------"
        print "%s%s" % (comment, comment)
        print "%s not exist." % msg
        print "%s%s" % (comment, comment)

    def already_exist(self, msg):
        """When create file and it's exist take a warning."""
        comment = "++++++++++++++++++++++++++++++++++++++"
        print "%s%s" % (comment, comment)
        print "%s already exist." % msg
        print "%s%s" % (comment, comment)

    def delete_blank_line(self, src, des):
        """Delete the blank line in a file."""
        inf = open(src, "r")
        out = open(des, "w")
        lines = inf.readlines()
        for line in lines:
            if line.split():
                out.writelines(line)
        inf.close()
        out.close()


class NagiosAutoError(Exception):

    def __init__(self, msg):
        print "Error - %s" % msg
        raise SystemExit(-1)
