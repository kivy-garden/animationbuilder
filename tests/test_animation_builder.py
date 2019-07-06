import pytest
from textwrap import dedent as textwrap_dedent
from math import isclose
from kivy.tests import async_sleep, UnitKivyApp, async_run
from kivy_garden.animationbuilder import AnimationBuilder


def basic_app():
    from kivy.lang import Builder
    from kivy.app import App

    class TestApp(UnitKivyApp, App):
        def build(self):
            root = Builder.load_string(textwrap_dedent('''
                FloatLayout:
                    Image:
                        id: target
                        source: 'data/logo/kivy-icon-32.png'
                        size_hint: None, None
                '''))
            target = root.ids.target
            target.size = target.texture_size
            return root

    return TestApp()


@async_run(app_cls_func=basic_app)
async def test_simple_anim(kivy_app, delta):
    target = kivy_app.root.ids.target
    anim = AnimationBuilder.load_string(textwrap_dedent('''
        main:
            x: 300
            d: .5
        '''))['main']
    assert target.x == 0
    anim.start(target)
    await async_sleep(.25)
    assert isclose(target.x, 150, abs_tol=delta)
    await async_sleep(.25)
    assert isclose(target.x, 300, abs_tol=delta)


@async_run(app_cls_func=basic_app)
async def test_sequential_anim(kivy_app, delta):
    target = kivy_app.root.ids.target
    anim = AnimationBuilder.load_string(textwrap_dedent('''
        main:
            S:
                - x: 300
                  d: .5
                - y: 200
                  d: .5
        '''))['main']
    assert target.x == 0
    assert target.y == 0
    anim.start(target)
    await async_sleep(.25)
    assert isclose(target.x, 150, abs_tol=delta)
    assert target.y == 0
    await async_sleep(.25)
    assert isclose(target.x, 300, abs_tol=delta)
    assert isclose(target.y, 0, abs_tol=delta)
    await async_sleep(.25)
    assert target.x == 300
    assert isclose(target.y, 100, abs_tol=delta)
    await async_sleep(.25)
    assert target.x == 300
    assert isclose(target.y, 200, abs_tol=delta)


@async_run(app_cls_func=basic_app)
async def test_put_other_animation_inside(kivy_app, delta):
    target = kivy_app.root.ids.target
    anim = AnimationBuilder.load_string(textwrap_dedent('''
        move_to_right:
            x: 300
            d: .5
        main:
            sequence:
                - move_to_right
                - y: 200
                  d: .5
        '''))['main']
    assert target.x == 0
    assert target.y == 0
    anim.start(target)
    await async_sleep(.25)
    assert isclose(target.x, 150, abs_tol=delta)
    assert target.y == 0
    await async_sleep(.25)
    assert isclose(target.x, 300, abs_tol=delta)
    assert isclose(target.y, 0, abs_tol=delta)
    await async_sleep(.25)
    assert target.x == 300
    assert isclose(target.y, 100, abs_tol=delta)
    await async_sleep(.25)
    assert target.x == 300
    assert isclose(target.y, 200, abs_tol=delta)


@async_run(app_cls_func=basic_app)
async def test_parallel_anim(kivy_app, delta):
    target = kivy_app.root.ids.target
    anim = AnimationBuilder.load_string(textwrap_dedent('''
        main:
            P:
                - x: 300
                  d: 1
                - y: 200
                  d: .5
        '''))['main']
    assert target.x == 0
    assert target.y == 0
    anim.start(target)
    await async_sleep(.25)
    assert isclose(target.x, 75, abs_tol=delta)
    assert isclose(target.y, 100, abs_tol=delta)
    await async_sleep(.25)
    assert isclose(target.x, 150, abs_tol=delta)
    assert isclose(target.y, 200, abs_tol=delta)
    await async_sleep(.25)
    assert isclose(target.x, 225, abs_tol=delta)
    assert target.y == 200
    await async_sleep(.25)
    assert isclose(target.x, 300, abs_tol=delta)
    assert target.y == 200


def test_init():
    anims = AnimationBuilder.load_string(textwrap_dedent('''
        __init__: |
            import random
            def func():
                return 100
            value = 400
        '''))
    available_ids = set(anims.locals.keys()) | (anims.globals.keys())
    assert available_ids == {
        'random', 'func', 'value', '__builtins__',
    }


def test_init_and_eval():
    anim = AnimationBuilder.load_string(textwrap_dedent('''
        __init__: |
            def func():
                return 100
            value = 200
        main:
            x: value + func()
        '''))['main']
    assert anim._animated_properties == {'x': 300, }
    