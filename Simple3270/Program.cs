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
using System.IO;
using System.Text;
using Simple3270;
using Transmissions;

namespace Simple_3270
{
    class Program
    {
        static void Main(string[] args)
        {
            #region Load the json config file.
            if (!File.Exists("Simple3270.json"))
            {
                Console.WriteLine("The configuration file 'Simple3270.json' is missing.");
                return;
            }
            string json = File.ReadAllText("Simple3270.json");
            dynamic config = Serialize.ToDynamic(json);
            bool isDebug = false;
            #endregion

            #region Set config settings from file.
            string protocol = string.Empty;
            string key = string.Empty;
            string iv = string.Empty;
            string input = string.Empty;
            string output = string.Empty;
            try
            { 
                protocol = config["protocol"];
                Console.ForegroundColor = ConsoleColor.Red;
                Console.Write("DANGER!!! ");
                Console.ForegroundColor = ConsoleColor.DarkRed;
                Console.WriteLine("Config.json contains a manually entered debug encryption key value 'protocol'. This configuration exists only for dev/debug and represents a significant security risk for a production environment.  Delete the 'protocol' entry from config.json before deploying to production.");
            }
            catch { }
            try
            {
                key = config["key"];
                Console.ForegroundColor = ConsoleColor.Red;
                Console.Write("DANGER!!! ");
                Console.ForegroundColor = ConsoleColor.DarkRed;
                Console.WriteLine("Config.json contains a manually entered debug encryption key value 'key'. This configuration exists only for dev/debug and represents a significant security risk for a production environment.  Delete the 'key' entry from config.json before deploying to production.");
            }
            catch { }
            try
            {
                iv = config["iv"];
                Console.ForegroundColor = ConsoleColor.Red;
                Console.Write("DANGER!!! ");
                Console.ForegroundColor = ConsoleColor.DarkRed;
                Console.WriteLine("Config.json contains a manually entered debug encryption key value 'iv'. This configuration exists only for dev/debug and represents a significant security risk for a production environment.  Delete the 'iv' entry from config.json before deploying to production.");
            }
            catch { }
            try
            {
                input = config["client_to_server"];
                Console.ForegroundColor = ConsoleColor.Red;
                Console.Write("DANGER!!! ");
                Console.ForegroundColor = ConsoleColor.DarkRed;
                Console.WriteLine("Config.json contains a manually entered debug encryption key value 'client_to_server'. This configuration exists only for dev/debug and represents a significant security risk for a production environment.  Delete the 'client_to_server' entry from config.json before deploying to production.");
            }
            catch { }
            try
            {
                output = config["server_to_client"];
                Console.ForegroundColor = ConsoleColor.Red;
                Console.Write("DANGER!!! ");
                Console.ForegroundColor = ConsoleColor.DarkRed;
                Console.WriteLine("Config.json contains a manually entered debug encryption key value 'server_to_client'. This configuration exists only for dev/debug and represents a significant security risk for a production environment.  Delete the 'server_to_client' entry from config.json before deploying to production.");
            }
            catch { }
            string server = config["server"];
            int port = config["port"];
            bool useSsl = config["use_ssl"];
            string lu = config["lu"];
            int verbose_level = config["verbose_level"];
            Simple3270Config cfg = new Simple3270Config(server, port, useSsl, lu);
            cfg.TerminalType = config["terminal_type"];
            cfg.FastScreenMode = config["fast_screen_mode"];
            cfg.Debug = config["debug"];
            cfg.ColorDepth = config["color_depth"];
            cfg.ActionTimeout = config["action_timeout"];
            #endregion

            #region Get command line configuration.
            if (args.Length == 6)
            {
                protocol = args[0];
                verbose_level = Convert.ToInt32(args[1]);
                key = args[2];
                iv = args[3];
                input = args[4];
                output = args[5];
            }
            #endregion

            byte[] Key = Encoding.UTF8.GetBytes(key);
            byte[] IV = Encoding.UTF8.GetBytes(iv);

            #region Establish connection to mainframe.
            Simple3270Api emu = null;
            try
            {
                emu = new Simple3270Api(cfg);
            }
            catch (Exception)
            {
                if (!isDebug)
                {
                    string msg = "Unable to connect to mainframe at " + server + ":" + port + "@ssl=" + useSsl.ToString();
                    string jsn = ("{'response':'EXCEPTION','message':'" + msg + "'}").ToJson();
                    Win32Comm.Set(jsn, output);
                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine(msg);
                    Console.ForegroundColor = ConsoleColor.DarkRed;
                    Console.WriteLine("Press enter to close...");
                    Console.ReadLine();
                    return;
                }
            }
            if (!isDebug)
            {
                string jsn = ("{'response':'SUCCESS','message':'Connection established!'}").ToJson();
                Win32Comm.Set(jsn, "Simple3270_" + output);
            }
            #endregion

            #region Run as a service for a Python client.
            if (!isDebug)
            {
                RunWin32Pipes(Key, IV, input, output, emu);
            }
            #endregion
            #region Otherwise run routines as a test in C#
            else
            {
                //string inputJs = ("[{'name':'Enterprise','x':1,'y':1,'l':20},{'name':'Url','x':46,'y':2,'l':28},{'name':'Ip','x':63,'y':1,'l':14},{'name':'MainFrame','x':14,'y':5,'l':20},{'name':'NextGen','x':28,'y':15,'l':19}]").ToJson();
                //string outputJs = ("[{'name':'Login','x':1,'y':24,'value':'TSO'}]").ToJson();
                //string keyJs = ("{'button':'Enter'}").ToJson();
                //string waitJs = ("{'name':'WaitFor','x':12,'y':1,'value':'ENTER USERID -'}").ToJson();

                //string resp1 = emu.ReadScreenText(inputJs);
                //string resp2 = emu.ReadScreenColors(inputJs);
                //string resp3 = emu.WriteScreenText(outputJs);
                //string resp4 = emu.PressKey(keyJs);
                //string resp5 = emu.WaitForText(waitJs);
            }
            #endregion
        }
        // TODO: We can test to see if we can do the communication via the local file system
        // for Linux and Mac OS X clients.
        /// <summary>
        /// Runs Simple3270 as a service for a Python client.
        /// </summary>
        /// <param name="key">The encryption key to use.</param>
        /// <param name="iv">The initialization vector to use.</param>
        /// <param name="input">The input channel to listen on.</param>
        /// <param name="output">The output channel to write to.</param>
        /// <param name="emu">The emulator object we use for mainfram operation.</param>
        private static void RunWin32Pipes(byte[] key, byte[] iv, string input, string output, Simple3270Api emu)
        {
            while (true)
            {
                try
                {
                    #region Listen for next request from the client.
                    string text = Win32Comm.Get("Simple3270_" + input).Trim();
                    dynamic obj = Serialize.ToDynamic(text);
                    string package = obj["package"];
                    string letter = Steganography.Decrypt(package, key, iv);
                    dynamic header = Serialize.ToDynamic(letter);
                    string method = header["method"];
                    dynamic message = header["content"];
                    string wr = Serialize.FromDynamic(message);
                    string reply = string.Empty;
                    #endregion

                    #region Run the corresponding method.
                    try
                    {
                        switch (method)
                        {
                            case "read_screen_text":
                                reply = emu.ReadScreenText(wr);
                                break;
                            case "read_screen_colors":
                                reply = emu.ReadScreenColors(wr);
                                break;
                            case "write_screen_text":
                                reply = emu.WriteScreenText(wr);
                                break;
                            case "press_key":
                                reply = emu.PressKey(wr);
                                break;
                            case "wait_for_text":
                                reply = emu.WaitForText(wr);
                                break;
                            case "dispose_and_shutdown":
                                if (wr == "{\"content\":\"close_session\"}")
                                {
                                    emu.Dispose();
                                    Console.Clear();
                                    return;
                                }
                                break;
                        }
                    }
                    catch (Exception e) 
                    { 
                        reply = ("'response':'EXCEPTION','message':'" + e.Message + "'}").ToJson(); 
                    }
                   #endregion

                #region Send the response back to the client.
                if (reply.Contains("\"length\""))
                    {   // Handles sending binary files.
                        Win32Comm.Set(reply, "Simple3270_" + output);
                    }
                    else
                    {   // Handles sending text data.
                        string resp = ("{'response':'SUCCESS','content':'" + Steganography.Encrypt(reply, key, iv) + "'}").ToJson();
                        Win32Comm.Set(resp, "Simple3270_" + output);
                    }
                }
                catch (Exception e)
                {   // Handles sending response if exception is thrown.
                    Win32Comm.Set("{'response':'EXCEPTION','content':'" + e.Message + "'}", "Simple3270_" + output);
                }
                #endregion
            }
        }
    }
    public static class Extensions
    {
        public static string ToJson(this string value, string replace = null)
        {
            string text = value.Replace("'", "\"");
            if (replace != null)
                text = text.Replace("%1", replace);
            return text;
        }
    }
}