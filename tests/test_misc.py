#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mframework._log as log


def test_log():
    log.disable_logger()
    log.enable_logger()


def test_version():
    from mframework.__version__ import __version__
    print(__version__)
