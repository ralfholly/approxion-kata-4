#!/usr/bin/env python3

#
# Part 1 of struct size kata, see https://www.approxion.com/?p=1699
#

import unittest

def struct_size(elems):
    """ Computes the total size of a given struct assuming base-2 alignment.
    elems -- Ordered list of struct member sizes. Returns Total size of struct.
    """

    print("---------")
    # Assume 8 is size of 'most-aligned' data type (e. g. double).
    align_values = {2, 4, 8}
    member_sum = 0
    most_aligned = elems[0]
    for elem in elems:
        pad = 0
        if elem in align_values:
            mod = member_sum % elem
            if mod != 0:
                pad = elem - mod
                most_aligned = max(most_aligned, elem)
        member_sum = member_sum + pad + elem
        print("elem: %d, pad: %d, member_sum: %d" % (elem, pad, member_sum))

    if most_aligned in align_values:
        mod = member_sum % most_aligned
        if mod != 0:
            member_sum += most_aligned - mod
    return member_sum


class TestStructSize(unittest.TestCase):

    def test_power_of_two_member_sizes(self):
        self.assertEquals(1, struct_size([1]))
        self.assertEquals(4, struct_size([1, 1, 1, 1]))
        self.assertEquals(8, struct_size([2, 4]))
        self.assertEquals(8, struct_size([1, 4]))
        self.assertEquals(8, struct_size([1, 1, 1, 4]))
        self.assertEquals(8, struct_size([4, 1]))
        self.assertEquals(12, struct_size([2, 4, 2]))
        self.assertEquals(12, struct_size([1, 4, 2]))
        self.assertEquals(12, struct_size([1, 4, 1]))
        self.assertEquals(12, struct_size([3, 4, 1]))
        self.assertEquals(12, struct_size([4, 4, 1]))
        self.assertEquals(8, struct_size([4, 1, 1, 1]))
        self.assertEquals(8, struct_size([4, 1, 1, 2]))
        self.assertEquals(12, struct_size([4, 1, 1, 1, 2]))

    def test_various_member_sizes(self):
        self.assertEquals(8, struct_size([6, 2]))
        self.assertEquals(6, struct_size([3, 2]))
        self.assertEquals(6, struct_size([1, 3, 2]))
        self.assertEquals(16, struct_size([1, 4, 3, 2]))
        self.assertEquals(5, struct_size([5]))

if __name__ == "__main__":
    unittest.main()

