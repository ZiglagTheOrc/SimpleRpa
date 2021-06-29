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
using System.Data;
using System.Diagnostics;
using System.IO;
using System.Text;
using Transmissions;

/// <summary>
/// The class used to configure the server with.
/// </summary>
namespace SimpleRPA
{
    /// <summary>
    /// List of communications protocols.
    /// </summary>
    public enum Protocols
    {
        Unspecified,
        Win32Pipe,
        WebService
    }
    /// <summary>
    /// This class is used to set configuration settings for the SimpleRPA service.
    /// This class is static because all core SimpleRPA functions (Mouse, Keyboard, Screen) are inherently singular.
    /// </summary>
    public static class Config
    {
        private static string _Key = null;
        private static string _IV = null;
        private static string _ClientToServer = null;
        private static string _ServerToClient = null;
        private static int _Verbose = -1;
        private static Protocols _Type = Protocols.Unspecified;
        private static Process _Service;
        private static string _Server;
        private static int _Port = -1;
        private static bool _UseWidgets = false;
        private static decimal _DefaultDelay = -1;
        /// <summary>
        /// The encryption key to use.  This property has write once read only after access.
        /// </summary>
        /// <exception cref="ReadOnlyException">Is thrown if you try to overwrite the existing value.</exception>
        public static byte[] KeyB
        {
            get
            {
                return Encoding.UTF8.GetBytes(_Key);
            }
        }
        public static byte[] IvB
        {
            get
            {
                return Encoding.UTF8.GetBytes(_IV);
            }
        }
        public static string Key
        {
            get
            {
                return _Key;
            }
            set
            {
                if (_Key == null)
                    _Key = value;
                else
                    throw new ReadOnlyException("The value of Key is read only once it has been set.");
            }
        }
        /// <summary>
        /// The initialization vector to use.  This property has write once read only after access.
        /// </summary>
        /// <exception cref="ReadOnlyException">Is thrown if you try to overwrite the existing value.</exception>
        public static string IV
        {
            get
            {
                return _IV;
            }
            set
            {
                if (_IV == null)
                    _IV = value;
                else
                    throw new ReadOnlyException("The value of IV is read only once it has been set.");
            }
        }
        /// <summary>
        /// The client to server channel to write to.
        /// </summary>
        /// <exception cref="ReadOnlyException">Is thrown if you try to overwrite the existing value.</exception>
        public static string ClientToServer
        {
            get
            {
                return _ClientToServer;
            }
            set
            {
                if (_ClientToServer == null)
                    _ClientToServer = value;
                else
                    throw new ReadOnlyException("The value of ClientToServer is read only once it has been set.");
            }
        }
        /// <summary>
        /// The server to client channel to read from.
        /// </summary>
        /// <exception cref="ReadOnlyException">Is thrown if you try to overwrite the existing value.</exception>
        public static string ServerToClient
        {
            get
            {
                return _ServerToClient;
            }
            set
            {
                if (_ServerToClient == null)
                    _ServerToClient = value;
                else
                    throw new ReadOnlyException("The value of ServerToClient is read only once it has been set.");
            }
        }
        /// <summary>
        /// Sets the level of verbosity for this service session.
        /// 0 = Print noting at all.
        /// 1 = Print basic level of information.
        /// 2 = Print advanced level of information.
        /// </summary>
        /// <exception cref="ReadOnlyException">Is thrown if you try to overwrite the existing value.</exception>
        public static int Verbose
        {
            get
            {
                return _Verbose;
            }
            set
            {
                if (_Verbose == -1)
                    _Verbose = value;
                else
                    throw new ReadOnlyException("The value of Verbose is read only once it has been set.");
            }
        }
        /// <summary>
        /// Sets the communication protocol to use.
        /// </summary>
        /// <exception cref="ReadOnlyException">Is thrown if you try to overwrite the existing value.</exception>
        public static Protocols ServerProtocol
        {
            get
            {
                return _Type;
            }
            set
            {
                if (_Type == Protocols.Unspecified)
                    _Type = value;
                else
                    throw new ReadOnlyException("The value of ServerProtocol is read only once it has been set.");
            }
        }
        /// <summary>
        /// The server to connect to. (Webservices)
        /// </summary>
        public static string Server 
        {
            get
            {
                return _Server;
            }
            set
            {
                if (_Server.IsNullOrEmpty())
                    _Server = value;
                else
                    throw new ReadOnlyException("The value of ServerProtocol is read only once it has been set.");
            }
        }
        /// <summary>
        /// The port to conect on. (Webservices)
        /// </summary>
        public static int Port
        {
            get
            {
                return _Port;
            }
            set
            {
                if (_Port == 0)
                    _Port = value;
                else
                    throw new ReadOnlyException("The value of ServerProtocol is read only once it has been set.");
            }
        }
        /// <summary>
        /// If true show widgest on items the RPA is looking at.
        /// </summary>
        public static bool UseWidgits
        {
            get
            {
                return _UseWidgets;
            }
        }
        /// <summary>
        /// The default delay (in seconds) to use.
        /// </summary>
        public static decimal DefaultDelay
        {
            get
            {
                return _DefaultDelay;
            }
        }
        /// <summary>
        /// Launches the SimpleRPA Python service.
        /// </summary>
        public static void StartService(Protocols protocolType)
        {
            #region Read the config.json file.
            string json = string.Empty;
            if (File.Exists("config.json"))
                json = File.ReadAllText("SimpleRpa.json");  // Production Location
            else
                json = File.ReadAllText("..\\..\\..\\..\\SimpleRPA\\SimpleRpa.json");  // Debug Location
            dynamic config = Serialize.ToDynamic(json);
            #endregion

            #region Load PRODUCTION serice config and generate service communication info for this session.
            _Type = protocolType;
            int verbose = config["verbose_level"];
            string key = Convert.ToBase64String(GetByteArray(32)); // Random encryption key.
            string iv = Convert.ToBase64String(GetByteArray(16));  // Random initialization vector.
            string opt1 = string.Empty;
            string opt2 = string.Empty;
            switch (_Type)
            {
                case Protocols.Win32Pipe:
                    opt1 = new Random().Next(65535, 65535).ToString("x") + new Random().Next(65535, 65535).ToString("x");  // Generate random client to server channel.
                    opt2 = new Random().Next(65535, 65535).ToString("x") + new Random().Next(65535, 65535).ToString("x");  // Generate random server to client channel.
                    break;
                case Protocols.WebService:
                    opt1 = config["server"];
                    if (opt1.IsNullOrEmpty())
                        opt1 = "localhost";
                    int minPort = config["minimum_port"];
                    int maxPort = config["minimum_port"];
                    opt2 = new Random().Next(minPort, maxPort).ToString();
                    break;
            }
            #endregion

            #region If we are DEBUGING then load DEBUG config values here.
            bool isDebug = false;
            try
            {
                key = config["key"];
                Console.ForegroundColor = ConsoleColor.Red;
                Console.Write("DANGER!!! ");
                Console.ForegroundColor = ConsoleColor.DarkRed;
                Console.WriteLine("Config.json contains a manually entered debug encryption key value 'key'. This configuration exists only for dev/debug and represents a significant security risk for a production environment.  Delete the 'key' entry from config.json before deploying to production.");
                isDebug = true;
            }
            catch { /* Do Nothing */ }

            try
            {
                iv = config["iv"];
                Console.ForegroundColor = ConsoleColor.Red;
                Console.Write("DANGER!!! ");
                Console.ForegroundColor = ConsoleColor.DarkRed;
                Console.WriteLine("Config.json contains a manually entered debug encryption key value 'iv'. This configuration exists only for dev/debug and represents a significant security risk for a production environment.  Delete the 'iv' entry from config.json before deploying to production.");
                isDebug = true;
            }
            catch { /* Do Nothing */ }

            if (protocolType == Protocols.WebService)
            {
                try
                {
                    opt1 = config["server"];
                    opt2 = config["minimum_port"];
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.Write("DANGER!!! ");
                    Console.ForegroundColor = ConsoleColor.DarkRed;
                    Console.WriteLine("Config.json contains a manually entered debug encryption key value 'server'. This configuration exists only for dev/debug and represents a significant security risk for a production environment.  Delete the 'server' entry from config.json before deploying to production.");
                    isDebug = true;
                }
                catch { /* Do Nothing */ }
                _Server = opt1;
                _Port = Convert.ToInt32(opt2);
            }

            if (protocolType == Protocols.Win32Pipe)
            {
                try
                {
                    opt1 = config["client_to_server"];
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.Write("DANGER!!! ");
                    Console.ForegroundColor = ConsoleColor.DarkRed;
                    Console.WriteLine("Config.json contains a manually entered debug encryption key value 'client_to_server'. This configuration exists only for dev/debug and represents a significant security risk for a production environment.  Delete the 'client_to_server' entry from config.json before deploying to production.");
                    isDebug = true;
                }
                catch { /* Do Nothing */ }
                try
                {
                    opt2 = config["server_to_client"];
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.Write("DANGER!!! ");
                    Console.ForegroundColor = ConsoleColor.DarkRed;
                    Console.WriteLine("Config.json contains a manually entered debug encryption key value 'server_to_client'. This configuration exists only for dev/debug and represents a significant security risk for a production environment.  Delete the 'server_to_client' entry from config.json before deploying to production.");
                    isDebug = true;
                }
                catch { /* Do Nothing */ }
                _ClientToServer = opt1;
                _ServerToClient = opt2;
            }
            _Key = key;
            _IV = iv;
            #endregion

            #region Launch SimpelRPA Python service.
            if (!isDebug)
            {
                ProcessStartInfo psi = new ProcessStartInfo();
                if (verbose == 0)
                    psi.WindowStyle = ProcessWindowStyle.Hidden;
                psi.FileName = "SimpleRPA.exe";
                psi.Arguments = _Type + " " + verbose + " " + key + " " + iv + " " + opt1 + " " + opt2;
                _Service = Process.Start(psi);
            }
            #endregion
        }
        /// <summary>
        /// Shuts down the SimpleRPA Python service.
        /// </summary>
        public static void StopService()
        {
            string json = "{'method':'shut_down'}".Replace("'","\"");
            if (_Type == Protocols.Win32Pipe)
            {
                string pkg = Steganography.Package(json, KeyB, IvB);
                Win32Comm.Set(pkg, "SimpleRpa_" + Config.ClientToServer);
            }
            else if (_Type == Protocols.WebService)
                ;
            //if (!_Service.HasExited)
            //    _Service.Kill();
        }
        /// <summary>
        /// Retuns an instance of the specified communicaton protocol.
        /// </summary>
        /// <returns>dynamic</returns>
        public static dynamic GetServiceConnection()
        {
            switch (ServerProtocol)
            {
                case Protocols.Win32Pipe:
                    return new Win32Comm(_Key, _IV, "SimpleRpa_" + _ServerToClient, "SimpleRpa_" + _ClientToServer);
                case Protocols.WebService:
                    return new WebComm(_Key, _IV, _Server, _Port);
                default:
                    throw new Exception("Communications protocol has not been set in Config.ServerProtocol.");
            }
        }
        private static byte[] GetByteArray(int size)
        {
            Random rnd = new Random();
            byte[] bytes = new byte[size];
            rnd.NextBytes(bytes);
            return bytes;
        }
    }

    /// <summary>
    /// Custom exception used to capture any exceptions that are being thrown from the Python service.
    /// </summary>
    public class PythonException : Exception
    {
        public PythonException(string message) : base(message)
        {
            
        }
    }
}