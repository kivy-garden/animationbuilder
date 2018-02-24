# -*- coding: utf-8 -*-

try:
    from ._animationbuilder import AnimationBuilder
    from ._exception import AnimationBuilderException
except ImportError:
    from _animationbuilder import AnimationBuilder
    from _exception import AnimationBuilderException
