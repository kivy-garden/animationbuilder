'''
(This file is based on kivy/tools/kviewer.py)

livepreview
===========

livepreview is a simple tool allowing you to dynamically display
an anim file, taking its changes into account (thanks to watchdog).

You can use the script as follows::

    python -m kivy_garden.animationbuilder.livepreview ./test.yaml

This will display the test.yaml and automatically update the display when the
file changes.

.. note: This scripts uses watchdog to listen for file changes. To install
   watchdog::

   pip install watchdog
'''

from sys import argv
import io
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.uix.label import Label
from kivy.graphics.transformation import Matrix

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from os.path import dirname, basename, join, exists

from . import AnimationBuilder
from .animation_classes import Animation


if len(argv) != 2:
    print('usage: %s filename.yaml' % argv[0])
    exit(1)


PATH = dirname(argv[1])
TARGET = basename(argv[1])

# create empty file if it doesn't exist
if not exists(argv[1]):
    stream = io.open(argv[1], 'wb')
    stream.close()

Builder.load_string(r'''
<AnimationTarget@Scatter>:
    size_hint: None, None
    Image:
        size: root.size
        allow_stretch: True
        source: 'data/logo/kivy-icon-128.png'
''')


def reset_widget(widget):
    Animation.cancel_all(widget)
    widget.pos = (0, 0, )
    widget.pos_hint = {}
    widget.size = (100, 100, )
    widget.size_hint = (None, None, )
    widget.opacity = 1
    if isinstance(widget, Factory.Scatter):
        widget.transform = Matrix()


class AnimHandler(FileSystemEventHandler):
    def __init__(self, callback, target, **kwargs):
        super(AnimHandler, self).__init__(**kwargs)
        self.callback = callback
        self.target = target

    def on_any_event(self, event):
        if basename(event.src_path) == self.target:
            self.callback()


class AnimViewerApp(App):
    def build(self):
        o = Observer()
        o.schedule(AnimHandler(self.update, TARGET), PATH)
        o.start()
        Clock.schedule_once(self.update, 1)
        self.root = root = Factory.FloatLayout()
        self.target = target = Factory.AnimationTarget()
        root.add_widget(target)
        return root

    def play_animation(self, *args):
        target = self.target
        reset_widget(target)
        # when the animation completed, replay automatically
        anim = self.anims['main'] + Animation(d=1)
        anim.bind(on_complete=self.play_animation)
        anim.start(target)

    @mainthread
    def update(self, *args):
        root = self.root
        for child in root.children[:]:
            root.remove_widget(child)
        root.add_widget(self.target)
        try:
            self.anims = AnimationBuilder.load_file(
                join(PATH, TARGET), locals={'parent': root, })
            self.play_animation()
        except Exception as e:
            root.add_widget(Label(text=(
                e.message if getattr(e, 'message', None) else str(e)
            )))


if __name__ == '__main__':
    AnimViewerApp().run()
