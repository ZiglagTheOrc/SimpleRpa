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
using System.Collections.Generic;
using Transmissions;

namespace SimpleRPA
{
    /// <summary>
    /// This class performs fast OCR for screen shot images.
    /// This instantiable because there is benefit to being able to dynamically load different font mappings specific
    /// to the needs of the specific system(s) that are being worked with.
    /// </summary>
    public class SimpleOcr
    {
        private static List<string> _FontMapNames = new List<string>();
        private static List<string> _FontMapPaths = new List<string>();
        private static dynamic _ps = null;
        /// <summary>
        /// Instantiates a new QuickOCR object.
        /// </summary>
        /// <param name="fontMapPath">The path to your FontMap folder.</param>
        public SimpleOcr(string fontMapPath)
        {
            if (_ps == null)
                _ps = Config.GetServiceConnection();
            if (_FontMapPaths.Contains(fontMapPath))
                return;
            _FontMapPaths.Add(fontMapPath);
            AddFont(fontMapPath);

            //string json = System.IO.File.ReadAllText("Z:\\fontmap\\font_map.json");
            string json = System.IO.File.ReadAllText(fontMapPath + "\\font_map.json");
            dynamic items = Serialize.ToDynamic(json);
            string name = items["name"];
            if (!_FontMapNames.Contains(name))
                _FontMapNames.Add(name);
        }
        /// <summary>
        /// Instantiates a new QuickOCR object.
        /// </summary>
        /// <param name="fontMapPath">The list of paths to your FontMap folders.</param>
        public SimpleOcr(List<string> fontMapPaths)
        {
            List<string> paths = new List<string>();
            for (int i = 0; i < fontMapPaths.Count; i++)
                if (!_FontMapPaths.Contains(fontMapPaths[i]))
                    paths.Add(fontMapPaths[i]);
            if (_ps == null)
                _ps = Config.GetServiceConnection();
            for (int i = 0; i < paths.Count; i++)
            {
                _FontMapPaths.Add(paths[i]);
                AddFont(fontMapPaths[i]);
            }
        }
        /// <summary>
        /// Takes a screen shot of the specified area then performs a quick OCR on the image.
        /// </summary>
        /// <param name="area">The area of the screen to screen shot.</param>
        /// <param name="ocrThreshold">The matching threshold to use when matching font maps to the screen shots.</param>
        /// <param name="captureThreshold">The capture threshold to us when reducing text to monochrome.</param>
        /// <param name="useWidget">If true will display the field highlighter widget.</param>
        /// <returns>string</returns>
        /// <exception cref="PythonException">Catches any exceptions thrown by the SimpleRPA python service.</exception>
        public string PerformOcr(Rectangle area, decimal ocrThreshold = .94m, byte captureThreshold = 148, bool? useWidget = null, int duration = 0)
        {
            string widget = Mouse.GetWidgetSettings(useWidget);
            string fmps = string.Empty;
            for (int i = 0; i < _FontMapNames.Count; i++)
                fmps += "\"" + _FontMapNames[i] + "\",";
            fmps = (fmps.Substring(0, fmps.Length - 1)).Replace("\\","\\\\");
            object[] items = new object[] { area.X, area.Y, area.Width, area.Height, ocrThreshold, captureThreshold, fmps, widget, duration };
            string json = ("{'method':'simple_ocr_perform_ocr','x':%1,'y':%2,'width':%3,'height':%4,'ocr_threshold':%5,'capture_threshold':%6,'font_maps':[%7],'use_widget':'%8','duration':%9}").ToJson(items);
            dynamic response = _ps.Query(json);
        
            return response["text"];
        }
        private void AddFont(string fontMapPath)
        {
            string json = ("{'method':'simple_ocr_add_font','path':'" + fontMapPath.Replace("\\", "\\\\") + "'}").ToJson();
            dynamic response = _ps.Query(json);
        }
    }
}