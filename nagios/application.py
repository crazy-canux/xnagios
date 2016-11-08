#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Copyright (C) 2015 Canux CHENG               #
# All rights reserved                                                #
# Name: application.py
# Author: Canux canuxcheng@gmail.com                                 #
# Version: V1.0                                                      #
# Time: Thu 16 Jul 2015 05:03:18 AM EDT
######################################################################
# Description:
######################################################################

import os
from base import NagiosAuto


class Application(NagiosAuto):

    """This used to create new hostgroup and template for a new application."""

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)

        self.app_conf = self.conf + "/application"
        self.hostgroup = self.app_conf + "/hostgroup.cfg"
        self.template = self.app_conf + "/template.cfg"
        self.h_dir = "%s/hostgroups/app/" % self.args.path
        self.t_dir = "%s/templates/hosts/app/" % self.args.path

        if self.__class__.__name__ == "Application":
            self.logger.debug("==== END DEBUG ====")

    def define_options(self):
        """Define options for this class."""
        super(Application, self).define_options()
        self.app_parser.add_argument("-a", "--application",
                                     dest="application",
                                     required=False,
                                     help="The application name.")
        self.app_parser.add_argument("-d", "--domain",
                                     dest="domain",
                                     required=False,
                                     help="Domain name, eg: cws or eit.")
        self.app_parser.add_argument("-s", "--system",
                                     action="append",
                                     dest="system",
                                     required=False,
                                     help="System used in this new applicaion. \
                                     eg: -s win -s aix -s linux")

    def write_hostgroup(self):
        try:
            fhr = open(self.hostgroup, "r")
            lines = fhr.readlines()
            fhw = open(self.hostgroupfile, "w")
            for line in lines:
                if "%s" in line:
                    fhw.write(line % self.application)
                else:
                    fhw.write(line)
            fhr.close()
            fhw.close()
        except Exception as e:
            self.error("write_hostgroup: %s" % e)

    def create_hostgroup(self):
        """Create hostgroup."""
        if os.path.isfile(self.hostgroupfile):
            self.already_exist(self.hostgroupfile)
            if self.args.force:
                self.write_hostgroup()
        else:
            self.write_hostgroup()

    def write_template(self):
        try:
            ftr = open(self.template, "r")
            lines = ftr.readlines()
            ftw = open(self.templatefile, "w")
            for loop in range(0, len(lines)):
                line = lines[loop]
                self.logger.debug("line {0}: {1}".format(loop, line))
                if 0 <= loop <= 12:
                    if loop == 4:
                        if self.args.domain:
                            ftw.write(line % self.application)
                        else:
                            ftw.write(line.split(",")[0]
                                      % self.application + "\n")
                    elif loop == 5:
                        if self.args.domain:
                            ftw.write(line % self.args.domain)
                        else:
                            continue
                    elif loop != 4 and loop != 5 and "%s" in line:
                        ftw.write(line % self.application)
                    else:
                        ftw.write(line)
            for loop in range(0, len(self.args.system)):
                system = self.args.system[loop]
                for loo in range(0, len(lines)):
                    line = lines[loo]
                    if 13 <= loo <= 21:
                        if loo == 13 or loo == 15 or loo == 18:
                            ftw.write(line % (self.application, system))
                        elif loo == 16:
                            ftw.write(line % self.application)
                        elif loo == 17:
                            ftw.write(line % system)
                        else:
                            ftw.write(line)
            for loop in range(0, len(lines)):
                line = lines[loop]
                if 22 <= loop <= 24:
                    ftw.write(line)
            for loop in range(0, len(self.args.system)):
                system = self.args.system[loop]
                for loo in range(0, len(lines)):
                    line = lines[loo]
                    if 25 <= loo <= 32:
                        if "%s" in line:
                            ftw.write(line % (self.application, system))
                        else:
                            ftw.write(line)
            ftr.close()
            ftw.close()
        except Exception as e:
            self.error("write_template: %s" % e)

    def create_template(self):
        """Create template."""
        if os.path.isfile(self.templatefile):
            self.already_exist(self.templatefile)
            if self.args.force:
                self.write_template()
        else:
            self.write_template()

    def create_application(self):
        try:
            if self.args.application and self.args.system:
                self.application = self.args.application
                self.hostgroupfile = self.h_dir + self.application + ".cfg"
                self.templatefile = self.t_dir + self.application + ".cfg"
                self.logger.debug("hostgroupfile: {}".
                                  format(self.hostgroupfile))
                self.logger.debug("templatefile: {}".format(self.templatefile))
                self.create_hostgroup()
                self.create_template()
            else:
                self.error("Please use -a specify application and -s specify \
                           system.")
        except Exception as e:
            self.error("create_application: %s" % e)

    def delete_hostgroup(self):
        if not os.path.isfile(self.hostgroupfile):
            self.not_exist(self.hostgroupfile)
        else:
            try:
                os.remove(self.hostgroupfile)
            except Exception as e:
                self.error("delete_hostgroup: %s" % e)

    def delete_template(self):
        if not os.path.isfile(self.templatefile):
            self.not_exist(self.templatefile)
        else:
            try:
                os.remove(self.templatefile)
            except Exception as e:
                self.error("delete_template: %s" % e)

    def delete_application(self):
        try:
            if self.args.application:
                self.application = self.args.application
                self.hostgroupfile = self.h_dir + self.application + ".cfg"
                self.templatefile = self.t_dir + self.application + ".cfg"
                self.logger.debug("hostgroupfile: {}".
                                  format(self.hostgroupfile))
                self.logger.debug("templatefile: {}".format(self.templatefile))
                self.delete_hostgroup()
                self.delete_template()
            else:
                self.error("Please use -a specify application.")
        except Exception as e:
            self.error("delete_application: %s" % e)
