#!/usr/bin/env python3
# -*- coding: utf-8 -*-m

import os
from pathlib import Path

from mframework import doc2rst

from aircraft._model import mspec

HERE = os.path.abspath(os.path.dirname(__file__))
doc_path = os.path.join(HERE, 'autodoc')

Path(doc_path).mkdir(parents=True, exist_ok=True)
doc2rst(mspec, doc_path)
