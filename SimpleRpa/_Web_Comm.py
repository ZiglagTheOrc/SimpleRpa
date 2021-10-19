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
import socket
import cherrypy
import datetime
import json
import _Steganography
import _Comm_Convergence as cc
from colorama import Fore


class WebServer(object):
    """
    This class creates a local web service to facilitate communication cross platforms.
    Windows users should use _Win32_Comm named pipes instead of this method.
    This class was put here primarily for Linux and Mac OS X users.
    """
    key = ''
    iv = ''
    verbose_level = 0

    def __init__(self, key, iv, verbose_level):
        """
        Constructs a new instance of the WebServer class.
        Args:
            key: The encryption key to use for communications.
            iv: The initialization vector to use for communications.
            verbose_level: The verbosity level the server should use.
        """
        self.key = key
        self.iv = iv
        self.verbose_level = verbose_level
        cc.log_header("Using Rest Protocol")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def request_receiver(self):
        """
        Intakes webrequests for the SimpleRPA service.
        Returns:
        json
        """
        try:
            pkg = cherrypy.request.json
            try:
                jsn = _Steganography.unpackage(pkg, self.key, self.iv)
            except:
                print(Fore.LIGHTYELLOW_EX + str(datetime.datetime.now()) + Fore.LIGHTRED_EX +
                      " INVALID REQUEST RECEIVED! " + Fore.YELLOW + " Someone may be trying to access the service!")

            if jsn == '{"method":"shut_down"}':
                cherrypy.engine.exit()
                return

            wr = json.loads(jsn)

            reply = cc.run_method(self.verbose_level, wr, jsn, self.key, self.iv)

            if '"length":' in reply:
                return json.loads(reply)
            else:
                # region Send response back to client.
                resp = {"response": "SUCCESS", "content": _Steganography.encrypt(reply, self.key, self.iv)}
                return resp
                # endregion
        except:
            e_type, e_value, e_trace = sys.exc_info()
            return {"response": "EXCEPTION", "content": str(e_type) + ": " + str(e_value)}


# region Detects the real local IP. (zzNOT Local Host or 127.0.0.1)
def _get_ip():
    """
    Detects the real local IP. (NOT Local Host or 127.0.0.1)
    Returns: string
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
# endregion


def run(port, key, iv, verbose_level=0):
    """
    Starts the web service.
    Args:
        port: The port to establish the service on.
        key: The encryption key to use for communications.
        iv: The initialization vector to use for communications.
        verbose_level: The level of verbosity the server should have.

    Returns: void
    """
    ip = _get_ip()
    print(ip)
    config = {'server.socket_host': '0.0.0.0', 'server.socket_port': port}
    cherrypy.config.update(config)
    cherrypy.quickstart(WebServer(key, iv, verbose_level))
