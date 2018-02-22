
# -*- coding: utf-8 -*-

import io

import yaml

from kivy.animation import Animation


__all__ = ('AnimationBuilder', )


class AnimationBuilder:

    def __init__(self, *, data):
        r'''(internal) Use load_file() or load_string() instead.'''
        self.data = data

    @staticmethod
    def load_file(filepath):
        with io.open(filepath, 'rt', encoding='utf_8') as stream:
            return AnimationBuilder.load_stream(stream)

    @staticmethod
    def load_string(s):
        return AnimationBuilder.load_stream(s)

    @staticmethod
    def load_stream(stream):
        return AnimationBuilder(data=yaml.load(stream))

    def __call__(self, name):
        return Animation(**self.data[name])


def _test():

    from kivy.lang import Builder
    from kivy.base import runTouchApp

    builder = AnimationBuilder.load_file('./test.anim')
    animation = builder('animation0') + builder('animation1') + builder('animation2')

    root = Builder.load_string(r'''
FloatLayout:
    Button:
        id: button
        size_hint: None, None
        size: 100, 100
        text: 'Start Animation'
''')
    button = root.ids.button
    button.bind(on_press=lambda button: animation.start(button))

    runTouchApp(root)


if __name__ == '__main__':
    _test()
