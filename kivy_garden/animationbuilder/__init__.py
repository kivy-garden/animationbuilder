__version__ = '0.0.1dev0'

try:
    from ._animationbuilder import AnimationBuilder
except ImportError:
    from _animationbuilder import AnimationBuilder
