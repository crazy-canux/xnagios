#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Copyright (C) 2015 Canux CHENG               #
# All rights reserved                                                #
# Name: nagios.py
# Author: Canux canuxcheng@gmail.com                                 #
# Version: V1.0                                                      #
# Time: Fri 14 Aug 2015 01:51:44 AM EDT
######################################################################
# Description:
######################################################################

from deploy import Deploy
from application import Application
from host import Host
# from service import Service
import os


class NRobot(Application, Host, Deploy):

    def define_options(self):
        super(NRobot, self).define_options()
        self.action_parser.add_argument("--cb",
                                        action="store_true",
                                        dest="create_branch",
                                        required=False,
                                        help="Specify to create or \
                                        checkout branch.")
        self.action_parser.add_argument("--db",
                                        action="store_true",
                                        dest="delete_branch",
                                        required=False,
                                        help="Specify to delete a local \
                                        branch or a remote branch.")
        self.action_parser.add_argument("--ca",
                                        action="store_true",
                                        dest="create_application",
                                        required=False,
                                        help="Specify to create application.")
        self.action_parser.add_argument("--da",
                                        action="store_true",
                                        dest="delete_application",
                                        required=False,
                                        help="Specify to delete application.")
        self.action_parser.add_argument("--ch",
                                        action="store_true",
                                        dest="create_host",
                                        required=False,
                                        help="Specify to create host. Use \
                                        -t to Specify the host file and \
                                        template file.")
        self.action_parser.add_argument("--dh",
                                        action="store_true",
                                        dest="delete_host",
                                        required=False,
                                        help="Specify to delete host. Write \
                                        the hostname you want to delete in \
                                        config/host/host.txt")
        self.action_parser.add_argument("--cs",
                                        action="store_true",
                                        dest="create_service",
                                        required=False,
                                        help="Specify to create service.")
        self.action_parser.add_argument("--ds",
                                        action="store_true",
                                        dest="delete_service",
                                        required=False,
                                        help="Specify to delete service.")


def main():
    # robot = NRobot(version="2.0.0.0", description="Config nagios automatic.")
    robot = NRobot()
    os.chdir(robot.args.path)

    # Create new application.
    if robot.args.create_application:
        robot.create_branch()
        robot.create_application()
        if robot.args.create_host:
            robot.create_host()
        robot.commit_branch()
        robot.deploy_branch()
    elif robot.args.delete_application:
        robot.create_branch()
        robot.delete_application()
        if robot.args.delete_host:
            robot.delete_host()
        robot.commit_branch()
        robot.deploy_branch()
    # Create new host.
    elif robot.args.create_host:
        robot.create_branch()
        robot.create_host()
        robot.commit_branch()
        robot.deploy_branch()
    # Remove host.
    elif robot.args.delete_host:
        robot.create_branch()
        robot.delete_host()
        robot.commit_branch()
        robot.deploy_branch()
    elif robot.args.create_service:
        pass
    elif robot.args.delete_service:
        pass
    else:
        pass
    robot.logger.debug("==== END DEBUG ====")


if __name__ == "__main__":
    main()
