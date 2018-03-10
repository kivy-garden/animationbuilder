# -*- coding: utf-8 -*-

from random import random
import itertools
import sys
import os.path
SEARCH_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SEARCH_PATH)

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import (
    StringProperty, BooleanProperty, ListProperty, NumericProperty,
    ObjectProperty)
from kivy.utils import get_random_color
from kivy.app import App

from animationbuilder import AnimationBuilder


animations = AnimationBuilder.load_string(r'''
change_color_randomly:
    color: "eval: get_random_color()"
    d: "eval: random() * + 1"

random_sleep:
    d: "eval: random()"

star_bounce:
    P:
        - center_x: "eval: random() * 800"
          d: "locals: bounce_duration"
        - y: 0
          d: "locals: bounce_duration"
          t: out_bounce

star_opacity:
    S:
        - opacity: 1
          d: "locals: bounce_duration"
        - random_sleep
        - opacity: 0
          d: "eval: random() + 1"

star_main:
    S:
        - random_sleep
        - P:
            - star_bounce
            - star_opacity
            - S:
                - change_color_randomly
                - change_color_randomly
                - change_color_randomly
''')
animations.locals = {'random': random, 'get_random_color': get_random_color, }

Builder.load_string(r'''
<Polygon>:
    canvas:
        StencilPush:
        Mesh:
            vertices: self.mesh_vertices
            indices: self.mesh_indices
            mode: self.mesh_mode
        StencilUse:
        Color:
            rgba: self.color
        Rectangle:
            pos: 0, 0,
            size: self.size
        StencilUnUse:
        StencilPop:
<Star>:
    mesh_indices: self.MESH_INDICES
    mesh_mode: 'triangles'
''')


class Polygon(Factory.RelativeLayout):
    color = ListProperty()
    mesh_vertices = ListProperty()
    mesh_indices = ListProperty()
    mesh_mode = StringProperty()


class Star(Polygon):
    MESH_INDICES = [
        0, 3, 5,
        1, 4, 6,
        1, 2, 3,
    ]
    MESH_VERTICES = [
        .0000, 1.0000, 0, 0,  # => x, y, u, v
        .2245, .3090, 0, 0,
        .9511, .3090, 0, 0,
        .3633, -.1180, 0, 0,
        .5878, -.8090, 0, 0,
        # .0000, -.3820, 0, 0,
        -.5878, -.8090, 0, 0,
        # -.3633, -.1180, 0, 0,
        -.9511, .3090, 0, 0,
        # -.2245, .3090, 0, 0,
    ]

    def on_size(self, __, size):
        half_size = (size[0] / 2, size[1] / 2, 0, 0, )  # => width, height, u, v
        self.mesh_vertices = (
            length * factor + length
            for length, factor
            in zip(itertools.cycle(half_size), self.MESH_VERTICES))


class ShootingStarApp(App):

    def build(self):
        self.root = root = Factory.FloatLayout()
        return root

    def on_start(self):
        Clock.schedule_interval(self.spawn_star, 0.5)

    def spawn_star(self, dt):
        length = random() * 200 + 20
        star = Star(
            color=get_random_color(),
            size=(length, length, ),
            size_hint=(None, None, ),
            top=600,
            right=800 - random() * 100,
            opacity=0)
        root = self.root
        root.add_widget(star)
        animations.locals['bounce_duration'] = random() * 4 + 2
        anim = animations['star_main']
        anim.bind(on_complete=lambda *args: root.remove_widget(star))
        anim.start(star)


if __name__ == '__main__':
    ShootingStarApp().run()
