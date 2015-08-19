#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2007-2009  B. Malengier
# Copyright (C) 2009  Swoon on bug tracker
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

#-------------------------------------------------------------------------
#
# Standard python modules
#
#-------------------------------------------------------------------------
import os
import shutil
import unittest

#-------------------------------------------------------------------------
#
# Gramps modules
#
#-------------------------------------------------------------------------
from gramps.gen.const import TEMP_DIR, USER_HOME, USER_PLUGINS
from gramps.gen.constfunc import get_env_var
from gramps.gen.utils.file import media_path, get_empty_tempdir
from gramps.gen.dbstate import DbState
from gramps.version import VERSION

#-------------------------------------------------------------------------
#
# FileTest class
#
#-------------------------------------------------------------------------
class FileTest(unittest.TestCase):

    def test_mediapath(self):
        # Create database
        dbstate = DbState()
        db = dbstate.make_database("bsddb")
        path = get_empty_tempdir("utils_file_test")
        db.write_version(path)
        db.load(path)
        dbstate.change_database(db)
        # Test without db.mediapath set
        self.assertEqual(media_path(db), os.path.normcase(os.path.normpath(os.path.abspath(USER_HOME))))
        self.assertTrue(os.path.exists(media_path(db)))
        # Test with absolute db.mediapath
        db.set_mediapath(os.path.abspath(USER_HOME) + "/test_abs")
        self.assertEqual(media_path(db), os.path.normcase(os.path.normpath(os.path.abspath(USER_HOME + "/test_abs"))))
        # Test with relative db.mediapath
        db.set_mediapath("test_rel")
        self.assertEqual(media_path(db), os.path.normcase(os.path.normpath(os.path.abspath(TEMP_DIR + "/utils_file_test/test_rel"))))
        # Test with environment variable
        db.set_mediapath("$GRAMPSHOME/test_var")
        self.assertEqual(media_path(db), os.path.normcase(os.path.normpath(os.path.abspath(USER_HOME + "/test_var"))))
        db.set_mediapath("/test/$GRAMPS_VERSION/test_var")
        self.assertEqual(media_path(db), os.path.normcase(os.path.normpath(os.path.abspath("/test/" + VERSION + "/test_var"))))
        db.set_mediapath("${GRAMPS_USER_PLUGINS}/test_var")
        self.assertEqual(media_path(db), os.path.normcase(os.path.normpath(os.path.abspath(USER_PLUGINS + "/test_var"))))


#-------------------------------------------------------------------------
#
# main
#
#-------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
