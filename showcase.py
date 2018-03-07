# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.animation import Animation
from kivy.properties import StringProperty, BooleanProperty
from kivy.app import runTouchApp
from kivy.graphics.transformation import Matrix

from animationbuilder import AnimationBuilder


WIDTH, HEIGHT = 800, 600

animations = AnimationBuilder.load_string(r'''
diagonal:
    right: {width}
    top: {height}
rectangle:
    S:
        - right: {width}
          y: 0
          d: 1.4
        - right: {width}
          top: {height}
        - x: 0
          top: {height}
          d: 1.4
        - pos: [0, 0]
rectangle_repeat:
    S:
        - rectangle
    repeat: True
ellipse:
    S:
        - P:
            - center_x: {half_width}
              t: in_sine
            - y: 0
              t: out_sine
        - P:
            - right: {width}
              t: out_sine
            - center_y: {half_height}
              t: in_sine
        - P:
            - center_x: {half_width}
              t: in_sine
            - top: {height}
              t: out_sine
        - P:
            - x: 0
              t: out_sine
            - center_y: {half_height}
              t: in_sine
ellipse_repeat:
    S:
        - ellipse
    repeat: True
blinking:
    S:
        - opacity: 0
          t: in_out_quad
          d: 0.3
        - opacity: 1
          t: in_out_quad
          d: 0.3
    repeat: True
rotate360:
    rotation: 360
rotate_and_rectangle:
    P:
        - rectangle
        - rotation: -2700
          d: 4
in_bounce:
    P:
        - right: {width}
          d: 4
        - top: {height}
          d: 4
          t: in_bounce

'''.format(
    width=WIDTH, half_width=WIDTH / 2,
    height=HEIGHT, half_height=HEIGHT / 2))

Builder.load_string(r'''
<Showcase>:
    target: target
    Scatter:
        id: target
        size_hint: None, None
        Image:
            source: 'kivy-logo-black-128.png'
            size: target.size
    BoxLayout:
        id: menu
        orientation: 'vertical'
        pos_hint: {'right': 1.0}
        size_hint: 0.4, 1
<MenuItem>:
    is_checked: checkbox.active
    CheckBox:
        id: checkbox
        size_hint_x: None
        group: 'menu'
    Label:
        text: root.text
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


class MenuItem(Factory.BoxLayout):
    text = StringProperty()
    is_checked = BooleanProperty()


class Showcase(Factory.FloatLayout):
    def __init__(self, **kwargs):
        super(Showcase, self).__init__(**kwargs)
        add_widget = self.ids.menu.add_widget
        for key in animations.keys():
            menuitem = MenuItem(text=key)
            menuitem.bind(is_checked=self.on_menuitem_clicked)
            add_widget(menuitem)

    def play_animation(self, key):
        print('playing:', key)
        target = self.target
        reset_widget(target)
        # when the animation completed, replay automatically
        anim = animations[key] + Animation(d=1)
        anim.bind(on_complete=lambda *args: self.play_animation(key))
        anim.start(target)

    def on_menuitem_clicked(self, menuitem, is_checked):
        if is_checked:
            self.play_animation(menuitem.text)


runTouchApp(Showcase())
