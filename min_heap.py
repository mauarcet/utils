"""
Min Heap Implementation
"""
import math
from typing import List, Optional

class MinHeap:
    """
    MinHeap
    """
    nodes: List[int]

    def __init__(self, nodes: List[int] = []):
        self.nodes = []
        for node in nodes:
            self.append(node)

    def __len__(self):
        return len(self.nodes)

    def __str__(self):
    	return str(self.nodes)

    def __get_left_child_index(self, parent_index: int) -> int:
        return 2 * parent_index + 1

    def __get_right_child_index(self, parent_index: int) -> int:
        return 2 * parent_index + 2

    def __get_parent_index(self, child_index: int) -> int:
        return (child_index - 1) // 2

    def __has_left_child(self, parent_index: int) -> bool:
        return self.__get_left_child_index(parent_index) < len(self.nodes)

    def __has_right_child(self, parent_index: int) -> bool:
        return self.__get_right_child_index(parent_index) < len(self.nodes)

    def __has_parent(self, child_index: int) -> bool:
        return self.__get_parent_index(child_index) >= 0

    def __left_child(self, index: int) -> Optional[int]:
        if not self.__has_left_child(index):
            return float('inf')
        return self.nodes[self.__get_left_child_index(index)]

    def __right_child(self, index: int) -> Optional[int]:
        if not self.__has_right_child(index):
            return float('inf')
        return self.nodes[self.__get_right_child_index(index)]

    def __parent(self, index: int) -> Optional[int]:
        if not self.__has_parent(index):
            return None
        return self.nodes[self.__get_parent_index(index)]

    def __swap_by_index(self, first_index: int, second_index: int):
        if first_index >= len(self.nodes) or second_index >= len(self.nodes):
            print(f"Invalid indices: {first_index}, {second_index}")
            return
        self.nodes[first_index], self.nodes[second_index] = self.nodes[second_index], self.nodes[first_index]

    def __heapify_up(self, child_index: Optional[int] = None):
        if child_index is None:
            child_index = len(self.nodes) - 1
        parent_index = self.__get_parent_index(child_index)
        if self.__has_parent(child_index) and self.nodes[child_index] < self.__parent(child_index):
            self.__swap_by_index(child_index, parent_index)
            self.__heapify_up(parent_index)

    def __heapify_down(self, index: int = 0):
        if not self.__has_left_child(index):
            return
        smaller_child_index = self.__get_left_child_index(index)
        if (self.__has_right_child(index) and 
                self.__right_child(index) < self.__left_child(index)):
            smaller_child_index = self.__get_right_child_index(index)

        if self.nodes[index] > self.nodes[smaller_child_index]:
            self.__swap_by_index(index, smaller_child_index)
            self.__heapify_down(smaller_child_index)

    def append(self, item: int):
        """Append element to heap"""
        self.nodes.append(item)
        self.__heapify_up()

    def pop(self) -> Optional[int]:
        """Pop first element from heap"""
        if not self.nodes:
            return None
        removed_node = self.nodes[0]
        self.nodes[0] = self.nodes[-1]
        del self.nodes[-1]
        self.__heapify_down()
        return removed_node

    def peek(self) -> Optional[int]:
        if not self.nodes:
            return None
        return self.nodes[0]

if __name__ == '__main__':
    heap = MinHeap([8, 1, 2, 3, 100, 32, 4, 5])
    print(heap)
