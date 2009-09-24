# -*- coding: utf-8 -*-
from buildbot.scheduler import Scheduler

class SVNScheduler(Scheduler):
    """Extend Scheduler to allow multiple projects"""

    def __init__(self, name, builderNames, repository):
        """Override Scheduler.__init__
        Add a new parameter : repository
        """
        Scheduler.__init__(self, name, None, 120,
                           builderNames, fileIsImportant=None)
        self.repository = repository

    def addChange(self, change):
        """Call Scheduler.addChange only if the branch name (eg. project name
        in your case) is in the repository url"""
        if isinstance(change.branch, basestring):
            if change.branch in self.repository:
                change.branch = None
                Scheduler.addChange(self, change)


class FixedScheduler(Scheduler):
    """ fix Scheduler to (somewhat) respect `branch=None` """

    def addChange(self, change):
        """ the documentation states that setting `branch` to `None` should
            make the scheduler only consider changes on the default branch;
            as there seems to be neither support for determining that default
            branch nor for checking for `None`, this gets fixed by always
            adding the change if `branch` was set to `None` """
        if self.branch is None and change.branch is not None:
            change.branch = None
            Scheduler.addChange(self, change)
