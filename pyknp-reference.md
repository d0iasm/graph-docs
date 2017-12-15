# Pyknp API reference
Python binding of JUMAN and KNP.
Download from [here](http://nlp.ist.i.kyoto-u.ac.jp/index.php?PyKNP).

## Directories Structure
pyknp/
  ├ __init__.py
　├ evaluate/
  │  ├ __init__.py
  │  ├ dep.py
  │  ├ mrph.py
  │  ├ pharase.py
　│　└ scorer.py
  ├ juman/
  │  ├ __init__.py
  │  ├ jumanapp.py
  │  ├ juman.py
  │  ├ mlist.py
  │  ├ morpheme.py
　│　└ simple.py
  ├ knp/
  │  ├ __init__.py
  │  ├ blist.py
  │  ├ bunsetsu.py
  │  ├ drawtree.py
  │  ├ features.py
  │  ├ knp.py
  │  ├ pas.py
  │  ├ rel.py
  │  ├ simple.py
  │  ├ syngraph.py
  │  ├ tag.py
　│　└ tlist.py
　└ scripts/
     └ knp-drawtree
	 

## Import modules
```__init__.py
from pyknp.juman.morpheme import Morpheme
from pyknp.juman.mlist import MList
from pyknp.juman.juman import Juman, Socket, Subprocess
from pyknp.juman.jumanpp import Jumanpp
from pyknp.knp.rel import Rel
from pyknp.knp.pas import Argument, Pas
from pyknp.knp.features import Features
from pyknp.knp.tag import Tag
from pyknp.knp.drawtree import DrawTree
from pyknp.knp.tlist import TList
from pyknp.knp.bunsetsu import Bunsetsu
from pyknp.knp.syngraph import SynNodes, SynNode
from pyknp.knp.blist import BList
from pyknp.knp.knp import KNP
import pyknp.evaluate
```
