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

import unittest  # pytest takes ages to run anything as soon as anything from zef is imported
from zef import *
from zef.ops import *


class MyTestCase(unittest.TestCase):
    def test_local_func(self):
        @func
        def adder(x, y=1):
            return x + y

        self.assertEqual(5 | adder | collect, 6)
        self.assertEqual(5 | adder[2] | collect, 7)

    def test_g_func(self):
        g = Graph()

        @func(g)
        def adder(x, y=1):
            return x + y

        self.assertEqual(5 | func[adder] | collect, 6)
        self.assertEqual(5 | func[adder][2] | collect, 7)

if __name__ == '__main__':
    unittest.main()
