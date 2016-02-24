# -*- coding: utf-8 -*-
from __future__ import absolute_import

import argparse
import ntpath
import os
import socket

import elk
from flask import Flask
from flask import request
from makeTorrent import makeTorrent
from werkzeug import secure_filename

from teamwork.plugin_bases import ModePlugin


app = Flask(__name__)


@app.route("/health")
def health():
    name = socket.gethostname()
    return '{}.TORRENT-BOT at your service !)'.format(name)


@app.route("/bagz/upload", methods=['POST'])
def receive_upload():
    f = request.files['filedata']
    filename = secure_filename(f.filename)
    try:
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(save_path)

        if 'true' in request.args.get('seed').lower():
            create_torrent(save_path, torrent_destination='bagz')
    except Exception as e:
        return str(e)

    return 'Successfully uploaded {}.'.format(filename)


def create_torrent(filepath, tracker='udp://tracker.openbittorrent.com:80/announce', torrent_destination='bagz'):
    mk = makeTorrent(announce=tracker)
    mk.single_file(filepath)

    name = ntpath.basename(filepath)
    with open(os.path.join(torrent_destination, name+'.torrent'), 'wb') as tf:
            tf.write(mk.getBencoded())


class TorrentPeerPlugin(elk.Elk):
    __with__ = ModePlugin

    def add_parser(self, subparsers):
        description = 'manages host torrent activity'
        parser = subparsers.add_parser('torrent-peer', description=description, help=description,
                                       formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('-u', '--upload-dir', default='bagz', help="directory to upload files to")
        parser.add_argument('-p', '--port', type=int, default=7777, help="port to listen on")

        parser.set_defaults(func=self.main)

    def main(self, args):
        app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), args.upload_dir)
        app.run(host='0.0.0.0', port=args.port)
