'''
(This file is based on kivy/tools/kviewer.py)

livepreview
=======

livepreview is a simple tool allowing you to dynamically display
a anim file, taking its changes into account (thanks to watchdog).

You can use the script as follows::

    python livepreview.py ./test.yaml

This will display the test.yaml and automatically update the display when the
file changes.

.. note: This scripts uses watchdog to listen for fiel changes. To install
   watchdog::

   pip install watchdog
'''

from sys import argv
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.uix.label import Label
from kivy.animation import Animation

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from os.path import dirname, basename, join

from animationbuilder import AnimationBuilder


if len(argv) != 2:
    print('usage: %s filename.anim' % argv[0])
    exit(1)


PATH = dirname(argv[1])
TARGET = basename(argv[1])


Builder.load_string(r'''
<AnimationTarget@Scatter>:
    size_hint: None, None
    Image:
        size: root.size
        source: 'kivy-logo-black-128.png'
''')


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
        self.root = Factory.FloatLayout()
        return self.root

    def schedule_update(self, *args):
        Clock.schedule_once(self.update, 1)

    @mainthread
    def update(self, *args):
        root = self.root
        for child in root.children[:]:
            Animation.cancel_all(child)
            root.remove_widget(child)
        try:
            anim = AnimationBuilder.load_file(join(PATH, TARGET))['preview']
            anim.bind(on_complete=self.schedule_update)
            child = Factory.AnimationTarget()
            root.add_widget(child)
            anim.start(child)
        except Exception as e:
            root.add_widget(Label(text=(
                e.message if getattr(e, 'message', None) else str(e)
            )))


if __name__ == '__main__':
    AnimViewerApp().run()
