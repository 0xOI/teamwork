from flask import Flask
from flask import request
from makeTorrent import makeTorrent
from werkzeug import secure_filename
import os
import socket

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './bagz'


@app.route("/")
def hello():
    return "Hello - {} at your service!".format(socket.gethostname().upper())

@app.route("/health")
def health():
    return "I'm healthy!"

@app.route("/skills")
def skills():
    return "I'm pretty much useless :/"

@app.route("/bagz/<cmd>", methods=['GET', 'POST'])
def bagz(cmd='show'):
    if cmd == 'show':
        if not os.path.exists('bagz'):
            os.makedirs('bagz')
            return 'Created empty bagz DIR'

        return ','.join(os.listdir('bagz'))
    elif cmd == 'create':
        if os.path.exists('bagz'):
            return 'bagz DIR already exists.'
        else:
            os.makedirs('bagz')
            return 'Successfully created bagz DIR.'
    elif cmd == 'upload':
        if request.method == 'POST':
            f = request.files['filedata']
            filename = secure_filename(f.filename)
            try:
                if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                create_torrent(filename)
            except Exception as e:
                print(e)
                return str(e)

            return 'Successfully uploaded {} and created torrent.'.format(filename)
        else:
            return 'WTH'

def create_torrent(filepath):
    mk = makeTorrent(announce='udp://tracker.openbittorrent.com:80/announce')
    mk.single_file(os.path.join('/home/ubuntu/bagz', filepath))

    name, ext = os.path.splitext(filepath)
    with open(name+'.torrent', 'wb') as tf:
        tf.write(mk.getBencoded())


if __name__ == "__main__":
    app.run(host='0.0.0.0')