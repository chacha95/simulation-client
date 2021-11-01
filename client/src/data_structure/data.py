from collections import deque
import sys


class CustomQueue:
    def __init__(self, size: int) -> None:
        self.size: int = size
        self.que: deque = deque()

    def __len__(self) -> int:
        return len(self.que)

    def push(self, data: dict) -> None:
        if len(self.que) == self.size:
            self.que.popleft()
        self.que.append(data)

    def pop(self):
        if len(self.que) == 0:
            print("[queue empty error]")
            sys.exit()
        return self.que.popleft()
