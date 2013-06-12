"""
An engine is just a callable-- given a path, returns rendered
HTML
"""
import subprocess


def nullengine(path):
    return file(path).read()


def markdown(path):
    return subprocess.check_output('pandoc', stdin=file(path))


ENGINES = {'Markdown': markdown}
