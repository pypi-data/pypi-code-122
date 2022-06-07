import unittest

from preserves import *
from preserves.schema import meta, Compiler

def literal_schema(modname, s):
    c = Compiler()
    c.load_schema((Symbol(modname),), preserve(s))
    return c.root

class BasicSchemaTests(unittest.TestCase):
    def test_dictionary_literal(self):
        m = literal_schema(
            's',
            meta.Schema(
                version = meta.Version(),
                embeddedType = meta.EmbeddedTypeName.false(),
                definitions = meta.Definitions({
                    Symbol('C'): meta.Definition.Pattern(
                        meta.Pattern.CompoundPattern(
                            meta.CompoundPattern.dict(
                                meta.DictionaryEntries({
                                    "core": meta.NamedSimplePattern.anonymous(
                                        meta.SimplePattern.lit(Symbol('true')))
                                }))))
                })))
        self.assertEqual(m.s.C.decode({'core': Symbol('true')}), m.s.C())
        self.assertEqual(preserve(m.s.C()), {'core': Symbol('true')})
