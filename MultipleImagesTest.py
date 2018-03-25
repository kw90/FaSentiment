__author__ = 'kai'

import unittest


class MultipleImagesTestCase(unittest.TestCase):
    def testAllImagesInFolder(self):
        main = Main('test')
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
