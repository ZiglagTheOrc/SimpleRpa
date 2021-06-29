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
import json
import string
import random
import subprocess
import sys
import _Steganography

if sys.platform == 'win32':
    from _Win32_Comm import Pipe


class TnKey:
    """
    The enumeration of virtual keys available in a 3270 instance.
    """
    F1 = "F1"
    F2 = "F2"
    F3 = "F3"
    F4 = "F4"
    F5 = "F5"
    F6 = "F6"
    F7 = "F7"
    F8 = "F8"
    F9 = "F9"
    F10 = "F10"
    F11 = "F11"
    F12 = "F12"
    F13 = "F13"
    F14 = "F14"
    F15 = "F15"
    F16 = "F16"
    F17 = "F17"
    F18 = "F18"
    F19 = "F19"
    F20 = "F20"
    F21 = "F21"
    F22 = "F22"
    F23 = "F23"
    F24 = "F24"
    TAB = "Tab"
    BACK_TAB = "BackTab"
    ENTER = "Enter"
    BACKSPACE = "Backspace"
    CLEAR = "Clear"
    DELETE = "Delete"
    DELETE_FIELD = "DeleteField"
    DELETE_WORD = "DeleteWord"
    LEFT = "Left"
    LEFT2 = "Left2"
    UP = "Up"
    RIGHT = "Right"
    RIGHT2 = "Right2"
    DOWN = "Down"
    ATTN = "Attn"
    CIRCUM_NOT = "CircumNot"
    CURSOR_SELECT = "CursorSelect"
    DUP = "Dup"
    ERASE = "Erase"
    ERASE_EOF = "EraseEOF"
    ERASE_INPUT = "EraseInput"
    FIELD_END = "FieldEnd"
    FIELD_MARK = "FieldMark"
    FIELD_EXIT = "FieldExit"
    HOME = "Home"
    INSERT = "Insert"
    INTERRUPT = "Interrupt"
    KEY = "Key"
    NEW_LINE = "Newline"
    NEXT_WORD = "NextWord"
    PANN = "PAnn"
    PREVIOUS_WORD = "PreviousWord"
    RESET = "Reset"
    SYS_REQ = "SysReq"
    TOGGLE = "Toggle"
    TOGGLE_INSERT = "ToggleInsert"
    TOGGLE_REVERSE = "ToggleReverse"
    PA1 = "PA1"
    PA2 = "PA2"
    PA3 = "PA3"
    PA4 = "PA4"
    PA5 = "PA5"
    PA6 = "PA6"
    PA7 = "PA7"
    PA8 = "PA8"
    PA9 = "PA9"
    PA10 = "PA10"
    PA11 = "PA11"
    PA12 = "PA12"


