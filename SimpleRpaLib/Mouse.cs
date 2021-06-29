#region License
/* 
 *
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
 */
#endregion
using System.Drawing;
using Transmissions;

namespace SimpleRPA
{
    /// <summary>
    /// All the available mouse buttons to click.
    /// </summary>
    public enum Buttons
    {
        LEFT,
        MIDDLE,
        RIGHT,
        PRIMARY,
        SECONDARY
    }
    /// <summary>
    /// All the types of clicks that can be performed.
    /// </summary>
    public enum Clicks
    {
        SINGLE,
        DOUBLE
    }
    /// <summary>
    /// All the options available to determine how the mouse moves between points.
    /// </summary>
    public enum Tweening
    {
        LINEAR,
        IN_QUAD,
        OUT_QUAD,
        IN_OUT_QUAD,
        IN_CUBIC,
        OUT_CUBIC,
        IN_OUT_CUBIC,
        IN_QUART,
        OUT_QUART,
        IN_OUT_QUART,
        IN_QUINT,
        OUT_QUINT,
        IN_OUT_QUINT,
        IN_SINE,
        OUT_SINE,
        IN_OUT_SINE,
        IN_EXPO,
        OUT_EXPO,
        IN_OUT_EXPO,
        IN_CIRC,
        OUT_CIRC,
        IN_OUT_CIRC,
        IN_ELASTIC,
        OUT_ELASTIC,
        IN_OUT_ELASTIC,
        IN_BACK,
        OUT_BACK,
        IN_OUT_BACK,
        IN_BOUNCE,
        OUT_BOUNCE,
        IN_OUT_BOUNCE
    }
    /// <summary>
    /// This class manages all the mouse operations.
    /// This class is static because we are presuming that there is only 1 mouse available.  Even if there is more
    /// than one mouse available they all perform the same singular function therefore there would be no value added
    /// in having multiple instantiations of this class.
    /// </summary>
    public static class Mouse
    {
        private static decimal _Interval = 0m;
        private static decimal _Duration = 0m;

        /// <summary>
        /// Sets the class wide default interval value for all methods. (default=0)
        /// </summary>
        public static decimal Interval
        {
            get { return _Interval; }
            set { _Interval = value; }
        }

        /// <summary>
        /// Sets the class wide duration interval value for all methods. (default=0)
        /// </summary>
        public static decimal Duration
        {
            get { return _Duration; }
            set { _Duration = value; }
        }

        /// <summary>
        /// If read this property will return the position of the mouse cursor.
        /// If written to it will move the mouse to that point.
        /// </summary>
        /// <exception cref="PythonException">Catches any exceptions thrown by the SimpleRPA python service.</exception>
        public static Point Position
        {
            get
            {
                var pc = Config.GetServiceConnection();
                string json = "{'method':'mouse_position'}".ToJson();
                dynamic response = pc.Query(json);
                int x = response["x"];
                int y = response["y"];
                return new Point(x, y);
            }
            set { Move(value, 0); }
        }

        /// <summary>
        /// Moves the mouse to the specified point.
        /// </summary>
        /// <param name="pt">The point to move to.</param>
        /// <param name="duration">How long the operation should take.</param>
        /// <param name="tween">How the mouse moves toward the specified point.</param>
        /// <param name="logScreenshot">If true will record a screen shot on method call.</param>
        /// <param name="useWidget">If true will display the field highlighter widget.</param>
        /// <exception cref="PythonException">Catches any exceptions thrown by the SimpleRPA python service.</exception>
        public static void Move(Point pt, decimal duration = -1m, Tweening tween = Tweening.LINEAR,
            bool logScreenshot = false, bool? useWidget = null)
        {
            string widget = GetWidgetSettings(useWidget);
            if (duration == -1)
                duration = _Duration;
            var pc = Config.GetServiceConnection();
            object[] items = new object[] { pt.X, pt.Y, duration, tween, logScreenshot, widget };
            string json = ("{'method':'mouse_move','x':%1,'y':%2,'duration':%3,'tween':'%4','log_screenshot':%5,'use_widget':'%6'}").ToJson(items);
            dynamic response = pc.Query(json);
        }

