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
import sys
from threading import Thread
from tkinter import *


class Widget (Thread):
    """
    Displays a rectangular widget over the specified area of the screen.
    """
    rect = tuple()
    duration = 3

    def __init__(self, rect, duration=3):
        """
        Constructs a new widget instance.
        :param rect: The are the widget should cover.
        :param duration: How long, in seconds, the widget should display for.
        """
        Thread.__init__(self)
        self.rect = (rect[0] - 4, rect[1] - 4, rect[2] + 8, rect[3] + 8)
        self.duration = duration

    def run(self):
        """
        Displays the widget
        :return: void
        """
        _widget(self.rect, self.duration)

    @staticmethod
    def _show_widget_pt(pt, duration):
        """
        Draws a square box around a single point on the screen.
        :param pt:  The point to draw around.
        :param duration: How long, in seconds, the widget should stay on the screen.
        :return: void
        """
        #region Calculate length based on operating system.
        if sys.platform == 'win32':
            length = duration - 0.1
        else:
            length = duration - 1
            if length < 0:
                length = 0
        #endregion

        if length < 0:
            length = 0
        widget = Widget((pt[0] - 8, pt[1] - 8, 16, 16), length)
        widget.start()

    @staticmethod
    def _show_widget_rect(rect, duration):
        """
        Draws a rectangle around the specified area.
        :param rect: The rectangular tuple to the widget should cover.
        :param duration: How long, in seconds, the widget should stay on the screen.
        :return: void
        """
        length = duration - 0.1
        if length < 0:
            length = 0
        widget = Widget(rect, length)
        widget.start()


def _widget(rect, duration):
    """
    Draws a rectangle around the specified area.
    :param rect: The rectangular tuple to the widget should cover.
    :param duration: How long, in seconds, the widget should stay on the screen.
    :return: void
    """
    widget = Tk()
    if sys.platform == "win32":
        widget.overrideredirect(True)
    else:
        widget.wm_attributes('-type', 'splash')
    widget.geometry(str(rect[2]) + 'x' + str(rect[3]) + '+' + str(rect[0]) + '+' + str(rect[1]))
    widget.config(bg='darkred')
    widget.attributes('-alpha',0.5)
    widget.call('wm', 'attributes', '.', '-topmost', '1')

    canvas = Canvas(
        widget,
        height=rect[3],
        width=rect[2],
        bg="darkred",
        highlightthickness=0
    )

    canvas.pack()

    canvas.create_rectangle(
        3, 3, rect[2]-3, rect[3]-3,
        outline='red',
        width=2,
        fill='#111')

    widget.after(int(duration * 1000), widget.destroy)

    widget.mainloop()