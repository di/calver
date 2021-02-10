import os
from distutils import log

import setuptools.command.sdist


class sdist(setuptools.command.sdist.sdist):
    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)
        verfile = os.path.join(base_dir, ".calver-version")
        log.info("Writing version file {}".format(verfile))
        with open(verfile, "wt") as f:
            f.write(self.distribution.metadata.version)
