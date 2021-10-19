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
import time
import _Platform_Convergence
from _Widget import Widget
from _Platform_Convergence import Config
from multipledispatch import dispatch


# Constants for the mouse button names:
class Btn:
    """
    An enumerated list of clickable mouse buttons.
    """
    LEFT = "left"
    MIDDLE = "middle"
    RIGHT = "right"
    PRIMARY = "primary"
    SECONDARY = "secondary"

# Constants for Mouse Tweening
class Tweening:
    """
    An enumerated list of all the different ways to tween the mouse.
    """
    LINEAR = _Platform_Convergence.linear
    IN_QUAD = _Platform_Convergence.easeInQuad
    OUT_QUAD = _Platform_Convergence.easeOutQuad
    IN_OUT_QUAD = _Platform_Convergence.easeInOutQuad
    IN_CUBIC = _Platform_Convergence.easeInCubic
    OUT_CUBIC = _Platform_Convergence.easeInOutQuad
    IN_OUT_CUBIC = _Platform_Convergence.easeInOutCubic
    IN_QUART = _Platform_Convergence.easeInQuart
    OUT_QUART = _Platform_Convergence.easeOutQuart
    IN_OUT_QUART = _Platform_Convergence.easeInOutQuart
    IN_QUINT = _Platform_Convergence.easeInQuint
    OUT_QUINT = _Platform_Convergence.easeOutQuint
    IN_OUT_QUINT = _Platform_Convergence.easeInOutQuint
    IN_SINE = _Platform_Convergence.easeInSine
    OUT_SINE = _Platform_Convergence.easeOutSine
    IN_OUT_SINE = _Platform_Convergence.easeInOutSine
    IN_EXPO = _Platform_Convergence.easeInExpo
    OUT_EXPO = _Platform_Convergence.easeOutExpo
    IN_OUT_EXPO = _Platform_Convergence.easeInOutExpo
    IN_CIRC = _Platform_Convergence.easeInCirc
    OUT_CIRC = _Platform_Convergence.easeOutCirc
    IN_OUT_CIRC = _Platform_Convergence.easeInOutCirc
    IN_ELASTIC = _Platform_Convergence.easeInElastic
    OUT_ELASTIC = _Platform_Convergence.easeOutElastic
    IN_OUT_ELASTIC = _Platform_Convergence.easeInOutElastic
    IN_BACK = _Platform_Convergence.easeInBack
    OUT_BACK = _Platform_Convergence.easeOutBack
    IN_OUT_BACK = _Platform_Convergence.easeInOutBack
    IN_BOUNCE = _Platform_Convergence.easeInBounce
    OUT_BOUNCE = _Platform_Convergence.easeOutBounce
    IN_OUT_BOUNCE = _Platform_Convergence.easeInOutBounce


# METHODS
def move(pt, duration=0.0, tween=Tweening.LINEAR, log_screenshot=False, use_widget=None):
    """
    Moves the mouse to the specified point.
    :param pt: A tuple of the point on the screen.
    :param duration: The amount of time the method should take.
    :param tween: How you would like to tween the mouse.
    :param log_screenshot: If true the method takes a screenshot after the action.
    :param use_widget: If true displays the field highlighting widget during operation.
    :return: void
    """
    if use_widget is None:
        use_widget = Config.use_widgets_by_default
        if duration == 0:
            duration = Config.default_widget_duration
    if use_widget:
        if pt is None:
            pt = position()
        Widget._show_widget_pt(pt, duration)
    _Platform_Convergence.move_to(pt[0], pt[1], duration, tween, log_screenshot, True)


def click(pt=None, clicks=1, interval=0.0, button=Btn.PRIMARY, duration=0.0, tween=Tweening.LINEAR, log_screenshot=False, use_widget=None):
    """
    Move to the point (if specified) and clicks the specified mouse button.
    :param pt: Tuple point on the screen to click on.
    :param clicks: The number of clicks to perform.
    :param interval: The time to take between clicks.
    :param button: Which button to click with.
    :param duration: The amount of time to take to perform the operation.
    :param tween: How you would like to tween the mouse.
    :param log_screenshot: If true the method takes a screenshot after the action.
    :param use_widget: If true displays the field highlighting widget during operation.
    :return: void
    """
    x = None
    y = None
    if isinstance(pt, type((int,int))):
        x = pt[0]
        y = pt[1]
    elif not isinstance(pt, type(None)):
        raise NotImplementedError('Type of pt must be tuple of none.')
    if use_widget is None:
        use_widget = Config.use_widgets_by_default
        if duration == 0:
            duration = Config.default_widget_duration
    if use_widget:
        if pt is None:
            pt = position()
        Widget._show_widget_pt(pt, duration)
    _Platform_Convergence.click(x, y, clicks, interval, button, duration, tween, log_screenshot, True)


