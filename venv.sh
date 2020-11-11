#!/usr/bin/env bash

DIRECTORY=virtualenvs/.cuppon
deactivate 2 > /dev/null
if [ -d "${DIRECTORY}" ]; then
    source ${DIRECTORY}/bin/activate
else
    virtualenv -p `which python` ${DIRECTORY}
    source ${DIRECTORY}/bin/activate
fi
