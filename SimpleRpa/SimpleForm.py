import Mouse
import ctypes
from ctypes import wintypes
from Mouse import Btn, Tweening

#user32 = ctypes.windll.user32


class WinStates:
    NORMAL = 9
    MINIMIZED = 6
    MAXIMIZED = 3


class Form:
    _handle = 0
    _title = None
    _left = 0
    _top = 0
    _width = 0
    _height = 0
    _transparency = 0
    _stay_on_top = False
    _window_state = None
    controls = list()

    def __init__(self, title):
        self._title = title
        self._handle = user32.FindWindowW(None, title)
        if self._handle == 0:
            raise Exception("Unable to find window with title '" + title + "'.")

    def __getitem__(self, item):
        raise Exception('Not implemented')

    def __setitem__(self, item):
        raise Exception('Not implemented')

    @property
    def left(self):
        self._get_size()
        return self._left

    @left.setter
    def left(self, l):
        if not isinstance(l, int):
            raise TypeError('Expected an int')
        self._get_size()
        user32.MoveWindow(self._handle, l, self._top, self._width, self._height, True)

    @property
    def top(self):
        self._get_size()
        return self._top

    @top.setter
    def top(self, t):
        if not isinstance(t, int):
            raise TypeError('Expected an int')
        self._get_size()
        user32.MoveWindow(self._handle, self._left, t, self._width, self.height, True)

    @property
    def width(self):
        self._get_size()
        return self._width

    @width.setter
    def width(self, w):
        if not isinstance(w, int):
            raise TypeError('Expected an int')
        self._get_size()
        user32.MoveWindow(self._handle, self._left, self._top, w, self.height, True)

    @property
    def height(self):
        self._get_size()
        return self._height

    @height.setter
    def height(self, h):
        if not isinstance(h, int):
            raise TypeError('Expected an int')
        self._get_size()
        user32.MoveWindow(self._handle, self._left, self._top, self._width, h, True)

    @property
    def windows_state(self):
        return self._window_state  #TODO: We should figure out how to PINVOKE this instead of relying on the last set value.

    @windows_state.setter
    def windows_state(self, value):
        if not isinstance(value, int):
            raise TypeError('Expected an int')
        self._window_state = value
        user32.ShowWindow(self._handle, value)

    def hide(self):
        user32.ShowWindow(self._handle, 0)

    def show(self):
        user32.ShowWindow(self._handle, 1)

    def activate(self):
        user32.SetForegroundWindow(self._handle)

    def close(self):
        user32.SendMessageW(self._handle, 0x0112, 0xF060, 0)

    def click(self, pt, clicks=1, interval=0.0, button=Btn.PRIMARY, duration=0, tween=Tweening.LINEAR, log_screenshot=False, use_widget=False):
        self.activate()
        self._get_size()
        pnt = (self._left + pt[0], self.top + pt[1])
        Mouse.click(pnt, clicks, interval, button, duration, tween, log_screenshot, use_widget)

    def _get_size(self):
        rect = wintypes.RECT()
        resp = user32.GetWindowRect(self._handlehandle, ctypes.pointer(rect))
        if resp != 1:
            raise Exception("Window not found.")
        self._left = rect.left
        self._top = rect.top
        self._width = rect.right
        self._height = rect.bottom


class Control:
    _name = None
    _id = None
    _text = None
    _enabled = None
    _visible = None
    _checked = None

    def __init__(self, name, id):
        self._name = name
        self._name = id

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected an str')
        self._text = value

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if not isinstance(value, bool):
            raise TypeError('Expected an bool')
        self._enabled = value

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        if not isinstance(value, bool):
            raise TypeError('Expected an bool')
        self._visible = value

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, value):
        if not isinstance(value, bool):
            raise TypeError('Expected an bool')
        self._checked = value

    def click(self):
        raise Exception('Not implemented')

    def focus(self):
        raise Exception('Not implemented')

    def set_text(self):
        raise Exception('Not implemented')

    def get_text(self):
        raise Exception('Not implemented')
