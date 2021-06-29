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
using System.Collections.Generic;
using Transmissions;

namespace SimpleRPA
{
    /// <summary>
    /// All the command keys available to hold down in conjunction with other keys.
    /// </summary>
    public enum CommandKey
    {
        CTRL,
        ALT,
        WIN,
        SHIFT,
        FN,
        CMD,
        OPT
    }
    /// <summary>
    /// All the available keys to press.
    /// </summary>
    public enum Key
    {
        BACK_SPACE,
        BREAK,
        CAPS_LOCK,
        DELETE,
        DOWN,
        END,
        ENTER,
        ESCAPE,
        F1,
        F2,
        F3,
        F4,
        F5,
        F6,
        F7,
        F8,
        F9,
        F10,
        F11,
        F12,
        F13,
        F14,
        F15,
        F16,
        F17,
        F18,
        F19,
        F20,
        F21,
        F22,
        F23,
        F24,
        HOME,
        INSERT,
        NUMLOCK,
        PAGE_DOWN,
        PAGE_UP,
        PRINT_SCREEN,
        LEFT,
        RIGHT,
        SCROLL_LOCK,
        SPACE,
        UP,
        TAB,
        NUM_0,
        NUM_1,
        NUM_2,
        NUM_3,
        NUM_4,
        NUM_5,
        NUM_6,
        NUM_7,
        NUM_8,
        NUM_9,
        ADD,
        SUBTRACT,
        MULTIPLY,
        DIVIDE,
        DECIMAL,
        RETURN,
        BROWSER_BACK,
        BROWSER_FAVORITES,
        BROWSER_FORWARD,
        BROWSER_HOME,
        BROWSER_REFRESH,
        BROWSER_SEARCH,
        BROWSER_STOP,
        PLAY,
        PAUSE,
        STOP,
        NEXT_TRACK,
        PREV_TRACK,
        VOLUME_DOWN,
        VOLUME_MUTE,
        VOLUME_UP,
        LAUNCH_APP1,
        LAUNCH_APP2,
        LAUNCH_MAIL,
        LAUNCH_MEDIA_SELECT,
        MODE_CHANGE,
        ACCEPT,
        APPS,
        CONVERT,
        EXECUTE,
        FINAL,
        HELP,
        NONCONVERT,
        SELECT,
        SEPARATOR,
        SLEEP,
        HANGUEL,
        HANGUL,
        HANJA,
        JUNJA,
        KANA,
        KANJI,
        YEN,
        EXCLAIM,
        HASH,
        DOLLAR,
        PERCENT,
        AMPERSAND,
        QUOTE,
        PARENTHESIS_LEFT,
        PARENTHESIS_RIGHT,
        ASTERISK,
        PLUS,
        COMMA,
        HYPHEN,
        PERIOD,
        FORWARD_SLASH,
        COLON,
        SEMICOLON,
        LESS_THAN,
        EQUALS,
        GREATER_THAN,
        QUESTION,
        AT,
        BRACKET_LEFT,
        BACK_SLASH,
        BRACKET_RIGHT,
        EXPONENT,
        UNDERSCORE,
        ACCENT,
        BRACE_LEFT,
        PIPE,
        BRACE_RIGHT,
        TILDE,
        KEY_0,
        KEY_1,
        KEY_2,
        KEY_3,
        KEY_4,
        KEY_5,
        KEY_6,
        KEY_7,
        KEY_8,
        KEY_9,
        A,
        B,
        C,
        D,
        E,
        F,
        G,
        H,
        I,
        J,
        K,
        L,
        M,
        N,
        O,
        P,
        Q,
        R,
        S,
        T,
        U,
        V,
        W,
        X,
        Y,
        Z
    }
    /// <summary>
    /// This class manages all the keyboard operations.
    /// This class is static because we are presuming that there is only 1 keyboard available.  Even if there is more
    /// than one keyboard available they all perform the same singular function therefore there would be no value added
    /// in having multiple instantiations of this class.
    /// </summary>
    public static class Keyboard
    {
        private static decimal _Interval = 0m;
        /// <summary>
        /// Sets the class wide default interval value for all methods. (default=0)
        /// </summary>
        public static decimal Interval { get { return _Interval; } set { _Interval = value; } }
        /// <summary>
        /// Presses the specified key.
        /// </summary>
        /// <param name="key">The key to press.</param>
        /// <param name="presses">The number of presses to make.</param>
        /// <param name="interval">The amount of time to take while pressing the key.</param>
        /// <param name="logScreenshot">If true will record a screen shot on method call.</param>
        public static void Press(Key key, int presses = 1, decimal interval = -1m, bool logScreenshot = false)
        {
            if (interval == -1)
                interval = _Interval;
            
            Press(key, new CommandKey[] {}, presses, interval, logScreenshot);
        }
        /// <summary>
        /// Presses the specified key.
        /// </summary>
        /// <param name="key">The key to press.</param>
        /// <param name="cmd">The command key to hold down during the press.</param>
        /// <param name="presses">The number of presses to make.</param>
        /// <param name="interval">The amount of time to take while pressing the key.</param>
        /// <param name="logScreenshot">If true will record a screen shot on method call.</param>
        public static void Press(Key key, CommandKey cmd, int presses = 1, decimal interval = -1m, bool logScreenshot = false)
        {
            if (interval == -1)
                interval = _Interval;

            Press(key, new CommandKey[] { cmd }, presses,interval, logScreenshot);
        }
        /// <summary>
        /// Presses the specified key.
        /// </summary>
        /// <param name="key">The key to press.</param>
        /// <param name="cmds">An array of command keys to hold down during the key press.</param>
        /// <param name="presses">The number of presses to make.</param>
        /// <param name="interval">The amount of time to take while pressing the key.</param>
        /// <param name="logScreenshot">If true will record a screen shot on method call.</param>
        public static void Press(Key key, CommandKey[] cmds, int presses = 1, decimal interval = -1m, bool logScreenshot = false)
        {
            if (interval == -1)
                interval = _Interval;

            string ja = SerializeList(cmds);
            dynamic pc = Config.GetServiceConnection();
            object[] items = new object[] { key, ja, presses, interval, logScreenshot };
            string json = ("{'method':'keyboard_press','key':'%1','command_keys':%2,'presses':%3,'interval':%4,'log_screenshot':%5}").ToJson(items);
            dynamic response = pc.Query(json);
        }
        /// <summary>
        /// Types the specified text.
        /// </summary>
        /// <param name="text">The text to type out</param>
        /// <param name="interval">The amount of time to take while pressing the key.</param>
        /// <param name="logScreenshot">If true will record a screen shot on method call.</param>
        public static void Type(string text, decimal interval = -1m, bool logScreenshot = false)
        {
            if (interval == -1)
                interval = _Interval;

            Type(text, new CommandKey[] {}, interval, logScreenshot);
        }
        /// <summary>
        /// Types the specified text.
        /// </summary>
        /// <param name="text">The text to type out</param>
        /// <param name="cmd">The command key to hold down during the press.</param>
        /// <param name="interval">The amount of time to take while pressing the key.</param>
        /// <param name="logScreenshot">If true will record a screen shot on method call.</param>
        public static void Type(string text, CommandKey cmd, decimal interval = -1m, bool logScreenshot = false)
        {
            if (interval == -1)
                interval = _Interval;

            Type(text, new CommandKey[] { cmd }, interval, logScreenshot);
        }
        /// <summary>
        /// Types the specified text.
        /// </summary>
        /// <param name="text">The text to type out</param>
        /// <param name="cmds">An array of command keys to hold down during the key press.</param>
        /// <param name="interval">The amount of time to take while pressing the key.</param>
        /// <param name="logScreenshot">If true will record a screen shot on method call.</param>
        public static void Type(string text, CommandKey[] cmds, decimal interval = -1m, bool logScreenshot = false)
        {
            if (interval == -1)
                interval = _Interval;

            string ja = SerializeList(cmds);
            var pc = Config.GetServiceConnection();
            object[] items = new object[] { text, ja, interval, logScreenshot };
            string json = ("{'method':'keyboard_type','text':'%1','command_keys':%2,'interval':%3,'log_screenshot':%4}").ToJson(items);
            dynamic response = pc.Query(json);
        }

        private static string SerializeList(CommandKey[] cmds)
        {
            List<string> cks = new List<string>();
            for (int i = 0; i < cmds.Length; i++)
                cks.Add(cmds[i].ToString().ToLower());
            return Serialization<List<string>>.Serialize(new List<string>(cks));
        }
    }
}