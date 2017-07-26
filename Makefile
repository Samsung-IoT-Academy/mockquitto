MODULE = mockquitto
VERSION != awk -F "'" '{print $$2}' $(MODULE)/version.py

PYENV_EXIST != command -v pyenv 2> /dev/null
ifdef PYENV_EXIST
PYENV_VENV_EXIST := $(shell find $$(pyenv root)/plugins -name "pyenv-virtualenv" \
	| head -1 | awk -F "/" '{print $$NF}')
endif

VENV_NAME ?= $(MOUDLE)-test-venv-system
ENV_RESTORE = 0
ENV_NAME_OLD = ""

# ---------------------------------------------------------------------------- #

.PHONY:
	build test-dist-deploy dist-deploy venv_check install clean-build clean-dist

build:
	python setup.py bdist_wheel sdist


install: venv_check
	pip uninstall $(MODULE)
	pip install dist/$(MODULE)-$(VERSION)-py3-none-any.whl

ifeq ($(ENV_RESTORE), 1)
	pyenv deactivate
	pyenv activate $(ENV_NAME_OLD)
endif

venv_check:
ifdef $(PYENV_EXIST)
ifdef $(PYENV_VENV_EXIST)
	ENV_NAME_OLD != pyenv version-name
ifneq ($(ENV_NAME_OLD), $(VENV_NAME))
	pyenv deactivate
	pyenv activate $(VENV_NAME)
	ENV_RESTORE = 1
endif
endif
endif

clean-build:
	rm -rf build/*

clean-dist:
	rm -rf dist/*

dist-deploy:
	twine upload -s --sign-with gpg2 dist/$(MODULE)-$(VERSION)*

test-dist-deploy:
	twine upload -s --sign-with gpg2 -r testpypi dist/$(MODULE)-$(VERSION)*