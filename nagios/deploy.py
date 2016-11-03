#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Copyright (C) 2015 Faurecia (China) Holding Co.,Ltd.               #
# All rights reserved                                                #
# Name: deploy.py
# Author: Canux canuxcheng@gmail.com                                 #
# Version: V1.0                                                      #
# Time: Mon 10 Aug 2015 10:18:25 PM EDT
######################################################################
# Description:
######################################################################

import commands
import os
from base import NagiosAuto


class Deploy(NagiosAuto):

    """This class used to operate git and fab for nagios configuration."""

    def __init__(self, *args, **kwargs):
        """Define variables."""
        super(Deploy, self).__init__(*args, **kwargs)

        self.parent = "master"
        self.branch_list = ["master", "incubator", "develop"]
        self.prefix = "request"
        self.user = os.getenv("USER")
        if self.args.branch:
            if self.args.branch in self.branch_list:
                self.branch = self.args.branch
                self.remote_branch = self.args.branch
            else:
                self.branch = "%s/%s" % (self.prefix, self.args.branch)
                self.remote_branch = "u/" + self.user + "/" + self.branch

    def define_options(self):
        """Define arguments."""
        super(Deploy, self).define_options()
        self.deploy_parser.add_argument("-b", "--branch",
                                        dest="branch",
                                        required=False,
                                        help="Branch number like 1234, auto add request.")
        self.deploy_parser.add_argument("-c", "--comment",
                                        default="",
                                        dest="comment",
                                        required=False,
                                        help="Commit comment like [CH1234]Revome/Add ....")

    def create_one_branch(self, branch):
        """Create new branch or checkout to old branch."""
        try:
            cmd = "git checkout %s" % branch
            (status, output) = commands.getstatusoutput(cmd)
            self.logger.debug("{0}: {1}".format(cmd, output))
            # If this branch is not exist.
            if status:
                cmd = "git checkout %s" % self.parent
                (status, output) = commands.getstatusoutput(cmd)
                self.logger.debug("{0}: {1}".format(cmd, output))
                # Checkout to master, you need to git pull.
                self.asyn_branch(self.parent, output)
                cmd1 = "git checkout -b %s %s" % (branch, self.parent)
                (status1, output1) = commands.getstatusoutput(cmd1)
                self.logger.debug("{0}: {1}".format(cmd1, output1))
                if not status1:
                    return output1
            # If this branch exist.
            else:
                self.already_exist(branch)
                return output
        except Exception as e:
            self.error("create_one_branch: %s" % e)

    def delete_one_branch(self, branch):
        """Delete a branch."""
        try:
            # Checkout to master to delete other branch.
            self.create_one_branch(self.parent)
            cmd1 = "git branch -D %s" % branch
            (status1, output1) = commands.getstatusoutput(cmd1)
            self.logger.debug("{0}: {1}".format(cmd1, output1))
            if status1:
                self.not_exist(branch)
        except Exception as e:
            self.error("delete_one_branch: %s" % e)

    def commit_one_branch(self, comment):
        """Use git add and git commit to commit changes."""
        try:
            cmd = "git add -A"
            (status, output) = commands.getstatusoutput(cmd)
            self.logger.debug("{0}: {1}".format(cmd, output))
            if not status:
                cmd1 = "git commit -a -m '%s'" % comment
                (status1, output1) = commands.getstatusoutput(cmd1)
                self.logger.debug("{0}: {1}".format(cmd1, output1))
        except Exception as e:
            self.error("commit_branch: %s" % e)

    def push_one_branch(self, branch, remote_branch):
        """Push branch to remote center repository."""
        try:
            if branch and remote_branch:
                cmd = "git push -u origin %s:%s" % (branch, remote_branch)
            elif (not branch) and (not remote_branch):
                cmd = "git push"
            # Delete remote branch.
            elif (not branch) and remote_branch:
                cmd = "git push -u origin :%s" % remote_branch
            (status, output) = commands.getstatusoutput(cmd)
            self.logger.debug("{0}: {1}".format(cmd, output))
            return output
        except Exception as e:
            self.error("push_branch: %s".format(e))

    def status_branch(self, branch):
        """Use git status to check branch status."""
        try:
            cmd = "git status"
            (status, output) = commands.getstatusoutput(cmd)
            self.logger.debug(cmd, output)
            if "Untracked files" in output or \
                    "Changes to be committed" in output:
                choice = input("%s\nCommit this files? " % output)
                if choice == 0:
                    comment = input("Input commit comment: ")
                    cmd1 = "git commit -a -m %s" % comment
                    (status1, output1) = commands.getstatusoutput(cmd1)
        except Exception as e:
            self.error("status_branch: %s" % e)

    def conflict_branch(self, output):
        if "Automatic merge failed" in output:
            cmd1 = "git mergetool --tool=meld"
            status1 = os.system(cmd1)
            self.logger.debug("{0}: ".format(cmd1))
            # Delete the *.cfg.orig file.
            # Some other file have to be deleted?
            if not status1:
                cmd2 = "find . -name '*.orig' | xargs rm -f"
                (status2, output2) = commands.getstatusoutput(cmd2)
                self.logger.debug("{0}: {1}".format(cmd2, output2))
                # Commit.
                if not status2:
                    self.commit_one_branch("")

    def asyn_branch(self, branch, output):
        """After checkout to a branch, synchronous to remote branch."""
        if branch in self.branch_list:
            try:
                if "have diverged" in output:
                    cmd = "git reset --hard origin/%s" % branch
                    (status, output) = commands.getstatusoutput(cmd)
                    self.logger.debug("{0}: {1}".format(cmd, output))
                else:
                    cmd1 = "git fetch -p"
                    (status1, output1) = commands.getstatusoutput(cmd1)
                    self.logger.debug("{0}: {1}".format(cmd1, output1))
                    cmd2 = "git pull"
                    (status2, output2) = commands.getstatusoutput(cmd2)
                    self.logger.debug("{0}: {1}".format(cmd2, output2))
                    # if "Automatic merge failed" in output2:
                    self.conflict_branch(output2)
            except Exception as e:
                self.error("asyn_branch %s" % e)

    def merge_branch(self, branch):
        """Merge branch and fix conflict."""
        try:
            cmd = "git merge --no-ff %s" % branch
            (status, output) = commands.getstatusoutput(cmd)
            self.logger.debug("{0}: {1}".format(cmd, output))
            # If conflict.
            self.conflict_branch(output)
        except Exception as e:
            self.error("merge_branch: %s" % e)

    def create_branch(self):
        """Create branch from -b."""
        try:
            if self.args.branch:
                self.create_one_branch(self.branch)
            else:
                self.error("Please use -b specify the branch number")
        except Exception as e:
            self.error("create_branch: %s" % e)

    def delete_branch(self):
        """Delete branch from -b."""
        try:
            if self.args.branch:
                choice = self.input("Are you sure delete %s? " % self.branch)
                if choice == 0:
                    self.delete_one_branch(self.branch)
                choice = self.input("Are you sure delete %s? " %
                                    self.remote_branch)
                if choice == 0:
                    output = self.push_one_branch("", self.remote_branch)
                    if "error" in output:
                        self.not_exist(self.remote_branch)
            else:
                self.error("Please use -b specify the branch number")
        except Exception as e:
            self.error("delete_branch: %s" % e)

    def commit_branch(self):
        try:
            choice = self.input("Are you sure commit this changes? ")
            if choice == 0:
                if self.args.comment:
                    self.commit_one_branch(self.args.comment)
                else:
                    self.error("Please use -c to specify commit comment.")
        except Exception as e:
            self.error("commit_branch: %s" % e)

    def deploy_branch(self):
        """After you finish the request use this function to deploy to nagios."""
        for branch in ["develop", "incubator"]:
            choice = self.input("Are you sure merge to %s? " % branch)
            if choice == 0:
                output = self.create_one_branch(branch)
                self.asyn_branch(branch, output)
                self.merge_branch(self.branch)
                choice = self.input("Are you sure push to %s? " % branch)
                if choice == 0:
                    self.push_one_branch("", "")
                choice = self.input("Are you sure deploy to %s? " % branch)
                if choice == 0:
                    try:
                        cmd = "fab gearman.deploy"
                        os.system(cmd)
                        self.logger.debug("{0}: ".format(cmd))
                    except Exception as e:
                        self.error("deploy_branch: %s" % e)
        # If everything is ok in nagios put it to center.
        choice = self.input("Are you sure push %s to center? " % self.branch)
        if choice == 0:
            output = self.push_one_branch(self.branch, self.remote_branch)
            if "error" in output:
                self.already_exist(self.remote_branch)
                choice = self.input("Are you sure delete and push to center? ")
                if choice == 0:
                    self.push_one_branch("", self.remote_branch)
                    self.push_one_branch(self.branch, self.remote_branch)
