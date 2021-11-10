from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import pymol
from pymol import cmd, testing, stored

# spectrum produces colors which are wrong in the second digit
get_color_tuple = lambda c, n=1: tuple([round(x, n) for x in cmd.get_color_tuple(c)])

class TestUtil(testing.PyMOLTestCase):

    _color_by_area_cache = {}

    @testing.foreach('molecular', 'solvent')
    @testing.requires_version('1.9.0')
    def test_color_by_area(self, mode):
        cmd.fragment('tyr')
        cmd.color('white')
        pymol.util.color_by_area('*', mode, palette='blue_white_red')
        stored.colors = set()
        cmd.iterate('*', 'stored.colors.add(color)')
        colors = [get_color_tuple(c) for c in sorted(stored.colors)]
        self.assertTrue((1., 0., 0.) in colors)
        self.assertTrue((0., 0., 1.) in colors)

        # compare with other mode
        self._color_by_area_cache[mode] = colors
        colors_mode_other = self._color_by_area_cache.get(
                'molecular' if mode == 'solvent' else 'solvent')
        self.assertNotEqual(colors, colors_mode_other)

    @testing.requires_version('1.7.2')
    def test_find_surface_residues(self):
        pymol.util.find_surface_residues
        self.skipTest("TODO")

    def test_find_surface_atoms(self):
        pymol.util.find_surface_atoms
        self.skipTest("TODO")

    @testing.requires_version('1.7.2')
    def test_get_area(self):
        pymol.util.get_area
        self.skipTest("TODO")

    def test_get_sasa(self):
        pymol.util.get_sasa
        self.skipTest("TODO")

    def test_mass_align(self):
        pymol.util.mass_align
        self.skipTest("TODO")

    def test_sum_formal_charges(self):
        pymol.util.sum_formal_charges
        self.skipTest("TODO")

    def test_sum_partial_charges(self):
        pymol.util.sum_partial_charges
        self.skipTest("TODO")

    def test_compute_mass(self):
        pymol.util.compute_mass
        self.skipTest("TODO")

    def test_protein_assign_charges_and_radii(self):
        pymol.util.protein_assign_charges_and_radii
        self.skipTest("TODO")

    def test_protein_vacuum_esp(self):
        pymol.util.protein_vacuum_esp
        self.skipTest("TODO")

    def test_color_carbon(self):
        pymol.util.color_carbon
        self.skipTest("TODO")

    def test_cbss(self):
        cmd.load(self.datafile('1oky-frag.pdb'))
        c = [2, 13, 22] # blue orange forest
        pymol.util.cbss('*', *c)
        stored.colors = set()
        cmd.iterate('*', 'stored.colors.add((ss or "L", color))')
        self.assertEqual(stored.colors, set(zip('HSL', c)))

    def _test_cba(self, fun, expected_color):
        cmd.fragment('gly')
        cmd.color('white')
        fun('*')
        stored.colors = set()
        cmd.iterate('elem C', 'stored.colors.add(color)')
        colors = [get_color_tuple(c, 3) for c in stored.colors]
        self.assertEqual(colors, [expected_color])

    def test_cbag(self):
        self._test_cba(pymol.util.cbag, (0.2, 1.0, 0.2))

    def test_cbac(self):
        self._test_cba(pymol.util.cbac, (0.0, 1.0, 1.0))

    def test_cbam(self):
        self._test_cba(pymol.util.cbam, (1.0, 0.2, 0.8))

    def test_cbay(self):
        self._test_cba(pymol.util.cbay, (1.0, 1.0, 0.0))

    def test_cbas(self):
        self._test_cba(pymol.util.cbas, (1.0, 0.6, 0.6))

    def test_cbaw(self):
        self._test_cba(pymol.util.cbaw, (0.9, 0.9, 0.9))

    def test_cbab(self):
        self._test_cba(pymol.util.cbab, (0.5, 0.5, 1.0))

    def test_cbao(self):
        self._test_cba(pymol.util.cbao, (1.0, 0.7, 0.2))

    def test_cbap(self):
        self._test_cba(pymol.util.cbap, (0.75, 0.0, 0.75))

    def test_cbak(self):
        self._test_cba(pymol.util.cbak, (1.0, 0.65, 0.85))

    def test_cnc(self):
        pymol.util.cnc
        self.skipTest("TODO")

    def test_cba(self):
        pymol.util.cba
        self.skipTest("TODO")

    def test_cbh(self):
        pymol.util.cbh
        self.skipTest("TODO")

    def test_enable_all_shaders(self):
        pymol.util.enable_all_shaders()
        # result depends on whether shaders are available or not

    def test_modernize_rendering(self):
        pymol.util.modernize_rendering(1)  # unused mode argument

    def test_performance(self):
        pymol.util.performance(0)
        self.assertEqual(1, cmd.get_setting_int('surface_quality'))
        self.assertEqual(1, cmd.get_setting_int('depth_cue'))
        pymol.util.performance(33)
        self.assertEqual(0, cmd.get_setting_int('surface_quality'))
        self.assertEqual(1, cmd.get_setting_int('depth_cue'))
        pymol.util.performance(66)
        self.assertEqual(0, cmd.get_setting_int('surface_quality'))
        self.assertEqual(0, cmd.get_setting_int('depth_cue'))
        pymol.util.performance(100)
        self.assertEqual(-1, cmd.get_setting_int('surface_quality'))
        self.assertEqual(0, cmd.get_setting_int('depth_cue'))

    def test_label_chains(self, mode='chain'):
        cmd.load(self.datafile('4m4b-minimal-w-assembly.cif'))
        if mode == 'chain':
            pymol.util.label_chains()
        else:
            pymol.util.label_segments()
        stored.labels = set()
        cmd.iterate('*', 'stored.labels.add(label)')
        self.assertEqual(stored.labels, set(['', mode + ' A', mode + ' B']))

    @testing.requires_version('1.7.2')
    def test_label_segments(self):
        self.test_label_chains('segi')

    def test_cbc(self):
        pymol.util.cbc
        self.skipTest("TODO")

    def test_color_objs(self):
        pymol.util.color_objs
        self.skipTest("TODO")

    def test_chainbow(self):
        pymol.util.chainbow
        self.skipTest("TODO")

    def test_ray_shadows(self):
        pymol.util.ray_shadows
        self.skipTest("TODO")

    def test_ff_copy(self):
        pymol.util.ff_copy
        self.skipTest("TODO")

    def test_b2vdw(self):
        pymol.util.b2vdw
        self.skipTest("TODO")

    def test_phipsi(self):
        pymol.util.phipsi
        self.skipTest("TODO")

    def test_rainbow(self):
        pymol.util.rainbow
        self.skipTest("TODO")

    def test_ss(self):
        pymol.util.ss
        self.skipTest("TODO")

    def test_colors(self):
        cmd.fragment('gly')
        pymol.util.colors("jmol")
        stored.colors = set()
        cmd.iterate('elem C', 'stored.colors.add(color)')
        colors = [get_color_tuple(c, 3) for c in stored.colors]
        self.assertEqual(colors, [(0.567, 0.567, 0.567)])

    @testing.requires_version('1.7.6')
    def test_interchain_distances(self):
        pymol.util.interchain_distances
        self.skipTest("TODO")

    @testing.requires_version('1.8.0')
    def test_get_sasa_relative(self):
        cmd.load(self.datafile('1oky-frag.pdb'))
        r = cmd.get_sasa_relative()
        self.assertAlmostEqual(r['1oky-frag', '', 'A', '86'], 0.708, delta=1e-3)
        r = cmd.get_sasa_relative("resi 86")
        self.assertAlmostEqual(r['1oky-frag', '', 'A', '86'], 0.708, delta=1e-3)

    @testing.requires_version('2.6')
    def test_get_sasa_relative_subsele(self):
        cmd.load(self.datafile('1oky-frag.pdb'))
        r = cmd.get_sasa_relative(subsele="sidechain")
        self.assertAlmostEqual(r['1oky-frag', '', 'A', '86'], 0.812, delta=1e-3)
        r = cmd.get_sasa_relative("resi 86", subsele="sidechain")
        self.assertAlmostEqual(r['1oky-frag', '', 'A', '86'], 0.812, delta=1e-3)

    @testing.requires_version('1.8.6')
    def test_ligand_zoom(self):
        pymol.util.ligand_zoom
        self.skipTest("TODO")
