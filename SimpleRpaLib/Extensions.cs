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

/// <summary>
/// Extends classes.
/// </summary>
public static class Extensions
{
    /// <summary>
    /// Returns the center point of a rectangle.
    /// </summary>
    /// <param name="value">This rectangle.</param>
    /// <returns>Point</returns>
    public static Point GetCenter(this Rectangle value)
    {
        int x = value.Width / 2;
        int y = value.Height / 2;
        return new Point(value.X + x, value.Y + y);
    }
    /// <summary>
    /// Extends the replace method to replace a string with multiple data types.
    /// </summary>
    /// <param name="value">This string.</param>
    /// <param name="text">The text to find.</param>
    /// <param name="obj">The object convert to a string and to replace the text with.</param>
    /// <returns>string</returns>
    public static string Replace(this string value, string text, object obj)
    {
        if(obj is bool)
            return value.Replace(text, obj.ToString().ToLower());
        return value.Replace(text, obj.ToString());
    }
    /// <summary>
    /// Returns wheter of not this string is null or empty.
    /// </summary>
    /// <param name="value">This string.</param>
    /// <returns>bool</returns>
    public static bool IsNullOrEmpty(this string value)
    {
        return string.IsNullOrEmpty(value);
    }
    /// <summary>
    /// Replaces all single quotes in the string with double quotes.
    /// </summary>
    /// <param name="value">This string.</param>
    /// <returns>string</returns>
    public static string ToJson(this string value, string replace = null)
    {
        string text = value.Replace("'", "\"");
        if (replace != null)
            text = text.Replace("%1", replace);
        return text;
    }
    /// <summary>
    /// Replaces all single quotes in the string with double quotes then inserts the string array in the appropriate places. 
    /// </summary>
    /// <param name="value">This string.</param>
    /// <param name="replace">Array of strings to insert.</param>
    /// <returns></returns>
    public static string ToJson(this string value, object[] replace)
    {
        string text = value.Replace("'", "\"");
        for (int i = 0; i < replace.Length; i++)
        {
            string item = replace[i].ToString();
            if (item == "True")
                item = "true";
            else if (item == "False")
                item = "false";
            text = text.Replace("%" + (i + 1), item);
        }
        return text;
    }
}