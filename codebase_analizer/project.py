import os
import shutil
import tempfile

from contextlib import contextmanager
# Python 2/3 compatibility
from builtins import object


class Project(object):
    def __init__(self, project_location):
        self._project_location = project_location
        self._tmpdir = tempfile.gettempdir()

    @property
    def should_be_clonned(self):
        return self._project_location.startswith('http')

    @property
    def name(self):
        project_name = self._project_location.split('/')[-1]
        if self.should_be_clonned:
            # Truncate .git postfix
            project_name = project_name.split('.git')[0]
        return project_name

    @property
    def path(self):
        if self.should_be_clonned:
            # Return path where projects are cloned
            return os.path.join(self._tmpdir, self.name)
        return self._project_location

    @contextmanager
    def open(self):
        """Open project and return its path.
        Clone the project if needed but clean after yourself.
        """
        if self.should_be_clonned:
            self._clone()

        yield self.path

        if self.should_be_clonned:
            # Remove clonned project -
            # user should not store folders he don't know about.
            self._remove()

    def _clone(self):
        assert self.should_be_clonned
        os.system('git clone {repo_url} {directory}'.format(
            repo_url=self._project_location,
            directory=self.path
        ))

    def _remove(self):
        shutil.rmtree(self.path)
