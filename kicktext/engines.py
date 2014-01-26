"""
An engine is just a callable-- given a path, returns rendered
HTML
"""
import subprocess




def markdown(path):
    return subprocess.check_output(['pandoc', '-t','html5', path])


ENGINES = {'Markdown': markdown}
