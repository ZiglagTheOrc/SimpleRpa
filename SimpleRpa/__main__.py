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
import sys
import json
import Keyboard as Kb
import Mouse as Ms
import Screen as Sn
import SimpleOcr as Qo
import _Web_Comm
from Keyboard import Keys, CKeys
from _Platform_Convergence import Config
from colorama import Fore
from Simple3270 import Simple3270Api, TnKey

# Master TO DO List
# TODO: Switch Simple3270 from a console based to text file based error logging.
# TODO: Fix length issue with encryption
# TODO: Allow optional methods for C# Simple3270
# TODO: Trim the fat off the files ported from PyAutoGui

if sys.platform == 'win32':
    import _Win32_Comm


def test_mouse():
    Ms.move((30, 200), duration=1)
    Ms.down((40, 200))
    Ms.up((40,100))
    Ms.click()
    Ms.drag((40,30), (120, 30), duration=2)
    # Ms.scroll(5) # TODO: Seems like this is not working?


def test_keyboard():
    Kb.press("Q")
    Kb.press("a", CKeys.CTRL)
    Kb.press("f", CKeys.ALT)
    Kb.press("s", (CKeys.CTRL, CKeys.SHIFT))
    #Kb.press(CKeys.WIN) # Working Win TODO: WIN key not working?
    Kb.type("this is a test")
    Kb.type("a", CKeys.CTRL)
    Kb.type("s", (CKeys.CTRL, CKeys.SHIFT))


def test_screen():
    c1 = Sn.get_pixel_color((33, 112))
    c2 = Sn.get_known_color((33, 112))
    c3 = Sn.get_console_color((33, 112))
    image = Sn.capture((0, 0, 128, 128))
    Sn.capture_to_file((0,0,128,128), "test.bmp")
    loc = Sn.find_image('icon.bmp')


def test_ocr():
    Qo.add_font('/home/michaelhalpin/Windows/fontmap')  # Working Win Lin
    rect = (10, 350, 250, 50)
    txt = Qo.perform_ocr('default', rect, .9, 175)  # Working Win Lin


