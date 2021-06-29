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
import os.path
import _Web_Comm
from _Platform_Convergence import Config
from Keyboard import Console
from colorama import Fore

if sys.platform == 'win32':
    import _Win32_Comm


def configure():
    if not os.path.isfile('SimpleRpa.json'):
        print("The configuration file 'SimpleRpa.json' is missing.")
        return
    jsn = open('SimpleRpa.json', 'r').read().encode().decode('utf-8-sig')
    config = json.loads(jsn)

    Config.run_as_a_service = config['run_as_a_service']

    # region Load settings from config file.
    try:
        prop = 'protocol'
        Config.protocol = config[prop]
        warn(prop)
    except:
        do_nothing = True
    try:
        prop = 'verbose_level'
        Config.verbose_level = config[prop]
        warn(prop)
    except:
        do_nothing = True
    try:
        prop = 'key'
        Config.key = config[prop]
        warn(prop)
    except:
        do_nothing = True
    try:
        prop = 'iv'
        Config.iv = config[prop]
        warn(prop)
    except:
        do_nothing = True
    try:
        prop = 'server'
        Config.server = config[prop]
        warn(prop)
    except:
        do_nothing = True
    try:
        prop = 'port'
        Config.port = config[prop]
        warn(prop)
    except:
        do_nothing = True
    try:
        prop = 'client_to_server'
        Config.client_to_server = config[prop]
        warn(prop)
    except:
        do_nothing = True
    try:
        prop = 'server_to_client'
        Config.server_to_client = config[prop]
        warn(prop)
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


def warn(prop):
    Console.forecolor(Fore.LIGHTRED_EX)
    Console.write("DANGER!!! ")
    Console.forecolor(Fore.RED)
    Console.writeln("Config.json contains a manually entered debug encryption key value '" + prop + "'. This configuration exists only for dev/debug and represents a significant security risk for a production environment.  Delete the '" + prop + "' entry from SimpleRpa.json before deploying to production.")
    Console.forecolor(Fore.WHITE)


if __name__ == '__main__':
    configure()

    if Config.protocol == "WebService":
        _Web_Comm.run(Config.port, Config.key, Config.iv, Config.verbose_level)
    elif Config.protocol == "Win32Pipe":
        _Win32_Comm.Pipe.run(Config.key, Config.iv, Config.client_to_server, Config.server_to_client, Config.verbose_level)
