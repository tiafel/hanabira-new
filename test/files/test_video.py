# -*- coding: utf-8 -*-
# vim: ts=4 noet sw=4 sts=4

from hanabira.model.files import VideoFile, Filetype

class MockFilesystem:
	def new_temp_path(self, ext: str) -> str:
		return './out_tmp.' + ext
	def thumbnail(self, path: str, ext: str, w: int, h: int) -> str:
		return '{0} {1} {2} {3}'.format(path, ext, w, h)

class MockTempFile:
	path = './in.webm'
	size = 0

class MockFile:
	temp_file = MockTempFile()


Filetype.process = lambda self, file, resolution, fileset, meta: 42
Filetype.fs = MockFilesystem()

def test_video():
	vf = VideoFile.__new__(VideoFile)

	file = MockFile()
	resolution = 200
	fileset = {}

	assert 42 == vf.process(file, resolution, fileset)
	assert file.thumbnail == './out_tmp.jpg jpg 200 150'