def configure():
    jsn = open('SimpleRpa.json', 'r').read().encode().decode('utf-8-sig')
    config = json.loads(jsn)

    Config.run_as_a_service = config['run_as_a_service']

    # region Load settings from config file.
    try:
        prop = 'protocol'
        Config.protocol = config[prop]
        print(Fore.LIGHTRED_EX + "DANGER!!! " + Fore.RED + "Config.json contains a manually entered debug encryption key value '" + prop + "'. This configuration exists only for dev/debug and represents a significant security risk for a production environment.  Delete the '" + prop + "' entry from SimpleRpa.json before deploying to production.")
    except:
        do_nothing = True
    try:
        prop = 'verbose_level'
        Config.verbose_level = config[prop]
        print(Fore.LIGHTRED_EX + "DANGER!!! " + Fore.RED + "Config.json contains a manually entered debug encryption key value '" + prop + "'. This configuration exists only for dev/debug and represents a significant security risk for a production environment.  Delete the '" + prop + "' entry from SimpleRpa.json before deploying to production.")
    except:
        do_nothing = True
    try:
        prop = 'key'
        Config.key = config[prop]
        print(Fore.LIGHTRED_EX + "DANGER!!! " + Fore.RED + "Config.json contains a manually entered debug encryption key value '" + prop + "'. This configuration exists only for dev/debug and represents a significant security risk for a production environment.  Delete the '" + prop + "' entry from SimpleRpa.json before deploying to production.")
    except:
        do_nothing = True
    try:
        prop = 'iv'
        Config.iv = config[prop]
        print(Fore.LIGHTRED_EX + "DANGER!!! " + Fore.RED + "Config.json contains a manually entered debug encryption key value '" + prop + "'. This configuration exists only for dev/debug and represents a significant security risk for a production environment.  Delete the '" + prop + "' entry from SimpleRpa.json before deploying to production.")
    except:
        do_nothing = True
    try:
        prop = 'server'
        Config.server = config[prop]
        print(Fore.LIGHTRED_EX + "DANGER!!! " + Fore.RED + "Config.json contains a manually entered debug encryption key value '" + prop + "'. This configuration exists only for dev/debug and represents a significant security risk for a production environment.  Delete the '" + prop + "' entry from SimpleRpa.json before deploying to production.")
    except:
        do_nothing = True
    try:
        prop = 'port'
        Config.port = config[prop]
        print(Fore.LIGHTRED_EX + "DANGER!!! " + Fore.RED + "Config.json contains a manually entered debug encryption key value '" + prop + "'. This configuration exists only for dev/debug and represents a significant security risk for a production environment.  Delete the '" + prop + "' entry from SimpleRpa.json before deploying to production.")
    except:
        do_nothing = True
    try:
        prop = 'client_to_server'
        Config.client_to_server = config[prop]
        print(Fore.LIGHTRED_EX + "DANGER!!! " + Fore.RED + "Config.json contains a manually entered debug encryption key value '" + prop + "'. This configuration exists only for dev/debug and represents a significant security risk for a production environment.  Delete the '" + prop + "' entry from SimpleRpa.json before deploying to production.")
    except:
        do_nothing = True
    try:
        prop = 'server_to_client'
        Config.server_to_client = config[prop]
        print(Fore.LIGHTRED_EX + "DANGER!!! " + Fore.RED + "Config.json contains a manually entered debug encryption key value '" + prop + "'. This configuration exists only for dev/debug and represents a significant security risk for a production environment.  Delete the '" + prop + "' entry from SimpleRpa.json before deploying to production.")
    except:
        do_nothing = True
    Config.use_widgets_by_default = config["use_widgets_by_default"]
    Config.default_widget_duration = config["default_widget_duration"]
    Config.minimum_port = config["minimum_port"]
    Config.maximum_port = config["maximum_port"]
    Config.server = config["server"]
    Config.port = config["minimum_port"]
    # endregion

    # region Load settings from command line.
    try:
        Config.protocol = sys.argv[1]
    except:
        do_nothing = True
    try:
        Config.verbose_level = sys.argv[2]
    except:
        do_nothing = True
    try:
        Config.key = sys.argv[3]
    except:
        do_nothing = True
    try:
        Config.iv = sys.argv[4]
    except:
        do_nothing = True
    if Config.protocol == "WebService":
        try:
            Config.server = sys.argv[5]
        except:
            do_nothing = True
        try:
            Config.port = sys.argv[6]
        except:
            do_nothing = True
    elif Config.protocol == "Win32Pipe":
        try:
            Config.client_to_server = sys.argv[5]
        except:
            do_nothing = True
        try:
            Config.server_to_client = sys.argv[6]
        except:
            do_nothing = True
    # endregion


def test_3270():
    emu = Simple3270Api("Win32Pipe", 1)
    js1 = [{"Name":"Enterprise","X":1,"Y":1,"L":20},{"Name":"Url","X":46,"Y":2,"L":28},{"Name":"Ip","X":63,"Y":1,"L":14},{"Name":"MainFrame","X":14,"Y":5,"L":20},{"name":"NextGen","X":28,"Y":15,"L":19}]
    js2 = [{"Name":"Login","X":1,"Y":24,"Value":"TSO"}]
    js3 = {"Name":"WaitFor","X":12,"Y":1,"Value":"ENTER USERID -"}
    output1 = emu.read_screen_text(js1)
    output2 = emu.read_screen_colors(js1)
    output3 = emu.write_screen_text(js2)
    output4 = emu.press_key(TnKey.ENTER)
    output5 = emu.wait_for_text(js3)
    emu.close()


def run_as_service():
    if Config.protocol == "WebService":
        _Web_Comm.run(Config.port, Config.key, Config.iv, Config.verbose_level)
    elif Config.protocol == "Win32Pipe":
        _Win32_Comm.Pipe.run(Config.key, Config.iv, Config.client_to_server, Config.server_to_client, Config.verbose_level)


if __name__ == '__main__':
    configure()

    if Config.run_as_a_service:
        run_as_service()
    else:
        #test_mouse()
        #test_keyboard()
        #test_screen()
        #test_ocr()
        #test_3270()
        print ("done")
