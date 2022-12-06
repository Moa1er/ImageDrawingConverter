import tkinter as tk
import random

list = [1, 2, 3]

def test(idx):
    if idx < len(list) and list[idx] == 3:
        print("nope")
        return list[idx]

    return

print(test(3))