        /// <summary>
        /// Clicks the specified mouse button.
        /// </summary>
        /// <param name="button">Which button to click.</param>
        /// <param name="click">The number of clicks to make.</param>
        /// <param name="interval">The time between clicks</param>
        /// <param name="useWidget">If true will display the field highlighter widget.</param>
        /// <param name="logScreenshot">If true will record a screen shot on method call.</param>
        public static void Click(Buttons button = Buttons.LEFT, Clicks click = Clicks.SINGLE, decimal interval = -1m,
            bool logScreenshot = false, bool? useWidget = null)
        {
            if (interval == -1)
                interval = _Interval;

            Point pt = new Point(-1, -1);
            Click(pt, button, click, interval, 0m, Tweening.LINEAR, logScreenshot, useWidget);
        }

        /// <summary>
        /// Moves the mouse to the specified point the clicks the mouse in the specified manner.
        /// </summary>
        /// <param name="pt">The point to move to.</param>
        /// <param name="button">Which button to click.</param>
        /// <param name="click">The number of clicks to make.</param>
        /// <param name="interval">The time between clicks</param>
        /// <param name="duration"></param>
        /// <param name="tween">How the mouse moves toward the specified point.</param>
        /// <param name="logScreenshot">If true will record a screen shot on method call.</param>
        /// <param name="useWidget">If true will display the field highlighter widget.</param>
        /// <exception cref="PythonException">Catches any exceptions thrown by the SimpleRPA python service.</exception>
        public static void Click(Point pt, Buttons button = Buttons.LEFT, Clicks click = Clicks.SINGLE,
            decimal interval = -1m, decimal duration = -1m, Tweening tween = Tweening.LINEAR,
            bool logScreenshot = false, bool? useWidget = null)
        {
            string widget = GetWidgetSettings(useWidget);

            if (interval == -1)
                interval = _Interval;
            if (duration == -1)
                duration = _Duration;

            int clks = click == Clicks.SINGLE ? 1 : 2;
            var pc = Config.GetServiceConnection();
            object[] items = new object[] { pt.X, pt.Y, button, clks, interval, duration, tween, logScreenshot, widget };
            string json = ("{'method':'mouse_click','x':%1,'y':%2,'button':'%3','clicks':%4,'interval':%5,'duration':%6,'tween':'%7','log_screenshot':%8,'use_widget':'%9'}").ToJson(items);
            dynamic response = pc.Query(json);
        }
        /// <summary>
        /// Moves the mouse to the start point, clicks and drags the mouse to the end point the releases the mouse button.
        /// </summary>
        /// <param name="start">The point to start at.</param>
        /// <param name="finish">The point to finish at.</param>
        /// <param name="duration">How long the operation should take.</param>
        /// <param name="tween">How the mouse moves toward the specified point.</param>
        /// <param name="button">The specified button to press.</param>
        /// <param name="logScreenshot">If true will record a screen shot on method call.</param>
        /// <param name="useWidget">If true will display the field highlighter widget.</param>
        /// <exception cref="PythonException">Catches any exceptions thrown by the SimpleRPA python service.</exception>
        public static void Drag(Point start, Point finish, decimal duration = -1m, Tweening tween = Tweening.LINEAR,
            Buttons button = Buttons.PRIMARY, bool logScreenshot = false, bool? useWidget = null)
        {
            string widget = GetWidgetSettings(useWidget);

            if (duration == -1)
                duration = _Duration;

            var pc = Config.GetServiceConnection();
            object[] items = new object[] { start.X, start.Y, finish.X, finish.Y, duration, tween, button, logScreenshot, widget };
            string json = ("{'method':'mouse_drag','x1':%1,'y1':%2,'x2':%3,'y2':%4,'duration':%5,'tween':'%6','button':'%7','log_screenshot':%8,'use_widget':'%9'}").ToJson(items);
            dynamic response = pc.Query(json);
        }

        /// <summary>
        /// Scrolls the mouse.  Positive number scrolls up, negative number scrolls down.
        /// </summary>
        /// <param name="clicks">The number of scroll clicks to make.</param>
        /// <param name="useWidget">If true will display the field highlighter widget.</param>
        /// <param name="logScreenshot">If true will record a screen shot on method call.</param>
        public static void Scroll(int clicks = 1, bool logScreenshot = false)
        {
            Point pt = new Point(-1, -1);
            Scroll(pt, clicks, logScreenshot, false);
        }

