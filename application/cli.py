import re
import application.handler as handler

class FTPCLI:
    _handlers = {
        'ls': handler.ls,
        'get': handler.get
    }

    @classmethod
    def execute(cls, src) -> handler.IResponse:
        tokens = cls._tokenize(src)

        if not cls._is_tokenlist_valid(tokens):
            return None
        
        result = cls._handlers[tokens[0]](tokens[1:])

        if (result != None):
            return result
        else:
            return True

    @classmethod
    def validate(cls, src):
        result = False
        tokens = cls._tokenize(src)
        return cls._is_tokenlist_valid(tokens)

    @classmethod
    def _tokenize(cls, src):
        words = re.split(' +', src)
        return words

    @classmethod
    def _is_tokenlist_valid(cls, tokens):
        return tokens[0] in cls._handlers

        return result


