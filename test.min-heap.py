import unittest

from min_heap import MinHeap

class TestMinHeap(unittest.TestCase):
    def test_empty_heap(self):
        heap = MinHeap()
        self.assertIsNone(heap.peek())
        self.assertIsNone(heap.pop())
        self.assertEqual(len(heap), 0)

    def test_single_element(self):
        heap = MinHeap()
        heap.append(10)
        self.assertEqual(heap.peek(), 10)
        self.assertEqual(len(heap), 1)
        self.assertEqual(heap.pop(), 10)
        self.assertEqual(len(heap), 0)

    def test_heap_order(self):
        elements = [5, 3, 8, 1, 9, 2]
        heap = MinHeap(elements)
        sorted_elements = []
        while len(heap) > 0:
            sorted_elements.append(heap.pop())
        self.assertEqual(sorted_elements, sorted(elements))

    def test_duplicates(self):
        elements = [4, 4, 4, 4]
        heap = MinHeap(elements)
        sorted_elements = [heap.pop() for _ in range(len(heap))]
        self.assertEqual(sorted_elements, [4, 4, 4, 4])

if __name__ == '__main__':
    unittest.main()
