from os import listdir as _listdir
from typing import TypedDict, Literal
import os as _os

__server_path = './server'

class IResponse(TypedDict):
    dest: Literal['control', 'data']
    content: any

def generate_response(is_control, content) -> IResponse:
    obj : IResponse = {
        'dest': 'control' if is_control else 'data',
        'content': content
    }

    return obj


def ls(args) -> IResponse:
    filenames = []
    dirnames = []

    for (dirpath, _dirnames, _filenames) in _os.walk(__server_path):
        filenames.extend(_filenames)
        dirnames.extend(_dirnames)
        break

    dirnames = list(map(lambda x: '/' + x, dirnames))
    content = dirnames + filenames

    return generate_response(True, content)

def get(args) -> IResponse:
    try:
        src = __server_path + '/' + args[0]
        dest = args[1]
    except:
        return generate_response(True, 'Wrong Parameters')

    try:
        f = open(src)
    except:
        return generate_response(True, 'No such file')


    def iterator():
        step = 5
        filesize = _os.path.getsize(src)

        while f.tell() < filesize:
            content = f.read(step)
            yield content

    return generate_response(False, iterator)
