import unittest
from detector import FrameProcessor


class MyTestCase(unittest.TestCase):

    def test_the_cat_white(self):
        fp = FrameProcessor()
        det = fp.process_single_frame("test_images/white.jpg")
        print("detected white = " + str(det))
        self.assertEqual(det, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
