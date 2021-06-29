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
using Newtonsoft.Json;

namespace Transmissions
{
    /// <summary>
    /// Used to serialize classes to json and vice cersa.
    /// </summary>
    /// <typeparam name="T">The class to serialize/deserialize.</typeparam>
    public static class Serialization<T>
    {
        /// <summary>
        /// Serializes an object of T to a json string.
        /// </summary>
        /// <param name="obj">The object to serialize.</param>
        /// <returns>json</returns>
        public static string Serialize(T obj)
        {
            string json = JsonConvert.SerializeObject(obj);
            return json;
        }
        /// <summary>
        /// Deserializes a json string to the specified class.
        /// </summary>
        /// <param name="json">The json string to deserialize.</param>
        /// <returns>T</returns>
        public static T Deserialize(string json)
        {
            T obj = JsonConvert.DeserializeObject<T>(json);
            return obj;
        }
    }
    /// <summary>
    /// Used to serialize/deserialize json to and from dynamic objects.
    /// </summary>
    public static class Serialize
    {
        /// <summary>
        /// Take a json string and deserializes it to a dynamic object.
        /// </summary>
        /// <param name="json">The json string to deserialze.</param>
        /// <returns>dynamic</returns>
        public static dynamic ToDynamic(string json)
        {
            dynamic obj = JsonConvert.DeserializeObject(json);
            return obj;
        }
        /// <summary>
        /// Takes a dynamic object and serialize it to a json string.
        /// </summary>
        /// <param name="obj">The dynamic object to serialize.</param>
        /// <returns>json</returns>
        public static string FromDynamic(dynamic obj)
        {
            string json = JsonConvert.SerializeObject(obj);
            return json;
        }
    }
}