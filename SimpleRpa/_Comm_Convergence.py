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
import base64
import datetime
import json
import Keyboard
import Mouse
import Screen
import SimpleOcr
import _Steganography
import _Platform_Convergence as pc
from _Platform_Convergence import Config
from Keyboard import Console
from colorama import Fore


def run_method(verbose_level, wr, jsn, key, iv):
    """
    Writes logs to screen if verbose and sends data to do corresponding run evaluation.
    :param verbose_level: How descriptive we want to be.
    :param wr: The json web request to use.
    :param jsn: The raw json to write to the console..
    :param key: The encryption key to use.
    :param iv: The initialization vector to use.
    :return: json
    """
    _log_request(verbose_level, wr, jsn)
    reply = _run_corresponding_method(wr, key, iv)
    _log_response(verbose_level, wr, reply)
    return reply


def log_header(protocol):
    """
    If verbose writes initial startup text to the console..
    :param protocol: The communications protocol we are using.
    """
    Console.forecolor(Fore.YELLOW)
    Console.write("SimpleRPA")
    Console.forecolor(Fore.WHITE)
    Console.write(" Version " + pc.version)
    Console.forecolor(Fore.GREEN)
    Console.writeln(" is running! (" + protocol + ")")
    Console.forecolor(Fore.WHITE)



def _log_request(verbose_level, wr, jsn):
    """
    If verbose writes request text to the console.
    :param verbose_level: The level of verbosity we want to use. (0-2)
    :param wr: The web request containing the method name.
    :param jsn: The text of the actual json request.
    """
    verb = int(verbose_level)
    if verb == 1:
        Console.forecolor(Fore.CYAN)
        Console.write(str(datetime.datetime.now()))
        Console.forecolor(Fore.GREEN)
        Console.write(" request received for client ")
        Console.forecolor(Fore.YELLOW)
        Console.writeln("[" + wr['method'] + "]")
        Console.forecolor(Fore.WHITE)
    elif verb > 1:
        Console.forecolor(Fore.CYAN)
        Console.write(str(datetime.datetime.now()))
        Console.forecolor(Fore.GREEN)
        Console.write(" request received for client ")
        Console.forecolor(Fore.YELLOW)
        Console.writeln("[" + wr['method'] + "]")
        Console.forecolor(Fore.BLUE)
        Console.writeln(str(jsn).replace("'",'"').replace("True","true").replace("False","false"))
        Console.forecolor(Fore.WHITE)


def _log_response(verbose_level, wr, reply):
    """
    If verbose writes response text to the console.
    :param verbose_level: The level of verbosity we want to use. (0-2)
    :param wr: The web request containing the method name.
    :param jsn: The text of the actual json request.
    """
    verb = int(verbose_level)
    if verb == 1:
        Console.forecolor(Fore.CYAN)
        Console.write(str(datetime.datetime.now()))
        Console.forecolor(Fore.GREEN)
        Console.write(" response sent for client ")
        Console.forecolor(Fore.YELLOW)
        Console.writeln("[" + wr['method'] + "]")
        Console.forecolor(Fore.WHITE)
    elif verb > 1:
        Console.forecolor(Fore.CYAN)
        Console.write(str(datetime.datetime.now()))
        Console.forecolor(Fore.GREEN)
        Console.write(" response sent for client ")
        Console.forecolor(Fore.YELLOW)
        Console.writeln("[" + wr['method'] + "]")
        Console.forecolor(Fore.BLUE)
        Console.writeln(str(reply).replace("'",'"').replace("True","true").replace("False","false"))
        Console.forecolor(Fore.WHITE)


