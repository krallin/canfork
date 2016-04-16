#!/usr/bin/env python
import unittest
import os

import canfork


TEST_RESOURCES = os.path.join(os.path.dirname(__file__), "resources")


class TestMemoryMapParser(unittest.TestCase):
    def test_parse_memory_map(self):
        with open(os.path.join(TEST_RESOURCES, "smaps.ok.noreserve")) as f:
            vmas = canfork.parse_memory_map(f)

            self.assertEqual(vmas[0]["Size"], 4)
            self.assertEqual(vmas[1]["Size"], 4)
            self.assertEqual(vmas[3]["Size"], 134217728)

            self.assertFalse("ac" in vmas[0]["VmFlags"])
            self.assertTrue("ac" in vmas[1]["VmFlags"])
            self.assertFalse("ac" in vmas[3]["VmFlags"])

    def test_parse_invalid_memory_map(self):
        with open(os.path.join(TEST_RESOURCES, "meminfo")) as f:
            self.assertRaises(canfork.KernInfoParseException,
                              canfork.parse_memory_map, f)


class TestMeminfoParser(unittest.TestCase):
    def test_parse_meminfo(self):
        with open(os.path.join(TEST_RESOURCES, "meminfo")) as f:
            meminfo = canfork.parse_meminfo(f)
            self.assertEqual(7941748, meminfo["MemTotal"])
            self.assertEqual(7257072, meminfo["MemFree"])
            self.assertEqual(7648156, meminfo["MemAvailable"])

    def test_parse_invalid_meminfo(self):
        with open(os.path.join(TEST_RESOURCES, "smaps.ok.noreserve")) as f:
            self.assertRaises(canfork.KernInfoParseException,
                              canfork.parse_meminfo, f)


class TestMaxVma(unittest.TestCase):
    def test_max_vma_smaps_ok_scattered(self):
        fname = os.path.join(TEST_RESOURCES, "smaps.ok.scattered")
        with open(fname) as f:
            vmas = canfork.parse_memory_map(f)
        self.assertEqual(131072, canfork.max_accounted_vma_size(vmas))

    def test_max_vma_smaps_ok_noreserve(self):
        fname = os.path.join(TEST_RESOURCES, "smaps.ok.noreserve")
        with open(fname) as f:
            vmas = canfork.parse_memory_map(f)
        self.assertEqual(136, canfork.max_accounted_vma_size(vmas))

    def test_max_vma_smaps_ko_scattered(self):
        fname = os.path.join(TEST_RESOURCES, "smaps.ko")
        with open(fname) as f:
            vmas = canfork.parse_memory_map(f)
        self.assertEqual(7733248, canfork.max_accounted_vma_size(vmas))


def main():
    import sys
    sys.exit(unittest.main())


if __name__ == '__main__':
    main()
