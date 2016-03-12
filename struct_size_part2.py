#!/usr/bin/env python3

#
# Part 2 of struct size kata, see https://www.approxion.com/?p=1699
#

import unittest


def struct_size(items):
    """ Computes the total size of a given (potentially nested) struct.
    items -- A list like this:
        items := [ [elem, elem-alignment] + ]
        elem := elem-size | items
        elem-size:= integer
        elem-alignment:= integer
    Returns a 2-element list whose first element is the total size of the
    struct and the second element is the alignment of the most aligned member.
    """

    member_sum = 0
    pad = 0
    most_aligned = 1
    for item in items:
        elem = item[0]
        # If nested struct.
        if isinstance(elem, list):
            elem, align = struct_size(item)
        else:
            align = item[1]
        most_aligned = max(most_aligned, align)
        pad = (align - member_sum % align) % align
        member_sum = member_sum + pad + elem
    pad = (most_aligned - member_sum % most_aligned) % most_aligned
    member_sum += pad
    return [member_sum, most_aligned]

class TestStructSize(unittest.TestCase):

    def test_simple_non_nested_cases(self):
        self.assertEqual([1, 1], struct_size([[1, 1]]))
        self.assertEqual([8, 4], struct_size([[2, 2], [4, 4]]))
        self.assertEqual([8, 2], struct_size([[6, 1], [2, 2]]))
        self.assertEqual([8, 1], struct_size([[6, 1], [2, 1]]))
        self.assertEqual([16, 4], struct_size([[1, 1], [4, 4], [3, 1], [2, 2]]))
        self.assertEqual([16, 4], struct_size([[1, 1], [4, 4], [3, 1], [2, 2]]))

    def test_more_complicated_still_non_nested(self):
        # 1 + 3 (pad) + 32 + 4 + 3 + 1 (pad) + 2 + p2 = 48
        self.assertEqual([48, 4], struct_size([[1, 1], [32, 4], [4, 4], [3, 1], [2, 2]]))
        # 1 + 31 (pad) + 32 + 4 + 3 + 1 (pad) + 2 + 22 (pad) = 96
        self.assertEqual([96, 32], struct_size([[1, 1], [32, 32], [4, 4], [3, 1], [2, 2]]))
        # 1 + 3 (pad) + 32 + 4 + 3 + 1 (pad) + 2 + 2 (pad) = 48
        self.assertEqual([48, 4], struct_size([[1, 1], [32, 1], [4, 4], [3, 1], [2, 2]]))

    def test_nested_cases(self):
        struct_inner = [[1, 1], [2, 2], [4, 4], [1, 1], [3, 1]]
        result_inner = struct_size(struct_inner)
        self.assertEqual([12, 4], result_inner)
        struct_outer = [[1, 1], struct_inner, [3, 1]]
        self.assertEqual([20, 4], struct_size(struct_outer))

    def test_weird_alignment(self):
        self.assertEqual([8, 4], struct_size([[1, 1], [3, 4], [1, 1]]))

if __name__ == "__main__":
    unittest.main()