def _run_corresponding_method(wr, key, iv):
    """
    Finds the corresponding method to run based on what is in the web request and runs it.
    :param wr: The web request containing the method name.
    :param key: The key to use for encryption routines.
    :param iv: The initialization vector to use for encryption routines.
    """
    # region MOUSE METHODS
    method = str(wr['method'])
    if method.startswith('mouse'):
        if method == 'mouse_move':
            wr['use_widget'], wr['duration'] = _get_widget_settings(wr['use_widget'], wr['duration'])
            Mouse.move((wr['x'], wr['y']), float(wr['duration']), pc._tween(wr['tween']), wr['log_screenshot'], wr['use_widget'])
            reply = json.dumps({"response": "SUCCESS"})
        elif method == 'mouse_click':
            wr['use_widget'], wr['duration'] = _get_widget_settings(wr['use_widget'], wr['duration'])
            if wr['x'] == -1 or wr['y'] == -1:
                pt = None
            else:
                pt = (wr['x'], wr['y'])
            Mouse.click(pt, wr['clicks'], float(wr['interval']), wr['button'], float(wr['duration']),
                        pc._tween(wr['tween']), wr['log_screenshot'], wr['use_widget'])
            reply = json.dumps({"response": "SUCCESS"})
        elif method == 'mouse_drag':
            wr['use_widget'], wr['duration'] = _get_widget_settings(wr['use_widget'], wr['duration'])
            Mouse.drag((wr['x1'], wr['y1']), (wr['x2'], wr['y2']), float(wr['duration']), pc._tween(wr['tween']),
                       wr['button'], wr['log_screenshot'], wr['use_widget'])
            reply = json.dumps({"response": "SUCCESS"})
        elif method == 'mouse_down':
            wr['use_widget'], wr['duration'] = _get_widget_settings(wr['use_widget'], wr['duration'])
            if wr['x'] == -1 or wr['y'] == -1:
                pt = None
            else:
                pt = (wr['x'], wr['y'])
            Mouse.down(pt, str.lower(wr['button']), pc._tween(wr['tween']), wr['log_screenshot'], wr['use_widget'],
                       wr['duration'])
            reply = json.dumps({"response": "SUCCESS"})
        elif method == 'mouse_up':
            wr['use_widget'], wr['duration'] = _get_widget_settings(wr['use_widget'], wr['duration'])
            if wr['x'] == -1 or wr['y'] == -1:
                pt = None
            else:
                pt = (wr['x'], wr['y'])
            Mouse.up(pt, str.lower(wr['button']), pc._tween(wr['tween']), wr['log_screenshot'], wr['use_widget'],
                     wr['duration'])
            reply = json.dumps({"response": "SUCCESS"})
        elif method == 'mouse_scroll':
            if wr['x'] == -1 or wr['y'] == -1:
                pt = None
            else:
                pt = (wr['x'], wr['y'])
            Mouse.scroll(wr['clicks'], pt, wr['log_screenshot'])
            reply = json.dumps({"response": "SUCCESS"})
        elif method == 'mouse_position':
            x, y = Mouse.position()
            reply = json.dumps({"response": "SUCCESS", "x": x, "y": y})
    # endregion
    # region KEYBOARD METHODS
    elif method.startswith("keyboard"):
        if method == 'keyboard_press':
            Keyboard.press(wr['key'], tuple(wr['command_keys']), wr['presses'], float(wr['interval']), wr['log_screenshot'])
            reply = json.dumps({"response": "SUCCESS"})
        elif method == 'keyboard_type':
            Keyboard.type(wr['text'], tuple(wr['command_keys']), float(wr['interval']), wr['log_screenshot'])
            reply = json.dumps({"response": "SUCCESS"})
    # endregion
    # region SCREEN METHODS
    elif method.startswith("screen"):
        if method == 'screen_capture':
            wr['use_widget'], wr['duration'] = _get_widget_settings(wr['use_widget'], wr['duration'])
            img = Screen.capture((wr['x'], wr['y'], wr['width'], wr['height'], wr['use_widget'], wr['duration']))
            ary = img.tobytes()
            attach = _Steganography.encrypt_bytes(ary, key, iv)
            lng = base64.b64encode(str(len(ary)).encode('utf-8')).decode('utf-8')
            reply = '{"response":"SUCCESS","content":"' + attach + '","length":"' + lng + '"}'
        elif method == 'screen_get_pixel_color':
            wr['use_widget'], wr['duration'] = _get_widget_settings(wr['use_widget'], wr['duration'])
            color = Screen.get_pixel_color((wr['x'], wr['y']), wr['use_widget'], wr['duration'])
            reply = json.dumps({"response": "SUCCESS", "red": str(color[0]), "green": str(color[1]), "blue": str(color[2]),
                     "name": ""})
        elif method == 'screen_get_known_color':
            wr['use_widget'], wr['duration'] = _get_widget_settings(wr['use_widget'], wr['duration'])
            color = Screen.get_known_color((wr['x'], wr['y']), wr['use_widget'], wr['duration'])
            reply = json.dumps({"response": "SUCCESS", "red": str(color.r), "green": str(color.g), "blue": str(color.b),
                     "name": color.name})
        elif method == 'screen_get_console_color':
            wr['use_widget'], wr['duration'] = _get_widget_settings(wr['use_widget'], wr['duration'])
            color = Screen.get_console_color((wr['x'], wr['y']), wr['use_widget'], wr['duration'])
            reply = json.dumps({"response": "SUCCESS", "red": str(color.r), "green": str(color.g), "blue": str(color.b),
                     "name": color.name})
        elif method == 'screen_find_image':
            # region Compile JSON list of locations.
            wr['use_widget'], wr['duration'] = _get_widget_settings(wr['use_widget'], wr['duration'])
            locs = Screen.find_image(wr['filename'], wr['threshold'], wr['use_widget'], wr['duration'])
            temp = '{"x":<X>,"y":<Y>,"w":<W>,"h":<H>}'
            text = '['
            leng = len(locs)
            for i in range(leng):
                text += temp.replace('<X>', str(locs[i][0])).replace('<Y>', str(locs[i][1])).replace('<W>', str(
                    locs[i][2])).replace('<H>', str(locs[i][3])) + ','
            text = text[0:len(text) - 1] + ']'
            # endregion
            reply = json.dumps(json.loads('{"response":"SUCCESS","locs":<LOCS>}'.replace('<LOCS>', text)))
    # endregion
    # region OCR METHODS
    elif method.startswith("simple_ocr"):
        if method == 'simple_ocr_add_font':
            SimpleOcr.add_font(wr['path'])
            reply = json.dumps({"response": "SUCCESS"})
        elif method == 'simple_ocr_perform_ocr':
            wr['use_widget'], wr['duration'] = _get_widget_settings(wr['use_widget'], wr['duration'])
            text = SimpleOcr.perform_ocr(wr['font_maps'], (wr['x'], wr['y'], wr['width'], wr['height']),
                                         wr['ocr_threshold'], wr['capture_threshold'],
                                         wr['use_widget'], wr['duration'])
            reply = json.dumps({"response": "SUCCESS", "text": text})
    # endregion
    elif method == "shut_down":
        quit()
    return reply


def _get_widget_settings(use_widget, duration):
    """
    Returns the default settings for widgets. If the widget is explicitly set to True of False then the current setting
    is returned. If use_widigt is set to None then it looks up the setting defauls in the config file and returns that.
    :param use_widget: The current widget setting.
    :param duration: The current duration.
    """
    if use_widget == "None":
        if Config.use_widgets_by_default:
            use_widget = "True"
            if duration == 0:
                duration = Config.default_widget_duration
    return use_widget, duration

