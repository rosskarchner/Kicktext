import os
import os.path
import tempfile

from gi.repository import Gio
from engines import ENGINES

class DocumentController(object):
    engine_name = 'Markdown'
    last_mtime = 0
    path = None
    monitor = None
    
    def __init__(self, window):
        self.window = window
        window.connect('delete_event', self.close_files)

    def watch_file(self, path, webview):
        self.path =path
        self.close_files()
        self.dir = os.path.dirname(self.path)
        self.gfile = Gio.file_new_for_path(path)
        self.monitor = self.gfile.monitor(0,None)

        self.scratch = tempfile.NamedTemporaryFile(dir=self.dir, prefix='.', suffix='.html')
        self.scratch_url = "file://%s" % self.scratch.name

        def update_webview(*args):
            engine = ENGINES[self.engine_name]
            content = engine(self.path)
            self.scratch.truncate(0)
            self.scratch.write(content)
            self.scratch.flush()
            os.fsync(self.scratch.file.fileno())
            webview.load_uri(self.scratch_url)

        update_webview()
        webview.connect('load-error',update_webview)
        self.monitor.connect('changed', update_webview)

    def close_files(self, *args):
        if hasattr(self,'scratch') and not self.scratch.closed:
            self.scratch.close()
        return False