class Simple3270Api:
    """
    An api used to connect to 3720 mainframe sessions.
    """
    c2s = ''
    s2c = ''
    key = []
    iv = []

    def __init__(self, protocol, verbose_level):
        """
        Used to construct a new instance of Simple3270Api.
        :param protocol: The cross platform communication protocol to use.
        :param verbose_level: The level of verbosity the session should use.
        :return: json
        """
        self.key = _rand(32, 3)
        self.iv = _rand(16, 3)
        self.c2s = _rand(16, 2)
        self.s2c = _rand(16, 2)

        self.key = '99999999999999999999999999999999'
        self.iv = '0000000000000000'
        self.s2c = '3270_ServerToClient'
        self.c2s = '3270_ClientToServer'

        path = "C:\\Users\\e007020\\RiderProjects\\SimpleRpaSharp\\Simple-3270\\bin\\Debug\\netcoreapp3.1\\"
        resp = json.loads(Pipe.get(self.s2c))
        if resp['response'] == 'EXCEPTION':
            raise Exception(resp['message'])
        return

        if sys.platform == 'win32':
            subprocess.Popen(path + "Simple-3270.exe " + protocol + " " + str(
                verbose_level) + " " + skey + " " + siv + " " + c2s + " " + s2c)
        elif sys.platform == 'linux':
            subprocess.Popen("mono SimpleRPA.exe")
        elif sys.platform == 'darwin':
            subprocess.Popen("mono SimpleRPA.exe")
        else:
            raise Exception("Your operating system '" + sys.platform + "' is not supported.")

    def close(self):
        """
        Sends message to shut down external service upon finishing.
        :return: void
        """
        shutdown = '{"method":"dispose_and_shutdown","content":{"content":"close_session"}}'
        req = _Steganography.package(shutdown, self.key, self.iv)
        Pipe.set(self.c2s, req)  # Send only, no need for a response.
        return

    def read_screen_text(self, jsn):
        """
        Reads the values of all the field colors for fields specified in the json field map.
        :param jsn: The map of fields to use to gather text.
        :return: json
        """
        if not isinstance(jsn, str):
            jsn = json.dumps(jsn)
        js = '{"method":"read_screen_text","content":' + jsn + '}'
        req = _Steganography.package(js, self.key, self.iv)
        resp = Pipe.query(req, self.c2s, self.s2c, self.key, self.iv)
        return resp

    def read_screen_colors(self, jsn):
        """
        Writes the specified values to all fields listed in the json field map.
        :param jsn: The map of fields to use to gather text.
        :return: json
        """
        if not isinstance(jsn, str):
            jsn = json.dumps(jsn)
        js = '{"method":"read_screen_colors","content":' + jsn + '}'
        req = _Steganography.package(js, self.key, self.iv)
        resp = Pipe.query(req, self.c2s, self.s2c, self.key, self.iv)
        return resp

    def write_screen_text(self, jsn):
        """
        Presses the specified key.
        :param jsn: The TnKey to press.
        :return: bool
        """
        if not isinstance(jsn, str):
            jsn = json.dumps(jsn)
        js = '{"method":"write_screen_text","content":' + jsn + '}'
        req = _Steganography.package(js, self.key, self.iv)
        resp = Pipe.query(req, self.c2s, self.s2c, self.key, self.iv)
        response = resp['response']
        if response == 'TIMEOUT':
            return False
        elif response == 'EXCEPTION':
            raise Exception(resp['message'])
        return True

    def press_key(self, key):
        """
        Presses the specified key.
        :param key: The TnKey to press.
        :return: bool
        """
        js = '{"method":"press_key","content":{"button":"' + key + '"}}'
        req = _Steganography.package(js, self.key, self.iv)
        resp = Pipe.query(req, self.c2s, self.s2c, self.key, self.iv)
        response = resp['response']
        if response == 'TIMEOUT':
            return False
        elif response == 'EXCEPTION':
            raise Exception(resp['message'])
        return True

    def wait_for_text(self, jsn):
        """
        Waits for the specified text to appear in the specified place of the screen before moving on.
        Returns True when text appears otherwise returns False if operation times out.
        :param jsn: The json map to use.
        :return: bool
        """
        if not isinstance(jsn, str):
            jsn = json.dumps(jsn)
        js = '{"method":"wait_for_text","content":' + jsn + '}'
        req = _Steganography.package(js, self.key, self.iv)
        resp = Pipe.query(req, self.c2s, self.s2c, self.key, self.iv)
        response = resp['response']
        if response == 'TIMEOUT':
            return False
        elif response == 'EXCEPTION':
            raise Exception(resp['message'])
        return True


def _rand(count, level):
    """
    Generates a random string.
    :param count: The number of characters to generate.
    :param level: The level of complexity in generated string.
    :return: string
    """
    text = ""
    symbols = ['!', '@', '#', '$', '%', '^', '(', ')', '-', '_', '=', '+', '[', ']', '~', ',']  # Can add more
    for _ in range(count):
        r = random.randint(0, level)
        if r == 0:
            text += random.choice(string.ascii_lowercase)
        elif r == 1:
            text += random.choice(string.ascii_uppercase)
        elif r == 2:
            text += random.choice(string.digits)
        elif r == 3:
            text += random.choice(symbols)
    return text
