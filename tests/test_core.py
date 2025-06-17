import unittest
from beatmaker.core import BeatMaker

class TestBeatMaker(unittest.TestCase):

    def setUp(self):
        self.beat_maker = BeatMaker()

    def test_load_sounds(self):
        result = self.beat_maker.load_sounds(['kick.wav', 'snare.wav'])
        self.assertTrue(result)
        self.assertEqual(len(self.beat_maker.sounds), 2)

    def test_create_beat(self):
        self.beat_maker.load_sounds(['kick.wav', 'snare.wav'])
        beat = self.beat_maker.create_beat()
        self.assertIsNotNone(beat)

    def test_export_beat(self):
        self.beat_maker.load_sounds(['kick.wav', 'snare.wav'])
        self.beat_maker.create_beat()
        export_result = self.beat_maker.export_beat('test_beat.wav')
        self.assertTrue(export_result)

if __name__ == '__main__':
    unittest.main()