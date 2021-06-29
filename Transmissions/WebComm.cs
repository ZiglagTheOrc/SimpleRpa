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
using System.Text;
using RestSharp;

namespace Transmissions
{
    /// <summary>
    /// Used to facilitate cross platform communications. (Default for Linux and Mac OS X)
    /// </summary>
    public class WebComm
    {
        string _Server;
        int _Port;
        private byte[] _Key;
        private byte[] _IV;
        /// <summary>
        /// WebComm class constructor.
        /// </summary>
        /// <param name="key">The encryption key to use.</param>
        /// <param name="iv">The encryption initialization vector.</param>
        public WebComm(string key, string iv, string server, int port)
        {
            _Key = Encoding.UTF8.GetBytes(key);
            _IV = Encoding.UTF8.GetBytes(iv);
            _Server = server;
            _Port = port;
        }
        /// <summary>
        /// Used by the client to query the server.
        /// </summary>
        /// <param name="json">The request to make.</param>
        /// <param name="server">The IP address to connect to.</param>
        /// <param name="port">The port to connect on.</param>
        /// <returns></returns>
        public dynamic Query(string json)
        {
            RestClient client;
            try { client = new RestClient("http://" + _Server + ":" + _Port); }
            catch (UriFormatException)
            {
                string connInfo = "http://" + _Server + ":" + _Port;
                throw new UriFormatException("Failed to connect to to SimpleRPA service at '" + connInfo + "'");
            }
            string pkg = Steganography.Package(json, _Key, _IV);
            RestRequest request = new RestRequest("request_receiver", Method.POST);
            request.AddParameter("application/json; charset=utf-8", pkg, ParameterType.RequestBody);
            request.RequestFormat = DataFormat.Json;
            IRestResponse response = client.Execute(request);
            if (string.IsNullOrEmpty(response.Content))
                throw new Exception("Empty response recieved.  Is SimpleRPA Python service still running?");
            dynamic resp = Serialize.ToDynamic(response.Content);
            if (json == "{\"method\":\"shut_down\"}")  // No response required if service is shutting down.
                return Serialize.ToDynamic(("{'response':'SUCCESS','content':''}").Replace("'", "\""));
            if (resp["response"] == "EXCEPTION")
                throw new Exception(resp["content"].ToString());
            string encrypted = resp["content"].ToString();
            string content = Steganography.Decrypt(encrypted, _Key, _IV);
            dynamic jsn = Serialize.ToDynamic(content);
            return jsn;
        }
        /// <summary>
        /// Used by the client to query the server.
        /// </summary>
        /// <param name="json">The request to make.</param>
        /// <returns>byte[]</returns>
        public byte[] QueryToBytes(string json)
        {
            RestClient client;
            try { client = new RestClient("http://" + _Server + ":" + _Port); }
            catch (UriFormatException)
            {
                string connInfo = "http://" + _Server + ":" + _Port;
                throw new UriFormatException("Failed to connect to to SimpleRPA service at '" + connInfo + "'");
            }
            string pkg = Steganography.Package(json, _Key, _IV);
            RestRequest request = new RestRequest("request_receiver", Method.POST);
            request.AddParameter("application/json; charset=utf-8", pkg, ParameterType.RequestBody);
            request.RequestFormat = DataFormat.Json;
            IRestResponse response = client.Execute(request);
            dynamic resp = Serialize.ToDynamic(response.Content);
            return Common.ProcessBytePackage(resp, _Key, _IV);
        }
    }
}