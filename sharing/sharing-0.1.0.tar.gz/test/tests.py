import sharable as sh

from dep1 import set_hop
from dep2 import set_hip

print("tests_1", sh.config)
set_hop()
set_hip()
print("tests_2", sh.config)
