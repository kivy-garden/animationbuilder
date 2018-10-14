# -*- coding: utf-8 -*-

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
        # Line:
        #     rectangle: [*self.pos, *self.size, ]
        PushMatrix:
        Translate:
            xy: self.center
        Scale:
            x: self.width
            y: self.height
        StencilPush:
        CustomizedMesh:
            vertices: self.MESH_VERTICES
            indices: self.MESH_INDICES
            mode: 'triangles'
        StencilUse:
        Color:
            rgba: self.color
        Rectangle:
            pos: -1, -1
            size: 2, 2
        StencilUnUse:
        CustomizedMesh:
            vertices: self.MESH_VERTICES
            indices: self.MESH_INDICES
            mode: 'triangles'
        StencilPop:
        PopMatrix:
''')


class Star(Factory.Widget):
    color = ListProperty()
    MESH_INDICES = [
        0, 3, 5,
        1, 4, 6,
        1, 2, 3,
    ]
    MESH_VERTICES = (
        0.0, 0.40449999999999997,
        0.11225, 0.059,
        0.47555, 0.059,
        0.18165, -0.1545,
        0.2939, -0.5,
        -0.2939, -0.5,
        -0.47555, 0.059,
    )


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
