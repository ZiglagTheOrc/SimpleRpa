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
using System.Drawing;
using SimpleRPA;


namespace Demo
{
    class Program
    {
        [STAThread]
        static void Main(string[] args)
        {
            Config.StartService(Protocols.WebService);

            //Point pt = Mouse.Position; 
            //Mouse.Position = new Point(40, 130);
            //Mouse.Down();
            //Mouse.Up();
            //Mouse.Move(new Point(80,200));
            //Mouse.Click();
            //Mouse.Move(new Point(100, 110));
            //Mouse.Move(new Point(40,110)); 
            //Mouse.Drag(new Point(40,110), new Point(100,110), 2); 
            //Mouse.Drag(new Point(36,30), new Point(102,30), 2);
            //Mouse.Scroll(3); // Does not seem to be working?

            //Keyboard.Type("this is a test"); 
            //Keyboard.Press(Key.A); 
            //Keyboard.Press(Key.A, CommandKey.CTRL); 
            //Keyboard.Press(Key.N, new CommandKey[] { CommandKey.CTRL, CommandKey.SHIFT }); 
            //Keyboard.Type("o", CommandKey.ALT); 
            //Keyboard.Type("n", new CommandKey[] {CommandKey.CTRL, CommandKey.SHIFT}); 

            //Color c1 = Screen.GetPixelColor(new Point(33, 112));
            //System.Threading.Thread.Sleep(2000);
            //Color c2 = Screen.GetKnownColor(new Point(33, 112));
            //System.Threading.Thread.Sleep(2000);
            //ConsoleColor c3 = Screen.GetConsoleColor(new Point(33, 112));
            //System.Threading.Thread.Sleep(2000);
            //Image img = Screen.Capture(new Rectangle(0, 0, 128, 128));
            //Rectangle[] rects1 = Screen.FindImage("{PATH_TO_FILE}"); 
            //Rectangle[] rects2 = Screen.FindImage(@"{PATH_TO_FILE}"); 
            //SimpleOcr _default = new SimpleOcr("{PATH_TO_FOLDER}"); 
            //SimpleOcr _default = new SimpleOcr("{PATH_TO_FOLDER}"); 
            //string txt = _default.PerformOcr(new Rectangle(11, 255, 357, 38), .9m, 175); 

            Config.StopService();
        }
    }
}