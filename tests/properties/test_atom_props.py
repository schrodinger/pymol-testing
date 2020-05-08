
'''
Testing atom properties for simple getting/setting and loading from sdf and mae files
'''

import unittest
from pymol import cmd, testing, stored

@testing.requires('properties')
class TestAtomProperties(testing.PyMOLTestCase):

    def testSetNoAtomProperty(self):
        try:
            cmd.set_atom_property('test_prop', 1, "index 1")
        except:
            self.assertEqual(False, True)
            pass

    @testing.foreach('1molecule.mae')
    def testLoadNoProperties(self, molfilename):
        cmd.set('load_object_props_default', '')
        cmd.load(self.datafile(molfilename), 'test')
        objs = cmd.get_object_list()
        for obj in objs:
            prop_list= cmd.get_property_list(obj)
            self.assertEquals(prop_list, None)

    @testing.foreach('1molecule.mae')
    def testLoadNoAtomProperties(self, molfilename):
        cmd.set('load_atom_props_default', '')
        cmd.load(self.datafile(molfilename), 'test', object_props='*')
        objs = cmd.get_object_list()
        for obj in objs:
            stored.prop_lookup = {}
            self.assertEquals(cmd.count_atoms(obj) > 0, True)
            cmd.iterate(obj, "stored.prop_lookup[index-1] = properties.all")
            for i in stored.prop_lookup.keys():
                self.assertEquals(len(stored.prop_lookup[i]), 0)

    @testing.foreach('1molecule.mae', '1d_smiles.mae')
    def testMAEchempy(self, molfilename):
        cmd.load(self.datafile(molfilename), 'test', object_props='*', atom_props='*')
        objs = cmd.get_object_list()
        for obj in objs:
            idxToVal = {}
            natoms = cmd.count_atoms(obj)
            for i in range(natoms):
                idxToVal[i+1] = i*10
                cmd.set_atom_property('test_prop', i*10, "index %d and %s" % (i+1, obj))
            model = cmd.get_model(obj)

            # test to make sure the properties that exist are the same
            prop_list= cmd.get_property_list(obj)
            mol_prop_list = [x[0] for x in model.molecule_properties]
            self.assertEqual(set(prop_list), set(mol_prop_list))

            # need to test whether the values are the same
            for prop, val in model.molecule_properties:
                propval = cmd.get_property(prop, obj)
                self.assertEqual(propval, val)

            self.assertEqual(natoms, len(model.atom))

            # need to test values of all atom properties, including the ones that were set above
            stored.prop_lookup = {}
            cmd.iterate(obj, "stored.prop_lookup[index-1] = properties.all")
            idx = 0
            for at in model.atom:
                for prop in at.atom_properties.keys():
                    val = at.atom_properties[prop]
                    self.assertEqual(val, stored.prop_lookup[idx][prop])
                idx += 1

    def testMAEsaveLoadSessionsWithAtomProperties(self, binary_dump=False):
        cmd.set('pse_binary_dump', binary_dump)
        cmd.load(self.datafile('1molecule.mae'), '1molecule', atom_props='*')
        allpropdata = {}
        objs = cmd.get_object_list()
        stored.prop_lookup = {}
        for obj in objs:
            stored.prop_lookup[obj] = {}
            cmd.iterate(obj, "stored.prop_lookup['%s'][index-1] = properties.all" % obj)
        prop_lookup = stored.prop_lookup
        with testing.mktemp('.pse') as psefilename:
            cmd.save(psefilename)
            cmd.load(psefilename)
        stored.prop_lookup = {}
        for obj in objs:
            stored.prop_lookup[obj] = {}
            cmd.iterate(obj, "stored.prop_lookup['%s'][index-1] = properties.all" % obj)
        #test to make sure the properties are exactly the same from the saved session as the loaded session
        self.assertEqual(prop_lookup, stored.prop_lookup)

    @testing.requires_version('2.4')
    def testMAEsaveLoadSessionsWithAtomPropertiesBinaryDump(self):
        cmd.set('pse_export_version', 2.4)
        self.testMAEsaveLoadSessionsWithAtomProperties(True)

    @testing.requires_version('1.8.0.7')
    def testDel(self):
        cmd.pseudoatom('m1')

        stored.keys = []
        cmd.alter('all', 'p.foo = 123')
        cmd.alter('all', 'p.bar = "Hello World"')
        cmd.iterate('all', 'stored.keys = list(sorted(p.all))')
        self.assertEqual(stored.keys, ['bar', 'foo'])

        stored.keys = []
        cmd.alter('all', "del p['foo']")
        cmd.iterate('all', 'stored.keys = list(sorted(p.all))')
        self.assertEqual(stored.keys, ['bar'])

        stored.keys = []
        cmd.alter('all', "p.bar = None")
        cmd.iterate('all', 'stored.keys = list(sorted(p.all))')
        self.assertEqual(stored.keys, [])

        # object-level
        cmd.set_property('bla', 456, 'm1')
        stored.keys = cmd.get_property_list('m1')
        self.assertEqual(stored.keys, ['bla'])
        cmd.set_property('bla', None, 'm1')
        stored.keys = cmd.get_property_list('m1')
        self.assertEqual(stored.keys, [])
