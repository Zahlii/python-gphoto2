# python-gphoto2 - Python interface to libgphoto2
# http://github.com/jim-easterbrook/python-gphoto2
# Copyright (C) 2023  Jim Easterbrook  jim@jim-easterbrook.me.uk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import tempfile
import unittest

import gphoto2 as gp


class TestFile(unittest.TestCase):
    def test_file(self):
        # create CameraFile from data
        test_file = os.path.join(
            os.path.dirname(__file__), 'vcamera', 'copyright-free-image.jpg')
        with open(test_file, 'rb') as f:
            src_data = f.read()
        self.assertEqual(len(src_data), os.path.getsize(test_file))
        self.assertEqual(src_data[:10], b'\xff\xd8\xff\xe0\x00\x10JFIF')
        cam_file = gp.CameraFile()
        cam_file.set_data_and_size(src_data)
        # get mime type from data
        cam_file.detect_mime_type()
        # check detected mime type
        self.assertEqual(cam_file.get_mime_type(), 'image/jpeg')
        # set mime type anyway
        cam_file.set_mime_type('image/jpeg')
        file_time = int(os.path.getmtime(test_file))
        cam_file.set_mtime(file_time)
        file_name = 'cam_file.jpg'
        cam_file.set_name(file_name)
        # read data from CameraFile
        self.assertEqual(cam_file.get_data_and_size(), src_data)
        self.assertEqual(cam_file.get_mime_type(), 'image/jpeg')
        self.assertEqual(cam_file.get_mtime(), file_time)
        self.assertEqual(cam_file.get_name(), file_name)
        self.assertEqual(
            cam_file.get_name_by_type(file_name, gp.GP_FILE_TYPE_RAW),
            'raw_' + file_name)
        self.assertEqual(cam_file.detect_mime_type(), None)
        # copy file
        file_copy = gp.CameraFile()
        file_copy.copy(cam_file)
        self.assertEqual(file_copy.get_data_and_size(), src_data)
        # open file directly
        direct_file = gp.CameraFile()
        direct_file.open(test_file)
        self.assertEqual(direct_file.get_data_and_size(), src_data)
        self.assertEqual(direct_file.get_mtime(), file_time)
        self.assertEqual(direct_file.get_name(), os.path.basename(test_file))
        # create file from file descriptor
        file_copy = gp.CameraFile(os.open(test_file, os.O_RDONLY))
        self.assertEqual(file_copy.get_data_and_size(), src_data)
        # save CameraFile to computer
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_file = os.path.join(tmp_dir, file_name)
            cam_file.save(temp_file)
            self.assertEqual(os.path.getsize(temp_file), len(src_data))
            with open(temp_file, 'rb') as f:
                self.assertEqual(f.read(), src_data)
            self.assertEqual(int(os.path.getmtime(temp_file)), file_time)
        # wipe file data
        cam_file.clean()
        self.assertEqual(cam_file.get_data_and_size(), b'')
        self.assertEqual(cam_file.get_name(), '')


if __name__ == "__main__":
    unittest.main()
