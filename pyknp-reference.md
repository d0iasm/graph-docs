# Pyknp API reference
Python binding of JUMAN and KNP.
Download from [here](http://nlp.ist.i.kyoto-u.ac.jp/index.php?PyKNP).

## Directories Structure
pyknp/  
　├ \_\_init\_\_.py  
　├ evaluate/  
　│　├ __init__.py  
　│　├ dep.py  
　│　├ mrph.py  
　│　├ pharase.py  
　│　└ scorer.py  
　├ juman/  
　│　├ \_\_init\_\_.py  
　│　├ jumanapp.py  
　│　├ juman.py  
　│　├ mlist.py  
　│　├ morpheme.py  
　│　└ simple.py  
　├ knp/  
　│　├ \_\_init\_\_.py  
　│　├ blist.py  
　│　├ bunsetsu.py  
　│　├ drawtree.py  
　│　├ features.py  
　│　├ knp.py  
　│　├ pas.py  
　│　├ rel.py  
　│　├ simple.py  
　│　├ syngraph.py  
　│　├ tag.py  
　│　└ tlist.py  
　└ scripts/  
　　　└ knp-drawtree  
	 

## Import modules
\_\_init\_\_.py
```python
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

## JUMAN simple usage
```python
import pyknp

juman = pyknp.Juman()
test_str = "この文を解析してください。"
print(juman.analysis(test_str)
```

## KNP simple usage
```python
import pyknp

knp = pyknp.KNP()
test_str = "この文を解析してください。"
print(knp.parse(test_str)
```
