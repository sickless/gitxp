#! /bin/sh

VERSIONS="2.6.8 2.7.3"
VIRTUALENV_PATH="$HOME/.virtualenvs"

for version in $VERSIONS; do
    . $VIRTUALENV_PATH/$version/bin/activate
    python --version
    python $(dirname $0)/../setup.py install
    python $(dirname $0)/test_gitxp.py
    deactivate
done
