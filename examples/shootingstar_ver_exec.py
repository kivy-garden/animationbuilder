# -*- coding: utf-8 -*-

import itertools

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import ListProperty
from kivy.app import App

import beforetest
from animationbuilder import AnimationBuilder


class CustomizedMesh(Factory.Mesh):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('fmt', [(b'vPosition', 2, 'float'), ])
        super(CustomizedMesh, self).__init__(*args, **kwargs)


Factory.register('CustomizedMesh', cls=CustomizedMesh)

ANIMATION_CODE = r'''
# __init__ is special, will be automatically instanciated when ANIMATION_CODE is loaded.
__init__:
    exec_on_create: |
        from random import random
        from kivy.utils import get_random_color

change_color_randomly:
    color: "eval: get_random_color()"
    d: "eval: random() + 1"

random_sleep:
    d: 0.01
    s: "eval: random()"

star_bounce:
    P:
        - center_x: "eval: random() * parent.width"
          d: "eval: bounce_duration"
        - y: 0
          d: "eval: bounce_duration"
          t: out_bounce

star_opacity:
    S:
        - opacity: 1
          d: "eval: bounce_duration"
        - random_sleep
        - opacity: 0
          d: "eval: random() + 1"

star_color:
    S:
        - change_color_randomly
        - change_color_randomly
        - change_color_randomly

star_init:
    S:
        - exec_on_create: |
            bounce_duration = random() * 4 + 2
        - exec: |
            length = random() * 200 + 20
            for property_name, value in {
                'color': get_random_color(),
                'size': (length, length, ),
                'size_hint': (None, None, ),
                'top': parent.height,
                'right': parent.width - random() * 100,
                'opacity': 0,
            }.items():
                setattr(widget, property_name, value)

star_main:
    S:
        - star_init
        - random_sleep
        - P:
            - star_bounce
            - star_opacity
            - star_color
'''

Builder.load_string(r'''
<Star>:
    canvas:
        StencilPush:
        CustomizedMesh:
            vertices: self.mesh_vertices
            indices: self.MESH_INDICES
            mode: 'triangles'
        StencilUse:
        Color:
            rgba: self.color
        Rectangle:
            pos: 0, 0,
            size: self.size
        StencilUnUse:
        StencilPop:
''')


class Star(Factory.RelativeLayout):
    color = ListProperty()
    mesh_vertices = ListProperty()
    MESH_INDICES = [
        0, 3, 5,
        1, 4, 6,
        1, 2, 3,
    ]
    MESH_VERTICES = [value / 2 + 0.5 for value in (
        .0000, 1.0000,
        .2245, .3090,
        .9511, .3090,
        .3633, -.1180,
        .5878, -.8090,
        # .0000, -.3820,
        -.5878, -.8090,
        # -.3633, -.1180,
        -.9511, .3090,
        # -.2245, .3090,
    )]

    def on_size(self, __, size):
        self.mesh_vertices = (
            length * factor
            for length, factor
            in zip(itertools.cycle(size), self.MESH_VERTICES))


class ShootingStarApp(App):

    def build(self):
        self.root = root = Factory.FloatLayout()
        self.anims = AnimationBuilder.load_string(
            ANIMATION_CODE, globals={'parent': root, })
        return root

    def on_start(self):
        Clock.schedule_interval(self.spawn_star, 0.5)

    def spawn_star(self, dt):
        star = Star()
        root = self.root
        anim = self.anims['star_main']
        root.add_widget(star)
        anim.bind(on_complete=lambda *args: root.remove_widget(star))
        anim.start(star)


if __name__ == '__main__':
    ShootingStarApp().run()
