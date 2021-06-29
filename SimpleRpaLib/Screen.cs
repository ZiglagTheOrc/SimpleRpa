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
using System;
using System.Collections.Generic;
using System.Drawing;
using Transmissions;

namespace SimpleRPA
{
    /// <summary>
    /// RPA interface to the screen.
    /// </summary>
    public static class Screen
    {
        /// <summary>
        /// Returns the color for the specified pixel.
        /// </summary>
        /// <param name="pt">The point of the pixel.</param>
        /// <returns>Color</returns>
        /// <exception cref="PythonException">Catches any exceptions thrown by the SimpleRPA python service.</exception>
        public static Color GetPixelColor(Point pt, bool? useWidget = null, decimal duration = 0m)
        {
            string widget = Mouse.GetWidgetSettings(useWidget);
            var pc = Config.GetServiceConnection();
            object[] items = new object[] { pt.X, pt.Y, widget, duration };
            string json = ("{'method':'screen_get_pixel_color','x':%1,'y':%2,'use_widget':'%3','duration':%4}").ToJson(items);
            dynamic response = pc.Query(json);
            int red = Convert.ToInt32(response["red"]);
            int green = Convert.ToInt32(response["green"]);
            int blue = Convert.ToInt32(response["blue"]);
            return Color.FromArgb(red, green, blue);
        }
        /// <summary>
        /// Returns the nearest known color for the specified pixel.
        /// </summary>
        /// <param name="pt">The point of the pixel.</param>
        /// <returns>Color</returns>
        /// <exception cref="PythonException">Catches any exceptions thrown by the SimpleRPA python service.</exception>
        public static Color GetKnownColor(Point pt, bool? useWidget = null, decimal duration = 0m)
        {
            string widget = Mouse.GetWidgetSettings(useWidget);
            var pc = Config.GetServiceConnection();
            object[] items = new object[] { pt.X, pt.Y, widget, duration };
            string json = ("{'method':'screen_get_known_color','x':%1,'y':%2,'use_widget':'%3','duration':%4}").ToJson(items);
            dynamic response = pc.Query(json);
            Enum.TryParse(response["name"].ToString(), out KnownColor color);
            return Color.FromKnownColor(color);
        }
        /// <summary>
        /// Returns the nearest console color for the specified pixel.
        /// </summary>
        /// <param name="pt">The point of the pixel.</param>
        /// <returns>ConsoleColor</returns>
        /// <exception cref="PythonException">Catches any exceptions thrown by the SimpleRPA python service.</exception>
        public static ConsoleColor GetConsoleColor(Point pt, bool? useWidget = null, decimal duration = 0m)
        {
            string widget = Mouse.GetWidgetSettings(useWidget);
            var pc = Config.GetServiceConnection();
            object[] items = new object[] { pt.X, pt.Y, widget, duration };
            string json = ("{'method':'screen_get_console_color','x':%1,'y':%2,'use_widget':'%3','duration':%4}").ToJson(items);
            dynamic response = pc.Query(json);
            string clr = response["name"];
            if (clr == "Orange")
                clr = "Dark Yellow";
            Enum.TryParse(clr, out ConsoleColor color);
            return color;
        }
        /// <summary>
        /// Captures the specified area of the screen.
        /// </summary>
        /// <param name="area">The area of the screen to capture.</param>
        /// <returns>Image</returns>
        /// <exception cref="PythonException">Catches any exceptions thrown by the SimpleRPA python service.</exception>
        public static Image Capture(Rectangle area, bool? useWidget = null, decimal duration = 0m)
        {
            string widget = Mouse.GetWidgetSettings(useWidget);
            var pc = Config.GetServiceConnection();
            object[] items = new object[] { area.X, area.Y, area.Width, area.Height, widget, duration };
            string json = ("{'method':'screen_capture','x':%1,'y':%2,'width':%3,'height':%4,'use_widget':'%5','duration':%6}").ToJson(items);
            byte[] response = pc.QueryToBytes(json);
            Bitmap bmp = new Bitmap(area.Height, area.Height);
            int i = 0;
            for (int y = 0; y < area.Width; y++)
            {
                for (int x = 0; x < area.Width; x++)
                {
                    bmp.SetPixel(x, y, Color.FromArgb(response[i + 1], response[i + 2], response[i]));
                    i += 3;
                }
            }

            return bmp;
        }
        /// <summary>
        /// Returns all areas of the screen to for all found matches of the specified image.
        /// </summary>
        /// <param name="filename">The image file name to use as reference.</param>
        /// <param name="threshold">The percentage threshold to match to. (Default: 0.9 [90%])</param>
        /// <returns>Rectangle[]</returns>
        /// <exception cref="PythonException">Catches any exceptions thrown by the SimpleRPA python service.</exception>
        public static Rectangle[] FindImage(string filename, decimal threshold = 0.9m, bool? useWidget = null,
            decimal duration = 0m)
        {
            string widget = Mouse.GetWidgetSettings(useWidget);
            var pc = Config.GetServiceConnection();
            object[] items = new object[] { filename.Replace("\\", "\\\\"), threshold, widget, duration };
            string json = ("{'method':'screen_find_image','filename':'%1','threshold':%2,'use_widget':'%3','duration':%4}").ToJson(items);
            dynamic response = pc.Query(json);
            List<Rectangle> rectangles = new List<Rectangle>();
            dynamic locs = response["locs"];
            int i = 0;
            while (true)
            {
                try
                {
                    dynamic rect = locs[i];
                    rectangles.Add(new Rectangle(Convert.ToInt16(rect["x"]), Convert.ToInt16(rect["y"]),
                        Convert.ToInt16(rect["w"]), Convert.ToInt16(rect["h"])));
                }
                catch (ArgumentOutOfRangeException e)
                {
                    break;
                }

                i++;
            }

            return rectangles.ToArray();
        }
    }
}