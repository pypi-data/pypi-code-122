from unittest import TestCase

from pykotor.resource.formats.gff import read_gff
from pykotor.resource.generics.are import construct_are, dismantle_are

TEST_FILE = "../../files/test.are"


class TestARE(TestCase):
    def test_io(self):
        gff = read_gff(TEST_FILE)
        are = construct_are(gff)
        self.validate_io(are)

        gff = dismantle_are(are)
        are = construct_are(gff)
        self.validate_io(are)

    def validate_io(self, are):
        self.assertEqual(0, are.unused_id)
        self.assertEqual(0, are.creator_id)
        self.assertEqual("Untitled", are.tag)
        self.assertEqual(75101, are.name.stringref)
        self.assertEqual("comments", are.comment)
        self.assertEqual(0, are.flags)
        self.assertEqual(0, are.mod_spot_check)
        self.assertEqual(0, are.mod_listen_check)
        self.assertEqual(0.20000000298023224, are.alpha_test)
        self.assertEqual(1, are.camera_style)
        self.assertEqual("defaultenvmap", are.default_envmap)
        self.assertEqual("grasstexture", are.grass_texture)
        self.assertEqual(1.0, are.grass_density)
        self.assertEqual(1.0, are.grass_size)
        self.assertEqual(0.25, are.grass_prob_ll)
        self.assertEqual(0.25, are.grass_prob_lr)
        self.assertEqual(0.25, are.grass_prob_ul)
        self.assertEqual(0.25, are.grass_prob_ur)
        self.assertEqual(0, are.moon_ambient)
        self.assertEqual(0, are.moon_diffuse)
        self.assertEqual(0, are.moon_fog)
        self.assertEqual(99.0, are.moon_fog_near)
        self.assertEqual(100.0, are.moon_fog_far)
        self.assertEqual(0, are.moon_fog_color)
        self.assertEqual(0, are.moon_shadows)
        self.assertEqual(1, are.fog_enabled)
        self.assertEqual(99.0, are.fog_near)
        self.assertEqual(100.0, are.fog_far)
        self.assertEqual(1, are.shadows)
        self.assertEqual(0, are.is_night)
        self.assertEqual(0, are.lighting_scheme)
        self.assertEqual(205, are.shadow_opacity)
        self.assertEqual(0, are.day_night)
        self.assertEqual(99, are.chance_rain)
        self.assertEqual(99, are.chance_snow)
        self.assertEqual(99, are.chance_lightning)
        self.assertEqual(1, are.wind_power)
        self.assertEqual(0, are.loadscreen_id)
        self.assertEqual(3, are.player_vs_player)
        self.assertEqual(0, are.no_rest)
        self.assertEqual(0, are.no_hang_back)
        self.assertEqual(0, are.player_only)
        self.assertEqual(1, are.unescapable)
        self.assertEqual(1, are.disable_transit)
        self.assertEqual(1, are.stealth_xp)
        self.assertEqual(25, are.stealth_xp_loss)
        self.assertEqual(25, are.stealth_xp_max)
        self.assertEqual(1, are.dirty_size_1)
        self.assertEqual(1, are.dirty_formula_1)
        self.assertEqual(1, are.dirty_func_1)
        self.assertEqual(1, are.dirty_size_2)
        self.assertEqual(1, are.dirty_formula_2)
        self.assertEqual(1, are.dirty_func_2)
        self.assertEqual(1, are.dirty_size_3)
        self.assertEqual(1, are.dirty_formula_3)
        self.assertEqual(1, are.dirty_func_3)
        self.assertEqual("k_on_enter", are.on_enter)
        self.assertEqual("onexit", are.on_exit)
        self.assertEqual("onheartbeat", are.on_heartbeat)
        self.assertEqual("onuserdefined", are.on_user_defined)

        self.assertEqual(88, are.version)
        self.assertEqual(16777215, are.grass_ambient.bgr_integer())
        self.assertEqual(16777215, are.grass_diffuse.bgr_integer())
        self.assertEqual(16777215, are.sun_ambient.bgr_integer())
        self.assertEqual(16777215, are.sun_diffuse.bgr_integer())
        self.assertEqual(16777215, are.fog_color.bgr_integer())
        self.assertEqual(16777215, are.dynamic_light.bgr_integer())
        self.assertEqual(123, are.dirty_argb_1.bgr_integer())
        self.assertEqual(1234, are.dirty_argb_2.bgr_integer())
        self.assertEqual(12345, are.dirty_argb_3.bgr_integer())

