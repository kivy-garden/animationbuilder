# -*- coding: utf-8 -*-

__all__ = ('AnimationBuilderException', )


class AnimationBuilderException(Exception):

    def __init__(self, message):
        super(AnimationBuilderException, self).__init__()
        self.message = message

    def __str__(self):
        return self.message
