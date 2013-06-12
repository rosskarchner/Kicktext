from gi.repository import Gio
from engines import ENGINES

class DocumentController(object):
    engine_name = 'Markdown'
    last_mtime = 0
    path = None
    monitor = None

    def watch_file(self, path, webview):
        self.path =path
        self.gfile = Gio.file_new_for_path(path)
        self.monitor = self.gfile.monitor(0,None)

        def update_webview(*args):
            engine = ENGINES[self.engine_name]
            content = engine(self.path)
            webview.load_string(content, 'text/html','UTF-8', 'http://localhost')

        update_webview()
        self.monitor.connect('changed', update_webview)
