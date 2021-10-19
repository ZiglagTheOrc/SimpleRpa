# region License
"""
 * SimplRPA - A simple RPA library for Python and C#
 *
 * Copyright (c) 2009-2021 Ziglag the Orc
 * Modifications (c) as per Git change history
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
import _Platform_Convergence
from multipledispatch import dispatch

# region ENUMERATIONS
class CKeys:
    """
    An enumerated list of command keys. (Keys you press and hold)
    """
    CTRL = 'ctrl'
    ALT = 'alt'
    WIN = 'win'
    SHIFT = 'shift'
    FN = 'fn'
    CMD = 'command'
    OPT = 'option'

class Keys:
    """
    An enumerated list of keys you press.
    """
    BACK_SPACE = 'backspace'
    BREAK = 'clear'
    CAPS_LOCK = 'capslock'
    DELETE = 'delete'
    DOWN = 'down'
    END = 'end'
    ENTER = 'enter'
    ESCAPE = 'escape'
    F1 = 'f1'
    F2 = 'f2'
    F3 = 'f3'
    F4 = 'f4'
    F5 = 'f5'
    F6 = 'f6'
    F7 = 'f7'
    F8 = 'f8'
    F9 = 'f9'
    F10 = 'f10'
    F11 = 'f11'
    F12 = 'f12'
    F13 = 'f13'
    F14 = 'f14'
    F15 = 'f15'
    F16 = 'f16'
    F17 = 'f17'
    F18 = 'f18'
    F19 = 'f19'
    F20 = 'f20'
    F21 = 'f21'
    F22 = 'f22'
    F23 = 'f23'
    F24 = 'f24'
    HOME = 'home'
    INSERT = 'insert'
    NUMLOCK = 'numlock'
    PAGE_DOWN = 'pagedown'
    PAGE_UP = 'pageup'
    PRINT_SCREEN = 'printscreen'
    LEFT = 'left'
    RIGHT = 'right'
    SCROLL_LOCK = 'scrolllock'
    SPACE = 'space'
    UP = 'up'
    TAB = 'tab'
    NUM_0 = 'num0'
    NUM_1 = 'num1'
    NUM_2 = 'num2'
    NUM_3 = 'num3'
    NUM_4 = 'num4'
    NUM_5 = 'num5'
    NUM_6 = 'num6'
    NUM_7 = 'num7'
    NUM_8 = 'num8'
    NUM_9 = 'num9'
    ADD = 'add'
    SUBTRACT = 'subtract'
    MULTIPLY = 'multiply'
    DIVIDE = 'divide'
    DECIMAL = 'decimal'
    RETURN = 'return'
    BROWSER_BACK = 'browserback'
    BROWSER_FAVORITES = 'browserfavorites'
    BROWSER_FORWARD = 'browserforward'
    BROWSER_HOME = 'browserhome'
    BROWSER_REFRESH = 'browserrefresh'
    BROWSER_SEARCH = 'browsersearch'
    BROWSER_STOP = 'browserstop'
    PLAY = 'playpause'
    PAUSE = 'pause'
    STOP = 'stop'
    NEXT_TRACK = 'nexttrack'
    PREV_TRACK = 'prevtrack'
    VOLUME_DOWN = 'volumedown'
    VOLUME_MUTE = 'volumemute'
    VOLUME_UP = 'volumeup'
    LAUNCH_APP1 = 'launchapp1'
    LAUNCH_APP2 = 'launchapp2'
    LAUNCH_MAIL = 'launchmail'
    LAUNCH_MEDIA_SELECT = 'launchmediaselect'
    MODE_CHANGE = 'modechange'
    ACCEPT = 'accept'
    APPS = 'apps'
    CONVERT = 'convert'
    EXECUTE = 'execute'
    FINAL = 'final'
    HELP = 'help'
    NONCONVERT = 'nonconvert'
    SELECT = 'select'
    SEPARATOR = 'separator'
    SLEEP = 'sleep'
    HANGUEL = 'hanguel'
    HANGUL = 'hangul'
    HANJA = 'hanja'
    JUNJA = 'junja'
    KANA = 'kana'
    KANJI = 'kanji'
    YEN = 'yen'
    SPACE = ' '
    EXCLAIM = '!'
    QUOTE = '"'
    HASH = '#'
    DOLLAR = '$'
    PERCENT = '%'
    AMPERSAND = '&'
    QUOTE = "'"
    PARENTHESIS_LEFT = '('
    PARENTHESIS_RIGHT = ')'
    ASTERISK = '*'
    PLUS = '+'
    COMMA = ','
    HYPHEN = '-'
    PERIOD ='.'
    FORWARD_SLASH = '/'
    COLON = ':'
    SEMICOLON = ';'
    LESS_THAN = '<'
    EQUALS = '='
    GREATER_THAN = '>'
    QUESTION = '?'
    AT = '@'
    BRACKET_LEFT = '['
    BACK_SLASH = '\\'
    BRACKET_RIGHT = ']'
    EXPONENT = '^'
    UNDERSCORE = '_'
    ACCENT = '`'
    BRACE_LEFT = '{'
    PIPE = '|'
    BRACE_RIGHT = '}'
    TILDE = '~'
    KEY_0 = '0'
    KEY_1 = '1'
    KEY_2 = '2'
    KEY_3 = '3'
    KEY_4 = '4'
    KEY_5 = '5'
    KEY_6 = '6'
    KEY_7 = '7'
    KEY_8 = '8'
    KEY_9 = '9'
    A = 'a'
    B = 'b'
    C = 'c'
    D = 'd'
    E = 'e'
    F = 'f'
    G = 'g'
    H = 'h'
    I = 'i'
    J = 'j'
    K = 'k'
    L = 'l'
    M = 'm'
    N = 'n'
    O = 'o'
    P = 'p'
    Q = 'q'
    R = 'r'
    S = 's'
    T = 't'
    U = 'u'
    V = 'v'
    W = 'w'
    X = 'x'
    Y = 'y'
    Z = 'z'
# endregion


#region PUBLIC METHODS
@dispatch(str)
def press(key, presses=1, interval=0.0, log_screenshot=False):
    """
    Presses the specified key.
    :param key: The key to press.
    :param presses: The number of presses to make.
    :param interval: The time to wait between presses.
    :param log_screenshot: If true the method takes a screenshot after the action.
    :return: void
    """
    _Platform_Convergence.press(key, presses, interval, log_screenshot, True)


@dispatch(str, str)
def press(key, command_key, presses=1, interval=0.0, log_screenshot=False):
    """
    Presses the specified key.
    :param key: The key to press.
    :param command_key: The command key to hold while pressing the key.
    :param presses: The number of times to press.
    :param interval: The time to wait between presses.
    :param log_screenshot: If true the method takes a screenshot after the action.
    :return: void
    """
    __down(command_key)
    _Platform_Convergence.press(key, presses, interval, log_screenshot, True)
    __up(command_key)


@dispatch(str, str, int, float, bool)
def press(key, command_key, presses=1, interval=0.0, log_screenshot=False):
    """
    Presses the specified key.
    :param key: The key to press.
    :param command_key: The command key to hold while pressing the key.
    :param presses: The number of times to press.
    :param interval: The time to wait between presses.
    :param log_screenshot: If true the method takes a screenshot after the action.
    :return: void
    """
    __down(command_key)
    _Platform_Convergence.press(key, presses, interval, log_screenshot, True)
    __up(command_key)


@dispatch(str, tuple)
def press(key, command_keys, presses=1, interval=0.0, log_screenshot=False):
    """
    Presses the specified key.
    :param key: The key to press.
    :param command_keys: A tuple of command keys to hold down while pressing the key.
    :param presses: The number of times to press.
    :param interval: The time to wait between presses.
    :param log_screenshot: If true the method takes a screenshot after the action.
    :return: void
    """
    _down(command_keys)
    _Platform_Convergence.press(key, presses, interval, log_screenshot, True)
    _up(command_keys)


@dispatch(str, tuple, int, float, bool)
def press(key, command_keys, presses=1, interval=0.0, log_screenshot=False):
    """
    Presses the specified key.
    :param key: The key to press.
    :param command_keys: The tuple containing all the command keys to hold down while pressing the key.
    :param presses: The number of times to press.
    :param interval: The time to wait between presses.
    :param log_screenshot: If true the method takes a screenshot after the action.
    :return: void
    """
    _down(command_keys)
    _Platform_Convergence.press(key, presses, interval, log_screenshot, True)
    _up(command_keys)


@dispatch(str)
def type(text, interval=0.0, log_screenshot=None):
    """
    Types the specified text.
    :param text: The text to type.
    :param interval: The time to wait between presses.
    :param log_screenshot: If true the method takes a screenshot after the action.
    :return: void
    """
    _Platform_Convergence.typewrite(text, interval, log_screenshot, True)


@dispatch(str,str)
def type(text, command_key, interval=0.0, log_screenshot=False):
    """
    Types the specified text.
    :param text: The text to type.
    :param command_key: The command key to hold down while pressing the key.
    :param interval: The time to wait between presses.
    :param log_screenshot: If true the method takes a screenshot after the action.
    :return: void
    """
    __down(command_key)
    _Platform_Convergence.typewrite(text, interval, log_screenshot, True)
    __up(command_key)


@dispatch(str,str,float,bool)
def type(text, command_key, interval=0.0, log_screenshot=False):
    """
    Types the specified text.
    :param text: The text to type.
    :param command_key: The command key to hold down while pressing the key.
    :param interval: The time to wait between presses.
    :param log_screenshot: If true the method takes a screenshot after the action.
    :return: void
    """
    __down(command_key)
    _Platform_Convergence.typewrite(text, interval, log_screenshot, True)
    __up(command_key)


@dispatch(str,tuple)
def type(text, command_keys, interval=0.0, log_screenshot=False):
    """
    Types the specified text.
    :param text: The text to type.
    :param command_keys: The tuple containing all the command keys to hold down while pressing the key.
    :param interval: The time to wait between presses.
    :param log_screenshot: If true the method takes a screenshot after the action.
    :return: void
    """
    _down(command_keys)
    _Platform_Convergence.typewrite(text, interval, log_screenshot, True)
    _up(command_keys)


@dispatch(str,tuple,float,bool)
def type(text, command_keys, interval=0.0, log_screenshot=False):
    """
    Types the specified text.
    :param text: The text to type.
    :param command_keys: The tuple containing all the command keys to hold down while pressing the key.
    :param interval: The time to wait between presses.
    :param log_screenshot: If true the method takes a screenshot after the action.
    :return: void
    """
    _down(command_keys)
    _Platform_Convergence.typewrite(text, interval, log_screenshot, True)
    _up(command_keys)
# endregion


# region PROTECTED METHODS
def _down(command_keys):
    """
    Presses each of the specified keys in the list of keys.
    :param command_keys: The list of keys to press.
    :return: void
    """
    for i in range(len(command_keys)):
        __down(command_keys[i])


def _up(command_keys):
    """
    Releases each of the specified keys in the list of keys.
    :param command_keys: The list of keys to release.
    :return: void
    """
    for i in range(len(command_keys)):
        __up(command_keys[i])


def __down(command_key):
    """
    Presses the key specified.
    :param command_key: The key to press
    :return: void
    """
    if  command_key == CKeys.ALT:
        _Platform_Convergence.key_down(CKeys.ALT, False, True)
    elif command_key == CKeys.CTRL:
        _Platform_Convergence.key_down(CKeys.CTRL, False, True)
    elif command_key == CKeys.SHIFT:
        _Platform_Convergence.key_down(CKeys.SHIFT, False, True)
    elif command_key == CKeys.WIN:
        _Platform_Convergence.key_down(CKeys.WIN, False, True)
    elif command_key == CKeys.FN:
        _Platform_Convergence.key_down(CKeys.FN, False, True)
    elif command_key == CKeys.OPT:
        _Platform_Convergence.key_down(CKeys.OPT, False, True)
    elif command_key == CKeys.CMD:
        _Platform_Convergence.key_down(CKeys.CMD, False, True)


def __up(command_key):
    """
    Releases the key specified.
    :param command_key: The key to release
    :return: void
    """
    if command_key == CKeys.ALT:
        _Platform_Convergence.key_up(CKeys.ALT, False, True)
    elif command_key == CKeys.CTRL:
        _Platform_Convergence.key_up(CKeys.CTRL, False, True)
    elif command_key == CKeys.SHIFT:
        _Platform_Convergence.key_up(CKeys.SHIFT, False, True)
    elif command_key == CKeys.WIN:
        _Platform_Convergence.key_up(CKeys.WIN, False, True)
    elif command_key == CKeys.FN:
        _Platform_Convergence.key_up(CKeys.FN, False, True)
    elif command_key == CKeys.OPT:
        _Platform_Convergence.key_up(CKeys.OPT, False, True)
    elif command_key == CKeys.CMD:
        _Platform_Convergence.key_up(CKeys.CMD, False, True)
# endregion