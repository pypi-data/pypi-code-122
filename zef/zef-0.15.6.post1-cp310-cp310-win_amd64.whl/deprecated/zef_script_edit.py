# Copyright 2022 Synchronous Technologies Pte Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import inspect
import pyperclip
import zefdb
from zefdb import *
from zefdb.zefops import *


# Zef functions are different from zef scripts or functions set up in subscriptions.
# ZefScripts come with an implicit execution policy and are automatically executed by zefDB.
# The execution of zef functions, on the other hand, is completely up to the outer context.
# Zefui provides tools to push functions from a scrap python file / repl into the graph
# and load them from a graph by generating code and comments that is copied to the clipboard.

def rae_type(z):
    """Given any """
    if BT(z)==BT.ENTITY_NODE:
        return ET(z)
    elif BT(z)==BT.RELATION_EDGE:
        return RT(z)
    elif BT(z)==BT.ATOMIC_ENTITY_NODE:
        return AET(z)
    else:
        return BT(z)    # e.g. for tx nodes, graph root nodes etc. 





def attach_zef_script_python(z, *args, **kwargs):
    """
    Changing up temporarily
    """
    def inner(func):
        """one more layer of indirection is needed if we want to create a decorator that takes arguments"""
        assert isinstance(z, zefdb.ZefRef) or isinstance(z, zefdb.EZefRef)
        
        def is_zef_function_name(fct_name: str)->bool:
            if len(fct_name) != 45:
                return False
            if fct_name[0:13] != 'zef_function_':
                return False
            uid_maybe = fct_name[13:]
            if not set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
                ).issuperset(set(uid_maybe)):
                return False
            return True
        
        s_full = inspect.getsource(func)        
        s = s_full[s_full.find('\n')+1:]

        g = Graph(z)
        with Transaction(g):
            z_python_str = (z| now) >> O[RT.ZEF_Python]
            if z_python_str is None:
                z | attach[RT.ZEF_Python, s]
            else:
                # zef function already exists. matching up
                if (z_python_str | value.String) != s:
                    z_python_str <= s
                
        return func
    
    return inner
        






def get_zef_python_scripts(z: ZefRef, policy: str):
    # z: ZefRef to root of graph with time slice. We could extend this to being a ZefRef to any RAE to which a zef function is attached? Maybe also lists of RAEs?
    assert isinstance(policy, str)
    assert isinstance(z, ZefRef)
    g = Graph(z) 
    def make_header(z: ZefRef)->str:
        return f"""
# ------------------------        this code snippet was generated by              -------------------------------
# ------------------------ zefui.get_zef_python_scripts at {str(now())} -------------------------------
# origin: first created by {'-- ZefDB user --'} at ...
# last change: by -- ZefDB user -- ...
# g = Graph("{uid(g)}")       tagged with {g.tags}       # Zef function lives on this graph
# z = g["{z | uid}"]
@attach_zef_script_python(g["{z | uid}"])
"""    
    
    zrs_candidates = g | instances[now][ET.ZEF_Script]
    # keep as data before flattening out: allow sorting and other processing
    my_list = []
    #found = blobs(g) | filter[RT.RawPythonFunction] | filter[lambda z: not internals.is_delegate(z)]    
    for z in zrs_candidates:
        z_str = z >> O[RT.ZEF_Python]
        if z_str is None:
            continue
        assert AET(z_str) == AET.String        
        my_list.append(make_header(z) + (z_str | value))
    if policy=='to_clipboard':
        pyperclip.copy("\n\n\n".join(my_list))   # copy to clipboard
