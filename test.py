# -*- coding: utf-8 -*-

import unittest
from textwrap import dedent
from kivy.config import Config
Config.set('graphics', 'maxfps', 0)
from kivy.lang import Builder
from kivy.base import runTouchApp, stopTouchApp

from animationbuilder import AnimationBuilder

AB_load_string = AnimationBuilder.load_string


def yieldsleep(create_gen):
    '''about this decorator
    https://github.com/gottadiveintopython/kivy-module-collection/tree/master/modules/yieldsleep
    '''
    from functools import wraps
    from kivy.clock import Clock

    @wraps(create_gen)
    def func(*args, **kwargs):
        gen = create_gen(*args, **kwargs)

        def resume_gen(dt):
            try:
                Clock.schedule_once(resume_gen, next(gen))
            except StopIteration:
                pass

        resume_gen(0)
    return func


class AnimationBuilderTestCase(unittest.TestCase):

    DELTA = 10

    def setUp(self):
        self.root = root = Builder.load_string(dedent('''
        FloatLayout:
            Image:
                id: target
                source: 'data/logo/kivy-icon-128.png'
                size_hint: None, None
        '''))
        self.target = target = root.ids.target
        target.size = target.texture.size

    def tearDown(self):
        from kivy.core.window import Window
        for child in Window.children[:]:
            Window.remove_widget(child)

    def test_simple_anim(self):
        root = self.root
        target = self.target

        @yieldsleep
        def _func():
            yield 0
            anims = AB_load_string(dedent('''
            main:
                x: 600
            '''))
            anim = anims['main']
            self.assertEqual(target.x, 0)
            yield 0
            anim.start(target)
            yield .5
            self.assertAlmostEqual(target.x, 300, delta=self.DELTA)
            yield .5
            self.assertAlmostEqual(target.x, 600, delta=self.DELTA)
            stopTouchApp()

        _func()
        runTouchApp(root)

    def test_sequential_anim(self):
        root = self.root
        target = self.target

        @yieldsleep
        def _func():
            yield 0
            anims = AB_load_string(dedent('''
            main:
                S:
                    - x: 600
                    - y: 400
            '''))
            anim = anims['main']
            self.assertEqual(target.x, 0)
            self.assertEqual(target.y, 0)
            yield 0
            anim.start(target)
            yield .5
            self.assertAlmostEqual(target.x, 300, delta=self.DELTA)
            self.assertEqual(target.y, 0)
            yield .5
            self.assertAlmostEqual(target.x, 600, delta=self.DELTA)
            self.assertAlmostEqual(target.y, 0, delta=self.DELTA)
            yield .5
            self.assertAlmostEqual(target.x, 600, delta=self.DELTA)
            self.assertAlmostEqual(target.y, 200, delta=self.DELTA)
            yield .5
            self.assertAlmostEqual(target.x, 600, delta=self.DELTA)
            self.assertAlmostEqual(target.y, 400, delta=self.DELTA)
            yield .5
            stopTouchApp()

        _func()
        runTouchApp(root)

    def test_sequential_anim2(self):
        root = self.root
        target = self.target

        @yieldsleep
        def _func():
            yield 0
            anims = AB_load_string(dedent('''
            move_to_right:
                x: 600
            main:
                sequence:
                    - move_to_right
                    - y: 400
            '''))
            anim = anims['main']
            self.assertEqual(target.x, 0)
            self.assertEqual(target.y, 0)
            yield 0
            anim.start(target)
            yield .5
            self.assertAlmostEqual(target.x, 300, delta=self.DELTA)
            self.assertEqual(target.y, 0)
            yield .5
            self.assertAlmostEqual(target.x, 600, delta=self.DELTA)
            self.assertAlmostEqual(target.y, 0, delta=self.DELTA)
            yield .5
            self.assertAlmostEqual(target.x, 600, delta=self.DELTA)
            self.assertAlmostEqual(target.y, 200, delta=self.DELTA)
            yield .5
            self.assertAlmostEqual(target.x, 600, delta=self.DELTA)
            self.assertAlmostEqual(target.y, 400, delta=self.DELTA)
            yield .5
            stopTouchApp()

        _func()
        runTouchApp(root)

    def test_parallel_anim(self):
        root = self.root
        target = self.target

        @yieldsleep
        def _func():
            yield 0
            anims = AB_load_string(dedent('''
            main:
                P:
                    - x: 600
                    - y: 400
                      d: .6
            '''))
            anim = anims['main']
            self.assertAlmostEqual(target.x, 0)
            yield 0
            anim.start(target)
            yield .5
            self.assertAlmostEqual(target.x, 300, delta=self.DELTA)
            self.assertAlmostEqual(target.y, 333, delta=self.DELTA)
            yield .5
            self.assertAlmostEqual(target.x, 600, delta=self.DELTA)
            self.assertAlmostEqual(target.y, 400, delta=self.DELTA)
            yield .5
            stopTouchApp()

        _func()
        runTouchApp(root)

    def test_parallel_anim2(self):
        root = self.root
        target = self.target

        @yieldsleep
        def _func():
            yield 0
            anims = AB_load_string(dedent('''
            move_to_right:
                x: 600
            main:
                parallel:
                    - move_to_right
                    - y: 400
                      d: 0.6
            '''))
            anim = anims['main']
            self.assertAlmostEqual(target.x, 0)
            yield 0
            anim.start(target)
            yield .5
            self.assertAlmostEqual(target.x, 300, delta=self.DELTA)
            self.assertAlmostEqual(target.y, 333, delta=self.DELTA)
            yield .5
            self.assertAlmostEqual(target.x, 600, delta=self.DELTA)
            self.assertAlmostEqual(target.y, 400, delta=self.DELTA)
            yield .5
            stopTouchApp()

        _func()
        runTouchApp(root)

    def test_eval(self):
        root = self.root
        target = self.target

        @yieldsleep
        def _func():
            yield 0
            anims = AB_load_string(dedent('''
            main:
                x: 'e: external_value * 2'
            '''))
            anims.locals = {'external_value': 300, }
            anim = anims['main']
            self.assertEqual(target.x, 0)
            yield 0
            anim.start(target)
            yield 1
            self.assertAlmostEqual(target.x, 600, delta=self.DELTA)
            yield .1
            anims.locals['external_value'] = 0
            anim = anims['main']
            yield 0
            anim.start(target)
            yield 1
            self.assertAlmostEqual(target.x, 0, delta=self.DELTA)
            yield .5
            stopTouchApp()

        _func()
        runTouchApp(root)

    def test_complex_anim(self):
        root = self.root
        target = self.target

        @yieldsleep
        def _func():
            yield 0
            anims = AB_load_string(dedent('''
            blink:
              repeat: True
              S:
                - opacity: .4
                  t: out_quad
                  d: .5
                - opacity: 1
                  t: out_quad
                  d: .5
            ellipse:
              S:
                - P:
                  - center_x: "e: half_width"
                    t: in_sine
                  - y: 0
                    t: out_sine
                - P:
                  - right: "e: width"
                    t: out_sine
                  - center_y: "e: half_height"
                    t: in_sine
                - P:
                  - center_x: "e: half_width"
                    t: in_sine
                  - top: "e: height"
                    t: out_sine
                - P:
                  - x: 0
                    t: out_sine
                  - center_y: "e: half_height"
                    t: in_sine
            main:
              P:
                - blink
                - ellipse
            '''))
            anims.locals = {
                'width': root.width,
                'height': root.height,
                'half_width': root.center_x,
                'half_height': root.center_y,
            }
            anim = anims['main']
            target.center_y = root.center_y
            anim.start(target)
            yield 4
            stopTouchApp()

        _func()
        runTouchApp(root)


if __name__ == '__main__':
    unittest.main()
