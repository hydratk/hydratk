PYTHON_EXE  = /usr/bin/py
PYINSTALLER = tools/pyinstaller-2.0
APP_SOURCE  = src/hydra.py
APP_NAME    = Hydra
APP_VERSION = 0.1.0a

all: build

build:
	@echo Building $(APP_NAME) $(APP_VERSION)
#	$(PYTHON_EXE) $(PYINSTALLER)/PyInstaller/configure.py
#	$(PYTHON_EXE) $(PYINSTALLER)/PyInstaller/makeespec.py --onefile --upx $(APP_SOURCE)
	$(PYTHON_EXE) $(PYINSTALLER)/pyinstaller.py --onefile $(APP_SOURCE)
	@echo Executeble is avalaible in dist directory

clean:
	@echo Cleanup
	rm -rf $(PYINSTALLER)/hydra
	rm -rf build dist
	rm hydra.spec

pre:
	@echo Install Hydra prerequirements
	pypy_pip install -r requirements.txt
	
pypyenv:


allin: