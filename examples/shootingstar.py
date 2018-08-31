# -*- coding: utf-8 -*-

import itertools
from functools import wraps as functools_wraps
from random import random

from kivy.utils import get_random_color
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import ListProperty
from kivy.app import App

import beforetest
from animationbuilder import AnimationBuilder

schedule_once = Clock.schedule_once


def yieldsleep(create_gen):
    @functools_wraps(create_gen)
    def func(*args, **kwargs):
        gen = create_gen(*args, **kwargs)

        def resume_gen(dt):
            try:
                schedule_once(resume_gen, next(gen))
            except StopIteration:
                pass

        resume_gen(0)
    return func


class CustomizedMesh(Factory.Mesh):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('fmt', [(b'vPosition', 2, 'float'), ])
        super(CustomizedMesh, self).__init__(*args, **kwargs)


Factory.register('CustomizedMesh', cls=CustomizedMesh)

ANIMATION_CODE = r'''
change_color_randomly:
    color: "e: get_random_color()"
    d: "e: random() + 1"

random_sleep:
    d: 0.01
    s: "e: random()"

star_bounce:
    P:
        - center_x: "e: random() * parent.width"
          d: "e: bounce_duration"
        - y: 0
          d: "e: bounce_duration"
          t: out_bounce

star_opacity:
    S:
        - opacity: 1
          d: "e: bounce_duration"
        - random_sleep
        - opacity: 0
          d: "e: random() + 1"

star_color:
    S:
        - change_color_randomly
        - change_color_randomly
        - change_color_randomly

star_main:
    P:
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
        CustomizedMesh:
            vertices: self.mesh_vertices
            indices: self.MESH_INDICES
            mode: 'triangles'
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
        return Factory.FloatLayout()

    def on_start(self):
        self.start_animation()

    @yieldsleep
    def start_animation(self):
        root = self.root
        anims = AnimationBuilder.load_string(
            ANIMATION_CODE,
            globals={
                'parent': root,
                'get_random_color': get_random_color,
                'random': random,
            })

        def spawn_star():
            anims.globals['bounce_duration'] = random() * 4 + 2
            length = random() * 200 + 20

            star = Star(
                color=get_random_color(),
                size=(length, length, ),
                size_hint=(None, None, ),
                top=root.top,
                right=root.width - random() * 100,
                opacity=0,
            )
            root.add_widget(star)
            anim = anims['star_main']
            anim.bind(on_complete=lambda *args: root.remove_widget(star))
            anim.start(star)

        while True:
            spawn_star()
            yield .5 + random()


if __name__ == '__main__':
    ShootingStarApp().run()
