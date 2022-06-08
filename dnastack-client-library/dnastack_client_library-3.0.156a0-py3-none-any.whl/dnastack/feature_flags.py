import sys
from dnastack.common.environments import flag

in_global_debug_mode = flag('DNASTACK_DEBUG')
in_interactive_shell = sys.__stdout__ and sys.__stdout__.isatty()
detailed_error = flag('DETAILED_ERROR')