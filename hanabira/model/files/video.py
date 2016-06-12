# -*- coding: utf-8 -*-

from pylons.i18n import _
from .filetype import Filetype
import logging, os, requests
log = logging.getLogger(__name__)

class VideoFile(Filetype):
    '''VideoFile represents a webm file

    Current implementation uses thumbnailer service (at :5000).
    Also required `exiftool` for creating metadata.
    '''

    __mapper_args__ = {'polymorphic_identity': u'video'}

    CouldNotCreateThumbnail = Exception('Could not create thumbnail!')
    NotAnVideoFile = Exception('Not a video file!')

    # XXX hardcoded
    thumbnailerURL = 'http://127.0.0.1:5000/'
    def thumbnailerConfig(self, w:int = 200, h:int = 200, interp: str = 'Lanczos3', jpeg: int = 90) -> dict:
        return {'w': str(w), 'h': str(h), 'interp': str(interp), 'jpeg': str(jpeg)}

    def process(self, file, resolution, fileset) -> bool:
        log.debug('Processing %s[0], %s bytes' % (file.temp_file.path, file.temp_file.size))

        meta = self.gen_meta(file.temp_file.path)

        # generate thumbnail
        conf = self.thumbnailerConfig(w = resolution, h = resolution)
        tmp = open(file.temp_file.path, 'rb')
        r = requests.post(VideoFile.thumbnailerURL, data = conf , files = {'file': tmp})
        tmp.close()

        # check errors
        if r.status_code != requests.codes.ok:
            log.warning('thumbnailer error', r.status_code, r.text)
            raise VideoFile.CouldNotCreateThumbnail

        # save the temporary file
        path = self.fs.new_temp_path('jpg')
        with open(path, 'wb') as out: out.write(r.content)
        if not os.path.exists(path): raise VideoFile.CouldNotCreateThumbnail

        # save
        w, h = r.headers['dstimage-width'], r.headers['dstimage-height']
        file.thumbnail = self.fs.thumbnail(path, 'jpg', w, h)
        return Filetype.process(self, file, resolution, fileset, meta)

    def process_metadata(self, metadata, file) -> str:
        return 'Video {0[Image Size]} x {0[Duration]}; {0[File Size]}'.format(metadata)

    def get_superscription(self) -> str:
        return _('Click the image to play video')

    def gen_meta(self, path: str) -> dict:
        exif = self.popen('exiftool "{0}"'.format(path))
        if not 'video/' in exif or not 'Duration' in exif or not 'Image Size' in exif:
            raise VideoFile.NotAnVideoFile

        meta = {}
        for line in exif.strip().split('\n'):
            if not ':' in line: continue
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip()
        print(meta) # XXX debug
        return meta

