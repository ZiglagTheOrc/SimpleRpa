import ctypes
from ctypes import wintypes
user32 = ctypes.windll.user32


def set_windows_state(handle, state):
    user32.ShowWindow(handle, state)


def hide(handle):
    user32.ShowWindow(handle, 0)


def show(handle):
    user32.ShowWindow(handle, 1)


def activate(handle):
    user32.SetForegroundWindow(handle)


def close(handle):
    user32.SendMessageW(handle, 0x0112, 0xF060, 0)


def get_size(handle):
    rect = wintypes.RECT()
    resp = user32.GetWindowRect(handle, ctypes.pointer(rect))
    if resp != 1:
        raise Exception("Window not found.")
    return (rect.left, rect.top, rect.right, rect.bottom)


def set_size(handle, rect):
    user32.MoveWindow(handle, rect[0], rect[1], rect[2], rect[3], True)