def down(pt=None, button=Btn.PRIMARY, tween=Tweening.LINEAR, log_screenshot=False, use_widget=None, duration=0.0):
    """
    Move to the point (if specified) and presses the specified mouse button down.
    :param pt: Tuple point on the screen to click on.
    :param button: Which button to click with.
    :param tween: How you would like to tween the mouse.
    :param log_screenshot: If true the method takes a screenshot after the action.
    :param use_widget: If true displays the field highlighting widget during operation.
    :param duration: The amount of time the widget should display for.
    :return: void
    """
    x = None
    y = None
    if isinstance(pt, type((int,int))):
        x = pt[0]
        y = pt[1]
    elif not isinstance(pt, type(None)):
        raise NotImplementedError('Type of pt must be tuple of none.')
    if use_widget is None:
        use_widget = Config.use_widgets_by_default
        if duration == 0:
            duration = Config.default_widget_duration
    if use_widget:
        if pt is None:
            pt = position()
        Widget._show_widget_pt(pt, duration)
        time.sleep(duration)
    _Platform_Convergence.mouse_down(x, y, button, tween, log_screenshot, True)


def up(pt=None, button=Btn.PRIMARY, tween=Tweening.LINEAR, log_screenshot=False, use_widget=None, duration=0):
    """
    Move to the point (if specified) and releases the specified mouse button.
    :param pt: Tuple point on the screen to move to.
    :param button: Which button to click with.
    :param tween: How you would like to tween the mouse.
    :param log_screenshot: If true the method takes a screenshot after the action.
    :param use_widget: If true displays the field highlighting widget during operation.
    :param duration: The amount of time to display the widget for.
    :return: void
    """
    x = None
    y = None
    if isinstance(pt, type((int,int))):
        x = pt[0]
        y = pt[1]
    elif not isinstance(pt, type(None)):
        raise NotImplementedError('Type of pt must be tuple of none.')
    if use_widget is None:
        use_widget = Config.use_widgets_by_default
        if duration == 0:
            duration = Config.default_widget_duration
    if use_widget:
        if pt is None:
            pt = position()
        Widget._show_widget_pt(pt, duration)
        time.sleep(duration)
    _Platform_Convergence.mouse_up(x, y, button, tween, log_screenshot, False)


def scroll(clicks=1, pt=None, log_screenshot=False):
    """
    Clicks the scroll wheel on the mouse. Positive number scrolls up, negative number scrolls down.
    :param clicks: The number of clicks to make.
    :param pt: The point on the screen to move to.
    :param log_screenshot: If true the method takes a screenshot after the action.
    :return: void
    """
    x = None
    y = None
    if isinstance(pt, type((int,int))):
        x = pt[0]
        y = pt[1]
    elif not isinstance(pt, type(None)):
        raise NotImplementedError('Type of pt must be tuple or none.')
    _Platform_Convergence.scroll(clicks, x, y, 'scroll', log_screenshot, True)


def drag(start_pt, end_pt, duration=0.0, tween=Tweening.LINEAR, button=Btn.PRIMARY, log_screenshot=False, use_widget=None):
    """
    Moves to the start point, clicks and drags to the end point and releases the mouse.
    :param start_pt: The point to move to before clicking.
    :param end_pt: The point to drag to afterclicking.
    :param duration: The amount of time to take to perform the operation.
    :param tween: How you would like to tween the mouse.
    :param button: Which button to click with.
    :param log_screenshot: If true the method takes a screenshot after the action.
    :param use_widget: If true displays the field highlighting widget during operation.
    :return: void
    """
    if use_widget is None:
        use_widget = Config.use_widgets_by_default
        if duration == 0:
            duration = Config.default_widget_duration
    if use_widget:
        if start_pt[1] is None:
            pt = position()
        if end_pt[1] is None:
            pt = position()
        Widget._show_widget_pt(start_pt, duration / 2)
        Widget._show_widget_pt(end_pt, duration)
    _Platform_Convergence._mouse_move_drag('drag', start_pt[0], start_pt[1], end_pt[0], end_pt[1], duration, tween, button, log_screenshot)


def position():
    """
    Gets a tuple coordinate of where the mouse is located at.
    :return: tuple
    """
    return _Platform_Convergence.position()
