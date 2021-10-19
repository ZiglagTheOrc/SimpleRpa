# region License
"""
 * SimplRPA - A simple RPA library for Python and C#
 *
 * This file has been forked from PyAutoGui https://github.com/asweigart/pyautogui
 *
 * Copyright (c) Al Sweigart
 * Modifications (c) as per Git change history
 * Modifications (c) 2021 Ziglag the Orc
 *
 * This Source Code Form is subject to the terms of the Mozilla
 * Public License, v. 2.0. If a copy of the MPL was not distributed
 * with this file, You can obtain one at
 * https://mozilla.org/MPL/2.0/.
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial
 * portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
 * LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
# endregion
from __future__ import absolute_import, division, print_function
from contextlib import contextmanager

import sys
import time
import datetime
import os
import platform
import re
import functools
import collections.abc

import pytweening

collectionsSequence = collections.abc.Sequence  # type: ignore
version = "1.0"
# TODO: TRIM THIS FILE
# region CUSTOM EXCEPTIONS
class SimpleRPAException(Exception):
    """
    SimpleRPA code will raise this exception class for any invalid actions. If SimpleRPA raises some other exception,
    you should assume that this is caused by a bug in SimpleRPA itself. (Including a failure to catch potential
    exceptions raised by SimpleRPA.)
    """

    pass


class FailSafeException(SimpleRPAException):
    """
    This exception is raised by SimpleRPA functions when the user puts the mouse cursor into one of the "failsafe
    points" (by default, one of the four corners of the primary monitor). This exception shouldn't be caught; it's
    meant to provide a way to terminate a misbehaving script.
    """
    pass


class ImageNotFoundException(SimpleRPAException):
    """
    This exception is the SimpleRPA version of PyScreeze's `ImageNotFoundException`, which is raised when a locate*()
    function call is unable to find an image.

    Ideally, `pyscreeze.ImageNotFoundException` should never be raised by SimpleRPA.
    """
# endregion


# region IMPORT TWEANING
try:
    from pytweening import (
        easeInQuad,
        easeOutQuad,
        easeInOutQuad,
        easeInCubic,
        easeOutCubic,
        easeInOutCubic,
        easeInQuart,
        easeOutQuart,
        easeInOutQuart,
        easeInQuint,
        easeOutQuint,
        easeInOutQuint,
        easeInSine,
        easeOutSine,
        easeInOutSine,
        easeInExpo,
        easeOutExpo,
        easeInOutExpo,
        easeInCirc,
        easeOutCirc,
        easeInOutCirc,
        easeInElastic,
        easeOutElastic,
        easeInOutElastic,
        easeInBack,
        easeOutBack,
        easeInOutBack,
        easeInBounce,
        easeOutBounce,
        easeInOutBounce,
    )

    # getLine is not needed.
    # getPointOnLine has been redefined in this file, to avoid dependency on pytweening.
    # linear has also been redefined in this file.
except ImportError:

    def _couldNotImportPyTweening(*unused_args, **unused_kwargs):
        """
        This function raises ``SimpleRPAException``. It's used for the PyTweening function names if the PyTweening
        module failed to be imported.
        :param unused_args:
        :param unsed_kwargs:
        :return:
        """
        raise SimpleRPAException(
            "SimpleRPA was unable to import pytweening. Please install this module to enable the function you tried to call."
        )

    easeInQuad = _couldNotImportPyTweening
    easeOutQuad = _couldNotImportPyTweening
    easeInOutQuad = _couldNotImportPyTweening
    easeInCubic = _couldNotImportPyTweening
    easeOutCubic = _couldNotImportPyTweening
    easeInOutCubic = _couldNotImportPyTweening
    easeInQuart = _couldNotImportPyTweening
    easeOutQuart = _couldNotImportPyTweening
    easeInOutQuart = _couldNotImportPyTweening
    easeInQuint = _couldNotImportPyTweening
    easeOutQuint = _couldNotImportPyTweening
    easeInOutQuint = _couldNotImportPyTweening
    easeInSine = _couldNotImportPyTweening
    easeOutSine = _couldNotImportPyTweening
    easeInOutSine = _couldNotImportPyTweening
    easeInExpo = _couldNotImportPyTweening
    easeOutExpo = _couldNotImportPyTweening
    easeInOutExpo = _couldNotImportPyTweening
    easeInCirc = _couldNotImportPyTweening
    easeOutCirc = _couldNotImportPyTweening
    easeInOutCirc = _couldNotImportPyTweening
    easeInElastic = _couldNotImportPyTweening
    easeOutElastic = _couldNotImportPyTweening
    easeInOutElastic = _couldNotImportPyTweening
    easeInBack = _couldNotImportPyTweening
    easeOutBack = _couldNotImportPyTweening
    easeInOutBack = _couldNotImportPyTweening
    easeInBounce = _couldNotImportPyTweening
    easeOutBounce = _couldNotImportPyTweening
    easeInOutBounce = _couldNotImportPyTweening
# endregion


def raiseSimpleRPAImageNotFoundException(wrappedFunction):
    """
    A decorator that wraps PyScreeze locate*() functions so that the SimpleRPA user sees them raise SimpleRPA's
    ImageNotFoundException rather than PyScreeze's ImageNotFoundException. This is because PyScreeze should be
    invisible to SimpleRPA users.
    :param wrappedFunction:
    :return:
    """

    @functools.wraps(wrappedFunction)
    def wrapper(*args, **kwargs):
        try:
            return wrappedFunction(*args, **kwargs)
        except pyscreeze.ImageNotFoundException:
            raise ImageNotFoundException  # Raise SimpleRPA's ImageNotFoundException.

    return wrapper


#region SCREEN SHOTS TODO: CAN WE JUST USE SCREEN.PY?
try:
    import pyscreeze
    from pyscreeze import center, grab, pixel, pixelMatchesColor, screenshot

    # Change the locate*() functions so that they raise SimpleRPA's ImageNotFoundException instead.
    @raiseSimpleRPAImageNotFoundException
    def locate(*args, **kwargs):
        """

        :param unused_args:
        :param unsed_kwargs:
        :return:
        """
        return pyscreeze.locate(*args, **kwargs)

    locate.__doc__ = pyscreeze.locate.__doc__

    @raiseSimpleRPAImageNotFoundException
    def locateAll(*args, **kwargs):
        """

        :param unused_args:
        :param unsed_kwargs:
        :return:
        """
        return pyscreeze.locateAll(*args, **kwargs)

    locateAll.__doc__ = pyscreeze.locateAll.__doc__

    @raiseSimpleRPAImageNotFoundException
    def locateAllOnScreen(*args, **kwargs):
        """

        :param unused_args:
        :param unsed_kwargs:
        :return:
        """
        return pyscreeze.locateAllOnScreen(*args, **kwargs)

    locateAllOnScreen.__doc__ = pyscreeze.locateAllOnScreen.__doc__

    @raiseSimpleRPAImageNotFoundException
    def locateCenterOnScreen(*args, **kwargs):
        """

        :param unused_args:
        :param unsed_kwargs:
        :return:
        """
        return pyscreeze.locateCenterOnScreen(*args, **kwargs)

    locateCenterOnScreen.__doc__ = pyscreeze.locateCenterOnScreen.__doc__

    @raiseSimpleRPAImageNotFoundException
    def locateOnScreen(*args, **kwargs):
        """

        :param unused_args:
        :param unsed_kwargs:
        :return:
        """
        return pyscreeze.locateOnScreen(*args, **kwargs)

    locateOnScreen.__doc__ = pyscreeze.locateOnScreen.__doc__

    @raiseSimpleRPAImageNotFoundException
    def locateOnWindow(*args, **kwargs):
        """

        :param unused_args:
        :param unsed_kwargs:
        :return:
        """
        return pyscreeze.locateOnWindow(*args, **kwargs)

    locateOnWindow.__doc__ = pyscreeze.locateOnWindow.__doc__


except ImportError:
    # If pyscreeze module is not found, screenshot-related features will simply not work.
    def _couldNotImportPyScreeze(*unused_args, **unsed_kwargs):
        """
        This function raises ``SimpleRPAException``. It's used for the PyScreeze function names if the PyScreeze module failed to be imported.
        :param unused_args:
        :param unsed_kwargs:
        :return:
        """
        raise SimpleRPAException(
            "SimpleRPA was unable to import pyscreeze. (This is likely because you're running a version of Python that Pillow (which pyscreeze depends on) doesn't support currently.) Please install this module to enable the function you tried to call."
        )

    center = _couldNotImportPyScreeze
    grab = _couldNotImportPyScreeze
    locate = _couldNotImportPyScreeze
    locateAll = _couldNotImportPyScreeze
    locateAllOnScreen = _couldNotImportPyScreeze
    locateCenterOnScreen = _couldNotImportPyScreeze
    locateOnScreen = _couldNotImportPyScreeze
    locateOnWindow = _couldNotImportPyScreeze
    pixel = _couldNotImportPyScreeze
    pixelMatchesColor = _couldNotImportPyScreeze
    screenshot = _couldNotImportPyScreeze
#endregion


# region IMPORTS MOUSE INFO
try:
    import mouseinfo

    def mouseInfo():
        """
        Launches the MouseInfo app. This application provides mouse coordinate information which can be useful when
        planning GUI automation tasks. This function blocks until the application is closed.
        :return:
        """
        mouseinfo.MouseInfoWindow()


except ImportError:

    def mouseInfo():
        """
        This function raises SimpleRPAException. It's used for the MouseInfo function names if the MouseInfo module
        failed to be imported.
        :return:
        """
        raise SimpleRPAException(
            "SimpleRPA was unable to import mouseinfo. Please install this module to enable the function you tried to call."
        )
# endregion


def useImageNotFoundException(value=None):
    """
    When called with no arguments, SimpleRPA will raise ImageNotFoundException when the PyScreeze locate*() functions
    can't find the image it was told to locate. The default behavior is to return None. Call this function with no
    arguments (or with True as the argument) to have exceptions raised, which is a better practice.

    You can also disable raising exceptions by passing False for the argument.
    :param value:
    :return:
    """
    if value is None:
        value = True
    # TODO - this will cause a NameError if PyScreeze couldn't be imported:
    try:
        pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = value
    except NameError:
        raise SimpleRPAException("useImageNotFoundException() ws called but pyscreeze isn't installed.")


if sys.platform == "win32":  # PyGetWindow currently only supports Windows.
    try:
        from pygetwindow import (
            Window,
            getActiveWindow,
            getActiveWindowTitle,
            getWindowsAt,
            getWindowsWithTitle,
            getAllWindows,
            getAllTitles,
        )
    except ImportError:
        # If pygetwindow module is not found, those methods will not be available.
        def _couldNotImportPyGetWindow(*unused_args, **unused_kwargs):
            """
            This function raises SimpleRPAException. It's used for the PyGetWindow function names if the PyGetWindow
            module failed to be imported.
            """
            raise SimpleRPAException(
                "SimpleRPA was unable to import pygetwindow. Please install this module to enable the function you tried to call."
            )

        Window = _couldNotImportPyGetWindow
        getActiveWindow = _couldNotImportPyGetWindow
        getActiveWindowTitle = _couldNotImportPyGetWindow
        getWindowsAt = _couldNotImportPyGetWindow
        getWindowsWithTitle = _couldNotImportPyGetWindow
        getAllWindows = _couldNotImportPyGetWindow
        getAllTitles = _couldNotImportPyGetWindow

# region CONSTANTS
KEY_NAMES = [
    "\t",
    "\n",
    "\r",
    " ",
    "!",
    '"',
    "#",
    "$",
    "%",
    "&",
    "'",
    "(",
    ")",
    "*",
    "+",
    ",",
    "-",
    ".",
    "/",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    ":",
    ";",
    "<",
    "=",
    ">",
    "?",
    "@",
    "[",
    "\\",
    "]",
    "^",
    "_",
    "`",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "{",
    "|",
    "}",
    "~",
    "accept",
    "add",
    "alt",
    "altleft",
    "altright",
    "apps",
    "backspace",
    "browserback",
    "browserfavorites",
    "browserforward",
    "browserhome",
    "browserrefresh",
    "browsersearch",
    "browserstop",
    "capslock",
    "clear",
    "convert",
    "ctrl",
    "ctrlleft",
    "ctrlright",
    "decimal",
    "del",
    "delete",
    "divide",
    "down",
    "end",
    "enter",
    "esc",
    "escape",
    "execute",
    "f1",
    "f10",
    "f11",
    "f12",
    "f13",
    "f14",
    "f15",
    "f16",
    "f17",
    "f18",
    "f19",
    "f2",
    "f20",
    "f21",
    "f22",
    "f23",
    "f24",
    "f3",
    "f4",
    "f5",
    "f6",
    "f7",
    "f8",
    "f9",
    "final",
    "fn",
    "hanguel",
    "hangul",
    "hanja",
    "help",
    "home",
    "insert",
    "junja",
    "kana",
    "kanji",
    "launchapp1",
    "launchapp2",
    "launchmail",
    "launchmediaselect",
    "left",
    "modechange",
    "multiply",
    "nexttrack",
    "nonconvert",
    "num0",
    "num1",
    "num2",
    "num3",
    "num4",
    "num5",
    "num6",
    "num7",
    "num8",
    "num9",
    "numlock",
    "pagedown",
    "pageup",
    "pause",
    "pgdn",
    "pgup",
    "playpause",
    "prevtrack",
    "print",
    "printscreen",
    "prntscrn",
    "prtsc",
    "prtscr",
    "return",
    "right",
    "scrolllock",
    "select",
    "separator",
    "shift",
    "shiftleft",
    "shiftright",
    "sleep",
    "space",
    "stop",
    "subtract",
    "tab",
    "up",
    "volumedown",
    "volumemute",
    "volumeup",
    "win",
    "winleft",
    "winright",
    "yen",
    "command",
    "option",
    "optionleft",
    "optionright",
]
KEYBOARD_KEYS = KEY_NAMES  # keeping old KEYBOARD_KEYS for backwards compatibility

# Constants for the mouse button names:
LEFT = "left"
MIDDLE = "middle"
RIGHT = "right"
PRIMARY = "primary"
SECONDARY = "secondary"

# Different keyboard mappings:
# TODO - finish this feature.
# NOTE: Eventually, I'd like to come up with a better system than this. For now, this seems like it works.
QWERTY = r"""`1234567890-=qwertyuiop[]\asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?"""
QWERTZ = r"""=1234567890/0qwertzuiop89-asdfghjkl,\yxcvbnm,.7+!@#$%^&*()?)QWERTZUIOP*(_ASDFGHJKL<|YXCVBNM<>&"""
# endregion


# region IMPORTS PLATFORM SPECIFIC RPA
if sys.platform == "darwin":
    import _Rpa_OSX as platformModule
elif sys.platform == "win32":
    import _Rpa_Win as platformModule
elif sys.platform == "linux":
    import _Rpa_Linux as platformModule
else:
    raise NotImplementedError("Your platform (%s) is not supported by SimpleRPA." % (platform.system()))
# endregion

# region TWEAKABLE SETTINGS
# In seconds. Any duration less than this is rounded to 0.0 to instantly move the mouse.
MINIMUM_DURATION = 0.1

# If sleep_amount is less than MINIMUM_DURATION, time.sleep() will be a no-op and the mouse cursor moves there instantly.
# TODO: This value should vary with the platform. http://stackoverflow.com/q/1133857
MINIMUM_SLEEP = 0.05

# The number of seconds to pause after EVERY public function call. Useful for debugging:
PAUSE = 0.1  # Tenth-second pause by default.

# Interface need some catch up time on darwin (macOS) systems. Possible values probably differ based on your system performance.
# This value affects mouse moveTo, dragTo and key event duration.
# TODO: Find a dynamic way to let the system catch up instead of blocking with a magic number.
DARWIN_CATCH_UP_TIME = 0.01

# If the mouse is over a coordinate in FAILSAFE_POINTS and FAILSAFE is True, the FailSafeException is raised.
# The rest of the points are added to the FAILSAFE_POINTS list at the bottom of this file, after size() has been defined.
# The points are for the corners of the screen, but note that these points don't automatically change if the screen resolution changes.
FAILSAFE = True
FAILSAFE_POINTS = [(0, 0)]

LOG_SCREENSHOTS = False  # If True, save screenshots for clicks and key presses.

# If not None, SimpleRPA deletes old screenshots when this limit has been reached:
LOG_SCREENSHOTS_LIMIT = 10
G_LOG_SCREENSHOTS_FILENAMES = []  # TODO - make this a deque
#endregion

Point = collections.namedtuple("Point", "x y")
Size = collections.namedtuple("Size", "width height")

# region GERNAL METHODS
def is_shift_character(character):
    """
    Returns True if the ``character`` is a keyboard key that would require the shift key to be held down, such as uppercase letters or the symbols on the keyboard's number row.
    :param character:
    :return:
    """
    # NOTE TODO - This will be different for non-qwerty keyboards.
    return character.isupper() or character in set('~!@#$%^&*()_+{}|:"<>?')

def _generic_simple_rpa_checks(wrapped_function):
    """
    A decorator that calls failSafeCheck() before the decorated function and _handlePause() after it.
    :param wrapped_function:
    :return:
    """
    @functools.wraps(wrapped_function)
    def wrapper(*args, **kwargs):
        fail_safe_check()
        returnVal = wrapped_function(*args, **kwargs)
        _handle_pause(kwargs.get("_pause", True))
        return returnVal

    return wrapper


def get_point_on_line(x1, y1, x2, y2, n):
    """
    Plots all tweening points along a line.
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return: tuple
    """
    x = ((x2 - x1) * n) + x1
    y = ((y2 - y1) * n) + y1
    return (x, y)


def linear(n):
    """
    The default tween for all mouse functions.
    :param n:
    :return: float
    """
    # We use this function instead of pytweening.linear for the default tween function just in case pytweening couldn't be imported.
    if not 0.0 <= n <= 1.0:
        raise SimpleRPAException("Argument must be between 0.0 and 1.0.")
    return n


def _handle_pause(_pause):
    """
    A helper function for performing a pause at the end of a SimpleRPA function based on some settings.
    :param _pause: If `_pause` is `True`, then sleep for `PAUSE` seconds (the global pause setting).
    :return: tuple
    """
    if _pause:
        assert isinstance(PAUSE, int) or isinstance(PAUSE, float)
        time.sleep(PAUSE)


def _normalize_xy_args(firstArg, second_arg):
    """
    Returns a `Point` object based on `firstArg` and `secondArg`, which are the first two arguments passed to
    several SimpleRPA functions. If `firstArg` and `secondArg` are both `None`, returns the current mouse cursor
    position.
    :param firstArg:
    :param second_arg:
    :return: void
    """
    if firstArg is None and second_arg is None:
        return position()

    elif isinstance(firstArg, str):
        # If x is a string, we assume it's an image filename to locate on the screen:
        try:
            location = locateOnScreen(firstArg)
            # The following code only runs if pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION is not set to True, meaning that
            # locateOnScreen() returns None if the image can't be found.
            if location is not None:
                return center(location)
            else:
                return None
        except pyscreeze.ImageNotFoundException:
            raise ImageNotFoundException

        return center(locateOnScreen(firstArg))

    elif isinstance(firstArg, collectionsSequence):
        if len(firstArg) == 2:
            # firstArg is a two-integer tuple: (x, y)
            if second_arg is None:
                return Point(int(firstArg[0]), int(firstArg[1]))
            else:
                raise SimpleRPAException(
                    "When passing a sequence for firstArg, secondArg must not be passed (received {0}).".format(
                        repr(second_arg)
                    )
                )
        elif len(firstArg) == 4:
            # firstArg is a four-integer tuple, (left, top, width, height), we should return the center point
            if second_arg is None:
                return center(firstArg)
            else:
                raise SimpleRPAException(
                    "When passing a sequence for firstArg, secondArg must not be passed and default to None (received {0}).".format(
                        repr(second_arg)
                    )
                )
        else:
            raise SimpleRPAException(
                "The supplied sequence must have exactly 2 or exactly 4 elements ({0} were received).".format(
                    len(firstArg)
                )
            )
    else:
        return Point(int(firstArg), int(second_arg))  # firstArg and secondArg are just x and y number values


def _log_screenshot(log_screenshot, func_name, func_args, folder="."):
    """
    A helper function that creates a screenshot to act as a logging mechanism. When a SimpleRPA function is called,
    this function is also called to capture the state of the screen when that function was called.
    :param log_screenshot: If this is `False` (or None and the `LOG_SCREENSHOTS` constant is `False`), no screenshot is taken.
    :param func_name: This argument is a string of the calling function's name. It's used in the screenshot's filename.
    :param func_args: This argument is a string describing the arguments passed to the calling function. It's limited to twelve characters to keep it short.
    :param folder: This argument is the folder to place the screenshot file in, and defaults to the current working directory.
    :return: tuple
    """
    if log_screenshot == False:
        return  # Don't take a screenshot.
    if log_screenshot is None and LOG_SCREENSHOTS == False:
        return  # Don't take a screenshot.

    # Ensure that the "specifics" string isn't too long for the filename:
    if len(func_args) > 12:
        funcArgs = func_args[:12] + "..."

    now = datetime.datetime.now()
    filename = "%s-%s-%s_%s-%s-%s-%s_%s_%s.png" % (
        now.year,
        str(now.month).rjust(2, "0"),
        str(now.day).rjust(2, "0"),
        now.hour,
        now.minute,
        now.second,
        str(now.microsecond)[:3],
        func_name,
        func_args,
    )
    filepath = os.path.join(folder, filename)

    # Delete the oldest screenshot if we've reached the maximum:
    if (LOG_SCREENSHOTS_LIMIT is not None) and (len(G_LOG_SCREENSHOTS_FILENAMES) >= LOG_SCREENSHOTS_LIMIT):
        os.unlink(os.path.join(folder, G_LOG_SCREENSHOTS_FILENAMES[0]))
        del G_LOG_SCREENSHOTS_FILENAMES[0]

    screenshot(filepath)
    G_LOG_SCREENSHOTS_FILENAMES.append(filename)


def position(x=None, y=None):
    """
    Returns the current xy coordinates of the mouse cursor as a two-integer tuple.
    :param x: If not None, this argument overrides the x in the return value.
    :param y: If not None, this argument overrides the y in the return value.
    :return: tuple
    """
    posx, posy = platformModule._position()
    posx = int(posx)
    posy = int(posy)
    if x is not None:  # If set, the x parameter overrides the return value.
        posx = int(x)
    if y is not None:  # If set, the y parameter overrides the return value.
        posy = int(y)
    return Point(posx, posy)


def size():
    """
    Returns the width and height of the screen as a two-integer tuple.
    :return: tuple
    """
    return Size(*platformModule._size())


def onScreen(x, y=None):
    """
    Returns whether the given xy coordinates are on the primary screen or not.

    Note that this function doesn't work for secondary screens.
    :param x: The x position of the mouse event.
    :param y: The y position of the mouse event.
    :return: void
    """
    x, y = _normalize_xy_args(x, y)
    x = int(x)
    y = int(y)

    width, height = platformModule._size()
    return 0 <= x < width and 0 <= y < height
# endregion


# region MOUSE METHODS
"""
NOTE: Although "mouse1" and "mouse2" buttons usually refer to the left and
right mouse buttons respectively, in SimpleRPA 1, 2, and 3 refer to the left,
middle, and right buttons, respectively. This is because Xlib interprets
button 2 as the middle button and button 3 as the right button, so we hold
that for Windows and macOS as well (since those operating systems don't use
button numbers but rather just "left" or "right").
"""


def _normalize_button(button):
    """
    The left, middle, and right mouse buttons are button numbers 1, 2, and 3 respectively. This is the numbering that
    Xlib on Linux uses (while Windows and macOS don't care about numbers; they just use "left" and "right").

    This function takes one of ``LEFT``, ``MIDDLE``, ``RIGHT``, ``PRIMARY``, ``SECONDARY``, ``1``, ``2``, ``3``, ``4``,
    ``5``, ``6``, or ``7`` for the button argument and returns either ``LEFT``, ``MIDDLE``, ``RIGHT``, ``4``, ``5``,
    ``6``, or ``7``. The ``PRIMARY``, ``SECONDARY``, ``1``, ``2``, and ``3`` values are never returned.

    The ``'left'`` and ``'right'`` mouse buttons will always refer to the physical left and right
    buttons on the mouse. The same applies for buttons 1 and 3.

    However, if ``button`` is ``'primary'`` or ``'secondary'``, then we must check if
    the mouse buttons have been "swapped" (for left-handed users) by the operating system's mouse
    settings.

    If the buttons are swapped, the primary button is the right mouse button and the secondary button is the left mouse
    button. If not swapped, the primary and secondary buttons are the left and right buttons, respectively.

    NOTE: Swap detection has not been implemented yet.
    :param button: The mouse button, either 'left', 'middle', or 'right'
    :return: void
    """
    # TODO - The swap detection hasn't been done yet. For Windows, see https://stackoverflow.com/questions/45627956/check-if-mouse-buttons-are-swapped-or-not-in-c
    # TODO - We should check the OS settings to see if it's a left-hand setup, where button 1 would be "right".

    # Check that `button` has a valid value:
    button = button.lower()
    if platform.system() == "Linux":
        # Check for valid button arg on Linux:
        if button not in (LEFT, MIDDLE, RIGHT, PRIMARY, SECONDARY, 1, 2, 3, 4, 5, 6, 7):
            raise SimpleRPAException(
                "button argument must be one of ('left', 'middle', 'right', 'primary', 'secondary', 1, 2, 3, 4, 5, 6, 7)"
            )
    else:
        # Check for valid button arg on Windows and macOS:
        if button not in (LEFT, MIDDLE, RIGHT, PRIMARY, SECONDARY, 1, 2, 3):
            raise SimpleRPAException(
                "button argument must be one of ('left', 'middle', 'right', 'primary', 'secondary', 1, 2, 3)"
            )

    # TODO - Check if the primary/secondary mouse buttons have been swapped:
    if button in (PRIMARY, SECONDARY):
        swapped = False  # TODO - Add the operating system-specific code to detect mouse swap later.
        if swapped:
            if button == PRIMARY:
                return RIGHT
            elif button == SECONDARY:
                return LEFT
        else:
            if button == PRIMARY:
                return LEFT
            elif button == SECONDARY:
                return RIGHT

    # Return a mouse button integer value, not a string like 'left':
    return {LEFT: LEFT, MIDDLE: MIDDLE, RIGHT: RIGHT, 1: LEFT, 2: MIDDLE, 3: RIGHT, 4: 4, 5: 5, 6: 6, 7: 7}[button]


@_generic_simple_rpa_checks
def mouse_down(x=None, y=None, button=PRIMARY, tween=linear, log_screenshot=None, _pause=True):
    """
    Send the mouse down event to the operating system.
    :param x: The x position of the mouse event.
    :param y: The y position of the mouse event.
    :param button: The mouse button, either 'left', 'middle', or 'right'
    :param tween: The tweening function used if the duration is not 0. A linear tween is used by default.
    :param log_screenshot: If true a screen shot is taken during the operation.
    :param _pause: How many seconds in the end of function process. None by default, for no pause in the end of function process.
    :return: void
    """
    button = _normalize_button(button)
    x, y = _normalize_xy_args(x, y)

    _mouse_move_drag("move", x, y, x, y, duration=0, tween=tween)

    _log_screenshot(log_screenshot, "mouseDown", "%s,%s" % (x, y), folder=".")
    platformModule._mouse_down(x, y, button)


@_generic_simple_rpa_checks
def mouse_up(x=None, y=None, button=PRIMARY, tween=linear, log_screenshot=None, _pause=True):
    """
    Send the mouse up event to the operating system.
    :param x: The x position of the mouse event.
    :param y: The y position of the mouse event.
    :param button: The mouse button, either 'left', 'middle', or 'right'
    :param tween: The tweening function used if the duration is not 0. A linear tween is used by default.
    :param log_screenshot: If true a screen shot is taken during the operation.
    :param _pause: How many seconds in the end of function process. None by default, for no pause in the end of function process.
    :return: void
    """
    button = _normalize_button(button)
    x, y = _normalize_xy_args(x, y)

    _mouse_move_drag("move", x, y, x, y, duration=0, tween=tween)

    _log_screenshot(log_screenshot, "mouseUp", "%s,%s" % (x, y), folder=".")
    platformModule._mouse_up(x, y, button)


@_generic_simple_rpa_checks
def click(
    x=None, y=None, clicks=1, interval=0.0, button=PRIMARY, duration=0.0, tween=linear, log_screenshot=None, _pause=True
):
    """
    Clicks the specified button the specified numberoftimes in the specified location.
    :param x: The x position of the mouse to click at.
    :param y: The y position of the mouse to click at.
    :param clicks: The number of clicks to make.
    :param interval: The time to wait between clicks.
    :param button: The mouse button, either 'left', 'middle', or 'right'
    :param duration: The total amount of time the operation should take.
    :param tween: The tweening function used if the duration is not 0. A linear tween is used by default.
    :param log_screenshot: If true a screen shot is taken during the operation.
    :param _pause: How many seconds in the end of function process. None by default, for no pause in the end of function process.
    :return: void
    """
    # TODO: I'm leaving buttons 4, 5, 6, and 7 undocumented for now. I need to understand how they work.
    button = _normalize_button(button)
    x, y = _normalize_xy_args(x, y)

    # Move the mouse cursor to the x, y coordinate:
    _mouse_move_drag("move", x, y, x, y, duration, tween)

    _log_screenshot(log_screenshot, "click", "%s,%s,%s,%s" % (button, clicks, x, y), folder=".")

    if sys.platform == 'darwin':
        for i in range(clicks):
            fail_safe_check()
            if button in (LEFT, MIDDLE, RIGHT):
                platformModule._multiClick(x, y, button, 1, interval)
    else:
        for i in range(clicks):
            fail_safe_check()
            if button in (LEFT, MIDDLE, RIGHT):
                platformModule._click(x, y, button)

            time.sleep(interval)


@_generic_simple_rpa_checks
def scroll(clicks, x=None, y=None, scroll='scroll', log_screenshot=None, _pause=True):
    """
    Performs a scroll of the mouse scroll wheel.

    Whether this is a vertical or horizontal scroll depends on the underlying
    operating system.

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.
    :param clicks: The amount of scrolling to do. A positive value is the mouse wheel moving forward (scrolling up), a negative value is backwards (down).
    :param x: The x position of the mouse event.
    :param y: The y position of the mouse event.
    :param scroll: The type of scroll to perform.
    :param log_screenshot: If true a screen shot is taken during the operation.
    :param _pause: How many seconds in the end of function process. None by default, for no pause in the end of function process.
    :return: void
    """
    if type(x) in (tuple, list):
        x, y = x[0], x[1]
    x, y = position(x, y)

    _log_screenshot(log_screenshot, "scroll", "%s,%s,%s" % (clicks, x, y), folder=".")
    platformModule._scroll(clicks, x, y)


@_generic_simple_rpa_checks
def move_to(x=None, y=None, duration=0.0, tween=linear, log_screenshot=False, _pause=True):
    """
    Moves the mouse cursor to a point on the screen.

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    :param x: The x position on the screen where the click happens. None by default. If tuple, this is used for x and y. If x is a str, it's considered a filename of an image to find on the screen with locateOnScreen() and click the center of.
    :param y: The y position on the screen where the click happens. None by default.
    :param duration: The amount of time the operation should take to ocmplete.
    :param tween: The tweening function used if the duration is not 0. A linear tween is used by default.
    :param log_screenshot: If true a screen shot is taken during the operation.
    :param _pause: How many seconds in the end of function process. None by default, for no pause in the end of function process.
    :return: void
    """
    x, y = _normalize_xy_args(x, y)

    _log_screenshot(log_screenshot, "moveTo", "%s,%s" % (x, y), folder=".")
    _mouse_move_drag("move", x, y, x, y, duration, tween)


@_generic_simple_rpa_checks
def drag_to(
    x=None, y=None, duration=0.0, tween=linear, button=PRIMARY, log_screenshot=None, _pause=True, mouse_down_up=True
):
    """
    Performs a mouse drag (mouse movement while a button is held down) to a
    point on the screen.

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.
    :param x: The x point on the screen to move to and mouse down from.
    :param y: The y point on the screen to move to and mouse down from.
    :param button: The mouse button, either 'left', 'middle', or 'right'
    :param duration: The amount of time the operation should take to ocmplete.
    :param tween: The tweening function used if the duration is not 0. A linear tween is used by default.
    :param button: The mouse button press and release.
    :param log_screenshot: If true a screen shot is taken during the operation.
    :param _pause: How many seconds in the end of function process. None by default, for no pause in the end of function process.
    :param mouse_down_up: When true, the mouseUp/Down actions are not performed. Which allows dragging over multiple (small) actions. 'True' by default.
    :return: void
    """
    x, y = _normalize_xy_args(x, y)

    _log_screenshot(log_screenshot, "dragTo", "%s,%s" % (x, y), folder=".")
    if mouse_down_up:
        mouse_down(button=button, logScreenshot=False, _pause=False)
    _mouse_move_drag("drag", x, y, x, y, duration, tween, button)
    if mouse_down_up:
        mouse_up(button=button, logScreenshot=False, _pause=False)


def _mouse_move_drag(move_or_drag, x1, y1, x2, y2, duration, tween=linear, button=LEFT, log_screenshot=False):
    """
    Handles the actual move or drag event, since different platforms
    implement them differently.

    On Windows & Linux, a drag is a normal mouse move while a mouse button is
    held down. On OS X, a distinct "drag" event must be used instead.

    The code for moving and dragging the mouse is similar, so this function
    handles both. Users should call the moveTo() or dragTo() functions instead
    of calling _mouseMoveDrag().
    :param move_or_drag: Either 'move' or 'drag', for the type of action this is.
    :param x1: The first x point on the screen to move to and mouse down from.
    :param y1: The first y point on the screen to move to and mouse down from.
    :param x2: The second x point on the screen to move to and mouse down from.
    :param y2: The second y point on the screen to move to and mouse down from.
    :param duration: The amount of time the operation should take to ocmplete.
    :param tween: The tweening function used if the duration is not 0. A linear tween is used by default.
    :param button: The mouse button press and release.
    :param log_screenshot: If true a screen shot is taken during the operation.
    :return: void
    """
    # The move and drag code is similar, but OS X requires a special drag event instead of just a move event when dragging.
    # See https://stackoverflow.com/a/2696107/1893164
    assert move_or_drag in ("move", "drag"), "moveOrDrag must be in ('move', 'drag'), not %s" % (move_or_drag)
    duration = duration / 2

    moveOrDrag = move_or_drag
    if sys.platform == "darwin":
        moveOrDrag = "osx_move"  # Only OS X needs the drag event specifically.

    start_x, start_y = position()
    width, height = size()

    # Make sure x and y are within the screen bounds.
    # x = max(0, min(x, width - 1))
    # y = max(0, min(y, height - 1))

    # If the duration is small enough, just move the cursor there instantly.
    steps = [(x1, y1)]

    if duration > MINIMUM_DURATION:
        # Non-instant moving/dragging involves tweening:
        num_steps = max(width, height)
        sleep_amount = duration / num_steps
        if sleep_amount < MINIMUM_SLEEP:
            num_steps = int(duration / MINIMUM_SLEEP)
            sleep_amount = duration / num_steps

        steps = [get_point_on_line(start_x, start_y, x1, y1, tween(n / num_steps)) for n in range(num_steps)]
        # Making sure the last position is the actual destination.
        steps.append((x2, y2))

    idx = 0
    for tweenX, tweenY in steps:
        idx += 1
        if len(steps) > 1:
            # A single step does not require tweening.
            time.sleep(sleep_amount)

        tweenX = int(round(tweenX))
        tweenY = int(round(tweenY))

        # Do a fail-safe check to see if the user moved the mouse to a fail-safe position, but not if the mouse cursor
        # moved there as a result of this function. (Just because tweenX and tweenY aren't in a fail-safe position
        # doesn't mean the user couldn't have moved the mouse cursor to a fail-safe position.)
        if (tweenX, tweenY) not in FAILSAFE_POINTS:
            fail_safe_check()

        if moveOrDrag == "move":
            platformModule._move_to(tweenX, tweenY)
        elif moveOrDrag == "drag":
            platformModule._move_to(tweenX, tweenY)
            if idx == len(steps) - 1:
                platformModule._move_to(x1, y1)
                mouse_down(x1, y1, button, tween, log_screenshot, True)
                move_to(x2, y2, duration/2, tween, log_screenshot, True)
                mouse_up(x2, y2, button, tween, log_screenshot, True)
        elif moveOrDrag == "osx_drag":
            platformModule._drag_to(tweenX, tweenY, button)
        else:
            raise NotImplementedError("Unknown value of moveOrDrag: {0}".format(moveOrDrag))

    _log_screenshot(log_screenshot, "moveTo", "%s,%s-%s,%s" % (x1, y1, x2, y2), folder=".")
    if (tweenX, tweenY) not in FAILSAFE_POINTS:
        fail_safe_check()
# endregion


# region KEYBOARD METHODS
def is_valid_key(key):
    """
    Returns a Boolean value if the given key is a valid value to pass to
    SimpleRPA's keyboard-related functions for the current platform.

    This function is here because passing an invalid value to the SimpleRPA
    keyboard functions currently is a no-op that does not raise an exception.

    Some keys are only valid on some platforms. For example, while 'esc' is
    valid for the Escape key on all platforms, 'browserback' is only used on
    Windows operating systems.
    :param key: The key value.
    :return: bool
    """
    return platformModule.keyboardMapping.get(key, None) != None


@_generic_simple_rpa_checks
def key_down(key, log_screenshot=None, _pause=True):
    """
    Performs a keyboard key press without the release. This will put that key in a held down state.
    :param key: The key to be pressed down. The valid names are listed in KEYBOARD_KEYS.
    :param log_screenshot: If true a screen shot is taken during the operation.
    :param _pause: How many seconds in the end of function process. None by default, for no pause in the end of function process.
    :return: void
    """
    if len(key) > 1:
        key = key.lower()

    _log_screenshot(log_screenshot, "keyDown", key, folder=".")
    platformModule._key_down(key)


@_generic_simple_rpa_checks
def key_up(key, log_screenshot=None, _pause=True):
    """
    Performs a keyboard key release (without the press down beforehand).
    :param key: The key to be released up. The valid names are listed in KEYBOARD_KEYS.
    :param log_screenshot: If true a screen shot is taken during the operation.
    :param _pause: How many seconds in the end of function process. None by default, for no pause in the end of function process.
    :return: void
    """
    if len(key) > 1:
        key = key.lower()

    _log_screenshot(log_screenshot, "keyUp", key, folder=".")
    platformModule._key_up(key)


@_generic_simple_rpa_checks
def press(keys, presses=1, interval=0.0, log_screenshot=None, _pause=True):
    """
    Performs a keyboard key press down, followed by a release.
    :param keys: The key to be pressed. The valid names are listed in KEYBOARD_KEYS. Can also be a list of such strings.
    :param presses: The number of press repetitions. 1 by default, for just one press.
    :param interval: How many seconds between each press. 0.0 by default, for no pause between presses.
    :param log_screenshot: If true a screen shot is taken during the operation.
    :param _pause: How many seconds in the end of function process. None by default, for no pause in the end of function process.
    :return: void
    """
    if type(keys) == str:
        if len(keys) > 1:
            keys = keys.lower()
        keys = [keys] # If keys is 'enter', convert it to ['enter'].
    else:
        lowerKeys = []
        for s in keys:
            if len(s) > 1:
                lowerKeys.append(s.lower())
            else:
                lowerKeys.append(s)
        keys = lowerKeys
    interval = float(interval)
    _log_screenshot(log_screenshot, "press", ",".join(keys), folder=".")
    for i in range(presses):
        for k in keys:
            fail_safe_check()
            platformModule._key_down(k)
            platformModule._key_up(k)
        time.sleep(interval)


@contextmanager
@_generic_simple_rpa_checks
def hold(keys, log_screenshot=None, _pause=True):
    """
    Context manager that performs a keyboard key press down upon entry, followed by a release upon exit.
    :param key: The key to be pressed. The valid names are listed in KEYBOARD_KEYS. Can also be a list of such strings.
    :param log_screenshot: If true a screen shot is taken during the operation.
    :param _pause:
    :return: void
    """
    if type(keys) == str:
        if len(keys) > 1:
            keys = keys.lower()
        keys = [keys] # If keys is 'enter', convert it to ['enter'].
    else:
        lowerKeys = []
        for s in keys:
            if len(s) > 1:
                lowerKeys.append(s.lower())
            else:
                lowerKeys.append(s)
        keys = lowerKeys
    _log_screenshot(log_screenshot, "press", ",".join(keys), folder=".")
    for k in keys:
        fail_safe_check()
        platformModule._key_down(k)
    try:
        yield
    finally:
        for k in keys:
            fail_safe_check()
            platformModule._key_up(k)


@_generic_simple_rpa_checks
def typewrite(message, interval=0.0, log_screenshot=None, _pause=True):
    """
    Performs a keyboard key press down, followed by a release, for each of the characters in message.

    The message argument can also be list of strings, in which case any valid keyboard name can be used.

    Since this performs a sequence of keyboard presses and does not hold down keys, it cannot be used to perform
    keyboard shortcuts. Use the hotkey() function for that.
    :param message: If a string, then the characters to be pressed. If a list, then the key names of the keys to press in order. The valid names are listed in KEYBOARD_KEYS.
    :param interval: The number of seconds in between each press. 0.0 by default, for no pause in between presses.
    :param log_screenshot: If true takes a screen shot during the operation.
    :param _pause:
    :return: void
    """
    interval = float(interval)  # TODO - this should be taken out.

    _log_screenshot(log_screenshot, "write", message, folder=".")
    for c in message:
        if len(c) > 1:
            c = c.lower()
        press(c, _pause=False)
        time.sleep(interval)
        fail_safe_check()
# endregion


#region INTERNAL METHODS
def fail_safe_check():
    """
    Check to see if the mouse is in any of hte failsafe points. If so raise an exception to abort theprocess.
    :return: void
    """
    if FAILSAFE and tuple(position()) in FAILSAFE_POINTS:
        raise FailSafeException(
            "SimpleRPA fail-safe triggered from mouse moving to a corner of the screen. To disable this fail-safe, set SimpleRPA.FAILSAFE to False. DISABLING FAIL-SAFE IS NOT RECOMMENDED."
        )


def display_mouse_position(x_offset=0, y_offset=0):
    """
    This function is meant to be run from the command line. It will
    automatically display the location and RGB of the mouse cursor.
    :param x_offset:
    :param y_offset:
    :return:
    """
    try:
        runningIDLE = sys.stdin.__module__.startswith("idlelib")
    except:
        runningIDLE = False

    print("Press Ctrl-C to quit.")
    if x_offset != 0 or y_offset != 0:
        print("xOffset: %s yOffset: %s" % (x_offset, y_offset))
    try:
        while True:
            # Get and print the mouse coordinates.
            x, y = position()
            positionStr = "X: " + str(x - x_offset).rjust(4) + " Y: " + str(y - y_offset).rjust(4)
            if not onScreen(x - x_offset, y - y_offset) or sys.platform == "darwin":
                # Pixel color can only be found for the primary monitor, and also not on mac due to the screenshot having the mouse cursor in the way.
                pixelColor = ("NaN", "NaN", "NaN")
            else:
                pixelColor = pyscreeze.screenshot().getpixel(
                    (x, y)
                )  # NOTE: On Windows & Linux, getpixel() returns a 3-integer tuple, but on macOS it returns a 4-integer tuple.
            positionStr += " RGB: (" + str(pixelColor[0]).rjust(3)
            positionStr += ", " + str(pixelColor[1]).rjust(3)
            positionStr += ", " + str(pixelColor[2]).rjust(3) + ")"
            sys.stdout.write(positionStr)
            if not runningIDLE:
                # If this is a terminal, than we can erase the text by printing \b backspaces.
                sys.stdout.write("\b" * len(positionStr))
            else:
                # If this isn't a terminal (i.e. IDLE) then we can only append more text. Print a newline instead and pause a second (so we don't send too much output).
                sys.stdout.write("\n")
                time.sleep(1)
            sys.stdout.flush()
    except KeyboardInterrupt:
        sys.stdout.write("\n")
        sys.stdout.flush()


def _snapshot(tag, folder=None, region=None, radius=None):
    """

    :param tag:
    :param folder:
    :param region:
    :param radius:
    :return:
    """
    # TODO feature not finished
    if region is not None and radius is not None:
        raise Exception("Either region or radius arguments (or neither) can be passed to snapshot, but not both")

    if radius is not None:
        x, y = platformModule._position()

    if folder is None:
        folder = os.getcwd()

    now = datetime.datetime.now()
    filename = "%s-%s-%s_%s-%s-%s-%s_%s.png" % (
        now.year,
        str(now.month).rjust(2, "0"),
        str(now.day).rjust(2, "0"),
        now.hour,
        now.minute,
        now.second,
        str(now.microsecond)[:3],
        tag,
    )
    filepath = os.path.join(folder, filename)
    screenshot(filepath)


def sleep(seconds):
    """

    :param seconds:
    :return:
    """
    time.sleep(seconds)


def countdown(seconds):
    """

    :param seconds:
    :return:
    """
    for i in range(seconds, 0, -1):
        print(str(i), end=" ", flush=True)
        time.sleep(1)
    print()


def _get_number_token(command_str):
    """
    Gets the number token at the start of command_str.

    Given '5hello' returns '5'
    Given '  5hello' returns '  5'
    Given '-42hello' returns '-42'
    Given '+42hello' returns '+42'
    Given '3.14hello' returns '3.14'

    Raises an exception if it can't tokenize a number.
    :param command_str:
    :return:
    """
    pattern = re.compile(r"^(\s*(\+|\-)?\d+(\.\d+)?)")
    mo = pattern.search(command_str)
    if mo is None:
        raise SimpleRPAException("Invalid command at index 0: a number was expected")

    return mo.group(1)


def _get_quoted_string_token(command_str):
    """
    Gets the quoted string token at the start of command_str. The quoted string must use single quotes.

    Given "'hello'world" returns "'hello'"
    Given "  'hello'world" returns "  'hello'"

    Raises an exception if it can't tokenize a quoted string.
    :param command_str:
    :return:
    """
    pattern = re.compile(r"^((\s*)('(.*?)'))")
    mo = pattern.search(command_str)
    if mo is None:
        raise SimpleRPAException("Invalid command at index 0: a quoted string was expected")

    return mo.group(1)


def _get_parens_command_str_token(command_str):
    """
    Gets the command string token at the start of command_str. It will also be enclosed with parentheses.

    Given "(ccc)world" returns "(ccc)"
    Given "  (ccc)world" returns "  (ccc)"
    Given "(ccf10(r))world" returns "(ccf10(r))"

    Raises an exception if it can't tokenize a quoted string.
    :param command_str:
    :return:
    """
    # Check to make sure at least one open parenthesis exists:
    pattern = re.compile(r"^\s*\(")
    mo = pattern.search(command_str)
    if mo is None:
        raise SimpleRPAException("Invalid command at index 0: No open parenthesis found.")

    # Check to make sure the parentheses are balanced:
    i = 0
    openParensCount = 0
    while i < len(command_str):
        if command_str[i] == "(":
            openParensCount += 1
        elif command_str[i] == ")":
            openParensCount -= 1
            if openParensCount == 0:
                i += 1  # Remember to increment i past the ) before breaking.
                break
            elif openParensCount == -1:
                raise SimpleRPAException("Invalid command at index 0: No open parenthesis for this close parenthesis.")
        i += 1
    if openParensCount > 0:
        raise SimpleRPAException("Invalid command at index 0: Not enough close parentheses.")

    return command_str[0:i]


def _get_comma_token(command_str):
    """
    Gets the comma token at the start of command_str.

    Given ',' returns ','
    Given '  ,', returns '  ,'

    Raises an exception if a comma isn't found.
    :param command_str:
    :return:
    """
    pattern = re.compile(r"^((\s*),)")
    mo = pattern.search(command_str)
    if mo is None:
        raise SimpleRPAException("Invalid command at index 0: a comma was expected")

    return mo.group(1)


def _tokenize_command_str(command_str):
    """
    Tokenizes command_str into a list of commands and their arguments for the run() function. Returns the list.
    :param command_str:
    :return:
    """
    commandPattern = re.compile(r"^(su|sd|ss|c|l|m|r|g|d|k|w|h|f|s|a|p)")

    # Tokenize the command string.
    command_list = []
    i = 0  # Points to the current index in command_str that is being tokenized.
    while i < len(command_str):
        if command_str[i] in (" ", "\t", "\n", "\r"):
            # Skip over whitespace:
            i += 1
            continue

        mo = commandPattern.match(command_str[i:])
        if mo is None:
            raise SimpleRPAException("Invalid command at index %s: %s is not a valid command" % (i, command_str[i]))

        individualCommand = mo.group(1)
        command_list.append(individualCommand)
        i += len(individualCommand)

        # Handle the no argument commands (c, l, m, r, su, sd, ss):
        if individualCommand in ("c", "l", "m", "r", "su", "sd", "ss"):
            pass  # This just exists so these commands are covered by one of these cases.

        # Handle the arguments of the mouse (g)o and mouse (d)rag commands:
        elif individualCommand in ("g", "d"):
            try:
                x = _get_number_token(command_str[i:])
                i += len(x)  # Increment past the x number.

                comma = _get_comma_token(command_str[i:])
                i += len(comma)  # Increment past the comma (and any whitespace).

                y = _get_number_token(command_str[i:])
                i += len(y)  # Increment past the y number.

            except SimpleRPAException as excObj:
                # Exception message starts with something like "Invalid command at index 0:"
                # Change the index number and reraise it.
                indexPart, colon, message = str(excObj).partition(":")

                indexNum = indexPart[len("Invalid command at index ") :]
                newIndexNum = int(indexNum) + i
                raise SimpleRPAException("Invalid command at index %s:%s" % (newIndexNum, message))

            # Make sure either both x and y have +/- or neither of them do:
            if x.lstrip()[0].isdecimal() and not y.lstrip()[0].isdecimal():
                raise SimpleRPAException("Invalid command at index %s: Y has a +/- but X does not." % (i - len(y)))
            if not x.lstrip()[0].isdecimal() and y.lstrip()[0].isdecimal():
                raise SimpleRPAException(
                    "Invalid command at index %s: Y does not have a +/- but X does." % (i - len(y))
                )

            # Get rid of any whitespace at the front:
            command_list.append(x.lstrip())
            command_list.append(y.lstrip())

        # Handle the arguments of the (s)leep and (p)ause commands:
        elif individualCommand in ("s", "p"):
            try:
                num = _get_number_token(command_str[i:])
                i += len(num)  # Increment past the number.

                # TODO - raise an exception if a + or - is in the number.

            except SimpleRPAException as excObj:
                # Exception message starts with something like "Invalid command at index 0:"
                # Change the index number and reraise it.
                indexPart, colon, message = str(excObj).partition(":")

                indexNum = indexPart[len("Invalid command at index ") :]
                newIndexNum = int(indexNum) + i
                raise SimpleRPAException("Invalid command at index %s:%s" % (newIndexNum, message))

            # Get rid of any whitespace at the front:
            command_list.append(num.lstrip())

        # Handle the arguments of the (k)ey press, (w)rite, (h)otkeys, and (a)lert commands:
        elif individualCommand in ("k", "w", "h", "a"):
            try:
                quotedString = _get_quoted_string_token(command_str[i:])
                i += len(quotedString)  # Increment past the quoted string.
            except SimpleRPAException as excObj:
                # Exception message starts with something like "Invalid command at index 0:"
                # Change the index number and reraise it.
                indexPart, colon, message = str(excObj).partition(":")

                indexNum = indexPart[len("Invalid command at index ") :]
                newIndexNum = int(indexNum) + i
                raise SimpleRPAException("Invalid command at index %s:%s" % (newIndexNum, message))

            # Get rid of any whitespace at the front and the quotes:
            command_list.append(quotedString[1:-1].lstrip())

        # Handle the arguments of the (f)or loop command:
        elif individualCommand == "f":
            try:
                numberOfLoops = _get_number_token(command_str[i:])
                i += len(numberOfLoops)  # Increment past the number of loops.

                subcommand_str = _get_parens_command_str_token(command_str[i:])
                i += len(subcommand_str)  # Increment past the sub-command string.

            except SimpleRPAException as excObj:
                # Exception message starts with something like "Invalid command at index 0:"
                # Change the index number and reraise it.
                indexPart, colon, message = str(excObj).partition(":")

                indexNum = indexPart[len("Invalid command at index ") :]
                newIndexNum = int(indexNum) + i
                raise SimpleRPAException("Invalid command at index %s:%s" % (newIndexNum, message))

            # Get rid of any whitespace at the front:
            command_list.append(numberOfLoops.lstrip())

            # Get rid of any whitespace at the front and the quotes:
            subcommand_str = subcommand_str.lstrip()[1:-1]
            # Recursively call this function and append the list it returns:
            command_list.append(_tokenize_command_str(subcommand_str))

    return command_list


def _run_command_list(command_list, _ss_count):
    """

    :param command_list:
    :param _ss_count:
    :return:
    """
    global PAUSE
    i = 0
    while i < len(command_list):
        command = command_list[i]

        if command == "c":
            click(button=PRIMARY)
        elif command == "l":
            click(button=LEFT)
        elif command == "m":
            click(button=MIDDLE)
        elif command == "r":
            click(button=RIGHT)
        elif command == "su":
            scroll(1)  # scroll up
        elif command == "sd":
            scroll(-1)  # scroll down
        elif command == "ss":
            screenshot("screenshot%s.png" % (_ss_count[0]))
            _ss_count[0] += 1
        elif command == "s":
            sleep(float(command_list[i + 1]))
            i += 1
        elif command == "p":
            PAUSE = float(command_list[i + 1])
            i += 1
        #elif command == "g":
        #    if command_list[i + 1][0] in ("+", "-") and command_list[i + 2][0] in ("+", "-"):
        #         move(int(command_list[i + 1]), int(command_list[i + 2]))
        #    else:
        #        moveTo(int(command_list[i + 1]), int(command_list[i + 2]))
        #    i += 2
        #elif command == "d":
        #    if command_list[i + 1][0] in ("+", "-") and command_list[i + 2][0] in ("+", "-"):
        #        drag(int(command_list[i + 1]), int(command_list[i + 2]))
        #    else:
        #        dragTo(int(command_list[i + 1]), int(command_list[i + 2]))
        #    i += 2
        elif command == "k":
            press(command_list[i + 1])
            i += 1
        elif command == "w":
            type(command_list[i + 1])
            i += 1
        #elif command == "h":
        #    hotkey(*command_list[i + 1].replace(" ", "").split(","))
        #    i += 1
        #elif command == "a":
        #    alert(command_list[i + 1])
        #    i += 1
        elif command == "f":
            for j in range(int(command_list[i + 1])):
                _run_command_list(command_list[i + 2], _ss_count)
            i += 2
        i += 1


def _tween(tween_type):
    """
    Is used to set the tweeing type (how the mouse will move to a point).
    :param key: The type of tweening to apply.
    :return: tween
    """
    if tween_type == "IN_QUAD":
        return easeInQuad
    elif tween_type == "OUT_QUAD":
        return easeOutQuad
    elif tween_type == "IN_OUT_QUAD":
        return easeInOutQuad
    elif tween_type == "IN_CUBIC":
        return easeInCubic
    elif tween_type == "OUT_CUBIC":
        return easeOutCubic
    elif tween_type == "IN_OUT_CUBIC":
        return easeInOutCubic
    elif tween_type == "IN_QUART":
        return easeInQuart
    elif tween_type == "OUT_QUART":
        return easeOutQuart
    elif tween_type == "IN_OUT_QUART":
        return easeInOutQuart
    elif tween_type == "IN_QUINT":
        return easeInQuint
    elif tween_type == "OUT_QUINT":
        return easeOutQuint
    elif tween_type == "IN_OUT_QUINT":
        return easeInOutQuint
    elif tween_type == "IN_SINE":
        return easeInSine
    elif tween_type == "OUT_SINE":
        return easeOutSine
    elif tween_type == "IN_OUT_SINE":
        return easeInOutSine
    elif tween_type == "IN_EXPO":
        return easeInExpo
    elif tween_type == "OUT_EXPO":
        return easeOutExpo
    elif tween_type == "IN_OUT_EXPO":
        return easeInOutExpo
    elif tween_type == "IN_CIRC":
        return easeInCirc
    elif tween_type == "OUT_CIRC":
        return easeOutCirc
    elif tween_type == "IN_OUT_CIRC":
        return easeInOutCirc
    elif tween_type == "IN_ELASTIC":
        return easeInElastic
    elif tween_type == "OUT_ELASTIC":
        return easeOutElastic
    elif tween_type == "IN_OUT_ELASTIC":
        return easeOutElastic
    elif tween_type == "IN_BACK":
        return easeInBack
    elif tween_type == "OUT_BACK":
        return easeOutBack
    elif tween_type == "IN_OUT_BACK":
        return easeInOutBack
    elif tween_type == "IN_BOUNCE":
        return easeInBounce
    elif tween_type == "OUT_BOUNCE":
        return easeOutBounce
    elif tween_type == "IN_OUT_BOUNCE":
        return easeInOutBounce
    else:
        return linear


def run(command_str, _ss_count=None):
    """
    Run a series of SimpleRPA function calls according to a mini-language
    made for this function. The `command_str` is composed of character
    commands that represent SimpleRPA function calls.

    For example, `run('ccg-20,+0c')` clicks the mouse twice, then makes
    the mouse cursor go 20 pixels to the left, then click again.

    Whitespace between commands and arguments is ignored. Command characters
    must be lowercase. Quotes must be single quotes.

    For example, the previous call could also be written as `run('c c g -20, +0 c')`.

    The character commands and their equivalents are here:

    `c` => `click(button=PRIMARY)`
    `l` => `click(button=LEFT)`
    `m` => `click(button=MIDDLE)`
    `r` => `click(button=RIGHT)`
    `su` => `scroll(1) # scroll up`
    `sd` => `scroll(-1) # scroll down`
    `ss` => `screenshot('screenshot1.png') # filename number increases on its own`

    `gX,Y` => `moveTo(X, Y)`
    `g+X,-Y` => `move(X, Y) # The + or - prefix is the difference between move() and moveTo()`
    `dX,Y` => `dragTo(X, Y)`
    `d+X,-Y` => `drag(X, Y) # The + or - prefix is the difference between drag() and dragTo()`

    `k'key'` => `press('key')`
    `w'text'` => `write('text')`
    `h'key,key,key'` => `hotkey(*'key,key,key'.replace(' ', '').split(','))`
    `a'hello'` => `alert('hello')`

    `sN` => `sleep(N) # N can be an int or float`
    `pN` => `PAUSE = N # N can be an int or float`

    `fN(commands)` => for i in range(N): run(commands)

    Note that any changes to `PAUSE` with the `p` command will be undone when
    this function returns. The original `PAUSE` setting will be reset.
    :param command_str:
    :param _ss_count:
    :return: void
    """

    # run("ccc")  straight forward
    # run("susu") if 's' then peek at the next character
    global PAUSE

    if _ss_count is None:
        _ssCount = [
            0
        ]  # Setting this to a mutable list so that the callers can read the changed value. TODO improve this comment

    command_list = _tokenize_command_str(command_str)

    # Carry out each command.
    originalPAUSE = PAUSE
    _run_command_list(command_list, _ssCount)
    PAUSE = originalPAUSE
# endregion


# Add the bottom left, top right, and bottom right corners to FAILSAFE_POINTS.
_right, _bottom = size()
FAILSAFE_POINTS.extend([(0, _bottom - 1), (_right - 1, 0), (_right - 1, _bottom - 1)])

#region CONFIGURATION CLASS
class Config:
    use_widgets_by_default = True
    default_widget_duration = 1.0
    verbose_level = 2
    minimum_port = 0
    maximum_port = 0
    key = ""
    iv = ""
    client_to_server = ""
    server_to_client = ""
    server = ""
    port = 0
    protocol = ""
    run_as_a_service = True
# endregion