        /// <summary>
        /// Moves the mouse to the specified point then scrolls the mouse.  Positive number scrolls up,
        /// negative number scrolls down.
        /// </summary>
        /// <param name="pt">The point to move to.</param>
        /// <param name="clicks">The number of clicks to make.</param>
        /// <param name="logScreenshot">If true will record a screen shot on method call.</param>
        /// <param name="useWidget">If true will display the field highlighter widget.</param>
        /// <exception cref="PythonException">Catches any exceptions thrown by the SimpleRPA python service.</exception>
        public static void Scroll(Point pt, int clicks = 1, bool logScreenshot = false, bool? useWidget = null)
        {
            string widget = GetWidgetSettings(useWidget);

            var pc = Config.GetServiceConnection();
            object[] items = new object[] { pt.X, pt.Y, clicks, logScreenshot, widget };
            string json = ("{'method':'mouse_scroll','x':%1,'y':%2,'clicks':%3,'log_screenshot':%4,'use_widget':'%5'}").ToJson(items);
            dynamic response = pc.Query(json);
        }

        /// <summary>
        /// Presses down on the specified mouse button.
        /// </summary>
        /// <param name="button">The button to press.</param>
        /// <param name="logScreenshot">If true will record a screen shot on method call.</param>
        /// <param name="useWidget">If true will display the field highlighter widget.</param>
        /// <exception cref="PythonException">Catches any exceptions thrown by the SimpleRPA python service.</exception>
        public static void Down(Buttons button = Buttons.PRIMARY, bool logScreenshot = false, bool? useWidget = null,
            decimal duration = 0)
        {
            Point pt = new Point(-1, -1);
            Down(pt, button, Tweening.LINEAR, logScreenshot, useWidget, duration);
        }

        /// <summary>
        /// Moves to the specified point then presses the specified mouse button down.
        /// </summary>
        /// <param name="pt">The point to move to.</param>
        /// <param name="button">The button to press.</param>
        /// <param name="tween">How the mouse moves toward the specified point.</param>
        /// <param name="logScreenshot">If true will record a screen shot on method call.</param>
        /// <param name="useWidget">If true will display the field highlighter widget.</param>
        /// <exception cref="PythonException">Catches any exceptions thrown by the SimpleRPA python service.</exception>
        public static void Down(Point pt, Buttons button = Buttons.PRIMARY, Tweening tween = Tweening.LINEAR,
            bool logScreenshot = false, bool? useWidget = null, decimal duration = 0)
        {
            string widget = GetWidgetSettings(useWidget);

            var pc = Config.GetServiceConnection();
            object[] items = new object[] { pt.X, pt.Y, button, tween, logScreenshot, widget, duration };
            string json = ("{'method':'mouse_down','x':%1,'y':%2,'button':'%3','tween':'%4','log_screenshot':%5,'use_widget':'%6','duration':%7}").ToJson(items);
            dynamic response = pc.Query(json);
        }

        /// <summary>
        /// Releases the specified mouse button.
        /// </summary>
        /// <param name="button">The button to press.</param>
        /// <param name="logScreenshot">If true will record a screen shot on method call.</param>
        /// <param name="useWidget">If true will display the field highlighter widget.</param>
        /// <exception cref="PythonException">Catches any exceptions thrown by the SimpleRPA python service.</exception>
        public static void Up(Buttons button = Buttons.PRIMARY, bool logScreenshot = false, bool? useWidget = null)
        {
            Point pt = new Point(-1, -1);
            Up(pt, button, Tweening.LINEAR, logScreenshot, useWidget);
        }

        /// <summary>
        /// Moves the mouse to the specified point and then releases the specified mouse button.
        /// </summary>
        /// <param name="pt"></param>
        /// <param name="button">The button to press.</param>
        /// <param name="tween">How the mouse moves toward the specified point.</param>
        /// <param name="logScreenshot">If true will record a screen shot on method call.</param>
        /// <param name="useWidget">If true will display the field highlighter widget.</param>
        /// <exception cref="PythonException">Catches any exceptions thrown by the SimpleRPA python service.</exception>
        public static void Up(Point pt, Buttons button = Buttons.PRIMARY, Tweening tween = Tweening.LINEAR,
            bool logScreenshot = false, bool? useWidget = null, decimal duration = 0)
        {
            string widget = GetWidgetSettings(useWidget);

            var pc = Config.GetServiceConnection();
            object[] items = new object[] { pt.X, pt.Y, button, tween, logScreenshot, widget, duration };
            string json = ("{'method':'mouse_up','x':%1,'y':%2,'button':'%3','tween':'%4','log_screenshot':%5,'use_widget':'%6','duration':%7}").ToJson(items);
            dynamic response = pc.Query(json);
        }

        internal static string GetWidgetSettings(bool? useWidget = null)
        {
            string widget = "None";
            if (useWidget.HasValue)
                if (useWidget.Value)
                    widget = "True";
                else
                    widget = "False";
            return widget;
        }
    }
}