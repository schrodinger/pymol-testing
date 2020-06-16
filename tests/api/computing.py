
from pymol import cmd, testing, stored

@testing.requires('no_edu')
class TestComputing(testing.PyMOLTestCase):

    @testing.requires('incentive')
    def testClean(self):
        cmd.fragment('his')
        xyz1 = cmd.get_model('his').get_coord_list()
        energy = cmd.clean('his')
        xyz2 = cmd.get_model('his').get_coord_list()
        self.assertEqual(len(xyz1), len(xyz2))

        # coords have changed
        self.assertNotEqual(xyz1, xyz2)

        # energy for HIS = 32.73887
        self.assertTrue(30.0 < energy < 35.0)

    @testing.requires("multi_undo")
    def testUndoClean(self):
        cmd.fragment('his')
        xyz1 = cmd.get_model('his').get_coord_list()
        energy = cmd.clean('his')
        xyz2 = cmd.get_model('his').get_coord_list()
        self.assertEqual(len(xyz1), len(xyz2))

        # coords have changed
        self.assertNotEqual(xyz1, xyz2)

        cmd.undo2()
        xyz2 = cmd.get_model('his').get_coord_list()
        self.assertEqual(xyz1, xyz2)

        cmd.redo2()
        xyz2 = cmd.get_model('his').get_coord_list()
        self.assertNotEqual(xyz1, xyz2)

