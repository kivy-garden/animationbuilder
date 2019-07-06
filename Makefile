PYTHON = python
PYTEST = $(PYTHON) -m pytest

test:
	env KIVY_EVENTLOOP=trio $(PYTEST) ./tests
livepreview:
	mkdir -p ./temp
	$(PYTHON) -m kivy_garden.animationbuilder.livepreview ./temp/test_anim.yaml
