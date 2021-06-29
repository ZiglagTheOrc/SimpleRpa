#region License
/* 
 *
 * Simple3270 - A simple implementation of the TN3270/TN3270E protocol for Python and C#
 *
 * Copyright (c) 2009-2021 Ziglag the Orc
 * Modifications (c) as per Git change history
 *
 * This Source Code Form is subject to the terms of the Mozilla
 * internal License, v. 2.0. If a copy of the MPL was not distributed
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
using System.Threading;
using System;
using Newtonsoft.Json;

namespace Simple3270
{
	/// <summary>
	/// Configuration struct for instantiating a new Simple3270Api
	/// </summary>
	public struct Simple3270Config
	{
		public string Server { get; set; }
		public int Port { get; set; }
		public string Lu { get; set; }
		public bool UseSsl { get; set; }
		public bool FastScreenMode { get; set; }
		public string TerminalType { get; set; }
		public bool Debug { get; set; }
		public int ActionTimeout { get; set; }
		public int ColorDepth { get; set; }
		public Simple3270Config(string server, int port, bool useSsl = true, string lu = null)
		{
			Server = server;
			Port = port;
			UseSsl = useSsl;
			Lu = lu;
			Debug = false;
			TerminalType = "IBM-3278-2-E";
			FastScreenMode = true;
			ActionTimeout = 1000;
			ColorDepth = 2;
		}
	}
	/// <summary>
	/// Simple3270Api class for connecting to 3270 mainframes.
	/// </summary>
	public class Simple3270Api : IDisposable
	{
		private int _MaxRow = 24;
		private int _MaxCol = 80;
		private int _ColorDepth;
		private bool _Verbose = true;
		private string _Screen;
		private int _ActionTimeOut;
		private TNEmulator _Emulator;
		private ConsoleColor[,] _ForeColors;
		/// <summary>
		/// Constructs a new instance of the Simple3270Api class.
		/// </summary>
		/// <param name="config">The configuration object to use.</param>
		public Simple3270Api(Simple3270Config config)
		{
			_Emulator = new TNEmulator();
			// emulator.Audit = this;
			_ColorDepth = config.ColorDepth;
			_ActionTimeOut = config.ActionTimeout;
			_Emulator.Debug = config.Debug;
			_Emulator.Config.TermType = config.TerminalType;
			_Emulator.Config.FastScreenMode = config.FastScreenMode;
			_Emulator.Config.UseSSL = config.UseSsl;
			_Emulator.Connect(config.Server, config.Port, config.Lu);
			_ForeColors = new ConsoleColor[_MaxCol, _MaxRow];
			ClearForeColors();
			Write();
			ReadAllText();
		}
		/// <summary>
		/// Releases resources and disposes this object.
		/// </summary>
		public void Dispose()
        {
			_Emulator.Dispose();
			_ForeColors = null;
        }

		#region PUBLIC CAST TO CLASS METHODS
		/// <summary>
		/// Reads all the field values in the specified list and casts them to object of T.
		/// </summary>
		/// <typeparam name="T">The class to cast the data into.</typeparam>
		/// <param name="fields">The list of fields to gather.</param>
		/// <returns>T</returns>
		public T ReadScreenText<T>(List<SimpleInput> fields)
		{
			string json = JsonConvert.SerializeObject(fields);
			string output = ReadScreenText(json);
			T obj = JsonConvert.DeserializeObject<T>(output);
			return obj;
		}
		/// <summary>
		/// Reads the forecolors for each field in the specified list.
		/// </summary>
		/// <typeparam name="T">The class to cast the data into.</typeparam>
		/// <param name="fields">The list of fields to get the colors of.</param>
		/// <returns>T</returns>
		public T ReadScreenColors<T>(List<SimpleInput> fields)
		{
			string json = JsonConvert.SerializeObject(fields);
			string output = ReadScreenColors(json);
			T obj = JsonConvert.DeserializeObject<T>(output);
			return obj;
		}
		#endregion

		#region PUBLIC DYNAMIC METHODS
		/// <summary>
		/// Reads the values for all fields in the specified list.
		/// </summary>
		/// <param name="fields">The list of fields to gather.</param>
		/// <returns>dynamic</returns>
		public dynamic ReadScreenText(List<SimpleInput> fields)
		{
			string output = iReadScreenText(fields);
			dynamic obj = JsonConvert.DeserializeObject(output);
			return obj;
		}
		/// <summary>
		/// Reads the forecorlors for all fields in the specified list.
		/// </summary>
		/// <param name="fields">The list of fields to get the color of.</param>
		/// <returns>dynamic</returns>
		public dynamic ReadScreenColors(List<SimpleInput> fields)
		{
			string output = iReadScreenColors(fields);
			dynamic obj = JsonConvert.DeserializeObject(output);
			return obj;
		}
		/// <summary>
		/// Writes all field values in the specified list to the mainframe screen.
		/// </summary>
		/// <param name="fields">The list of fields to gather.</param>
		/// <returns>dynamic</returns>
		public bool WriteScreenText(List<SimpleOutput> fields)
		{
			string output = iWriteScreenText(fields);
			bool value = output == "{\"response\":\"COMPLETE\"}" ? true : false;
			return value;
		}
		/// <summary>
		/// Presses the specified key.
		/// </summary>
		/// <param name="fields">The list of fields to gather.</param>
		/// <returns>bool</returns>
		public bool PressKey(TnKey key)
		{
			string text = _Screen;
			_Emulator.SendKey(true, key, 60);
			Console.Clear();
			Write();
			return true;
		}
		/// <summary>
		/// Wait for the specified text to appear at the specified location.
		/// </summary>
		/// <param name="fields">The list of fields to gather.</param>
		/// <param name="timeout">OPTIONAL The time out to use. (Default 10sec)</param>
		/// <returns>dynamic</returns>
		public bool WaitForText(SimpleOutput field, int timeout = 10000)
		{
			string output = iWaitForText(field, timeout);
			bool value = output == "{\"response\":\"COMPLETE\"}" ? true : false;
			return value;
		}
		#endregion

		#region PUBLIC JSON METHODS
		/// <summary>
		/// Reads all field values listed in the specified json map.
		/// </summary>
		/// <param name="json">The json field map to use.</param>
		/// <returns>json</returns>
		public string ReadScreenText(string json)
		{
			List<SimpleInput> fields = JsonConvert.DeserializeObject<List<SimpleInput>>(json);
			string output = iReadScreenText(fields);
			return output;
		}
		/// <summary>
		/// Reads all forecolors for all fields listed in the specified json map.
		/// </summary>
		/// <param name="json">The json field map to use.</param>
		/// <returns>json</returns>
		public string ReadScreenColors(string json)
		{
			List<SimpleInput> fields = JsonConvert.DeserializeObject<List<SimpleInput>>(json);
			string output = iReadScreenColors(fields);
			return output;
		}
		/// <summary>
		/// Writes all values in the specified json map.
		/// </summary>
		/// <param name="json">The json field map to use.</param>
		/// <returns>json</returns>
		public string WriteScreenText(string json)
		{
			List<SimpleOutput> fields = JsonConvert.DeserializeObject<List<SimpleOutput>>(json);
			iWriteScreenText(fields);
			return "{\"response\":\"COMPLETE\"}";
		}
		/// <summary>
		/// Presses the key specified in the json map.
		/// </summary>
		/// <param name="json">The json field map to use.</param>
		/// <returns>json</returns>
		public string PressKey(string json)
		{
            #region Perform key press.
            string text = _Screen;
			dynamic press = JsonConvert.DeserializeObject(json);
			string k = press["button"].ToString();
			TnKey key = (TnKey)Enum.Parse(typeof(TnKey), k);
			_Emulator.SendKey(true, key, 60);
			int tries = 0;
            #endregion

            #region Handles if mainframe is clocking or otherwise returns a blank screen.
            while (string.IsNullOrEmpty(_Screen.Trim()) || text == _Screen)
			{
				ReadAllText();
				Thread.Sleep(25);
				tries++;
				if (tries >= 400)
					throw new TimeoutException("The mainfrained did not respond with in 10 seconds of pressing key '" + k + "'.");
			}
			#endregion

			#region Redraw screen and return response.
			Console.Clear();
			Write();
			return "{\"response\":\"COMPLETE\"}";
            #endregion
        }
        /// <summary>
        /// Waits for the specified text in the jsom map to appear on the screen in the specified location.
        /// </summary>
        /// <param name="json">The json field map to use.</param>
        /// <param name="timeout">OPTIONAL The time out to use. (Default 10sec)</param>
        /// <returns></returns>
        public string WaitForText(string json, int timeout = 10000)
		{
			SimpleOutput field = JsonConvert.DeserializeObject<SimpleOutput>(json);
			string output = iWaitForText(field, timeout);
			return output;
		}
		#endregion

		#region PRIVATE METHODS
		private string iReadScreenText(List<SimpleInput> fields)
		{
			string output = "{";
			for (int i = 0; i < fields.Count; i++)
			{
				int x = fields[i].X;
				int y = fields[i].Y;
				ConsoleColor c = GetForeColor(x, y);
				string text = ReadField(fields[i]);
				string js = "\"" + fields[i].Name + "\":\"" + text + "\"";
				output += js + ",";
				WriteReadField(x, y, c, ConsoleColor.Black, text);
			}
			output = output.Substring(0, output.Length - 1) + "}";
			return output;
		}
		private string iReadScreenColors(List<SimpleInput> fields)
		{
			string output = "{";
			for (int i = 0; i < fields.Count; i++)
			{
				int x = fields[i].X;
				int y = fields[i].Y;
				ConsoleColor c = GetForeColor(x, y);
				string js = "\"" + fields[i].Name + "\":\"" + c.ToString() + "\"";
				output += js + ",";
			}
			output = output.Substring(0, output.Length - 1) + "}";
			return output;
		}
		private string iWriteScreenText(List<SimpleOutput> fields)
		{
			for (int i = 0; i < fields.Count; i++)
			{
				int x = fields[i].X;
				int y = fields[i].Y;
				_Emulator.SetCursor(x - 1, y - 1);
				_Emulator.SetText(fields[i].Value);
				WriteToField(x, y, ConsoleColor.Yellow, ConsoleColor.Black, fields[i].Value);
			}
			return "{\"response\":\"COMPLETE\"}";
		}
		private string iWaitForText(SimpleOutput field, int timeout)
		{
			if (field.Name != "WaitFor")
				throw new Exception("Element needs to be SimpleOutput struct with the name of 'WaitFor' to be valid.");

			DateTime end = DateTime.Now.AddMilliseconds(timeout);
			while (true)
			{
				if (DateTime.Now > end)
				{
					Write();
					return "{\"response\":\"TIMEOUT\"}";
				}
				string text = ReadField(new SimpleInput(field));
				if (field.Value == text)
					return "{\"response\":\"COMPLETE\"}";
				Thread.Sleep(100);
			}
		}

		private string ReadField(SimpleInput field)
		{
			string text = _Emulator.GetText(field.X - 1, field.Y - 1, field.L);
			return text.Trim();
		}
		public void Write()
		{
			if (_Verbose)
			{
				int retries = 0;
			retry:
				int r = Console.CursorTop;
				int c = Console.CursorLeft;
				try
				{
					// Get screen in the form of an array of rows.
					string[] rows = ReadScreenByRows();
					Console.Clear(); // Clear console before rewriting the screen.
					#region Go field by field and write each field on the screen with the assigned color.
					for (int i = 0; i < _Emulator.CurrentScreenXML.Fields.Length; i++)
					{
						if (_Emulator.CurrentScreenXML.Fields[i].Text != null)
						{
							int x = _Emulator.CurrentScreenXML.Fields[i].Location.left;
							int y = _Emulator.CurrentScreenXML.Fields[i].Location.top;
							int l = _Emulator.CurrentScreenXML.Fields[i].Location.length;
							Console.SetCursorPosition(x, y);
							ConsoleColor clr = GetFieldColor(i);
							Console.ForegroundColor = clr;
							SetForeColor(x, y, l, clr);
							Console.Write(_Emulator.CurrentScreenXML.Fields[i].Text);
							int d = _Emulator.CurrentScreenXML.Fields[i].Location.top;
							rows[d] = rows[d].Remove(x, l);
							rows[d] = rows[d].Insert(x, string.Empty.PadRight(l, ' '));
						}
					}
					#endregion

					#region Write any text to the screen that is present and not mapped.
					for (int y = 0; y < rows.Length; y++)
					{
						// Skip blank lines.
						if (string.IsNullOrEmpty(rows[y].Trim()))
						{
							continue;
						}
						else
						{
							string text = rows[y].Trim();
							int l = rows[y].IndexOf(text);
							Console.SetCursorPosition(l, y);
							Console.ForegroundColor = ConsoleColor.DarkGreen;
							Console.Write(text);
						}
					}
					#endregion
				}
				catch (Exception ex)
				{
					#region If we are stuck on a blank screen try to fix it by clearing it.
					if (string.IsNullOrEmpty(_Emulator.GetText(0, 0, (_MaxCol * _MaxRow)).Trim()))
					{
						Console.Clear();
						Thread.Sleep(_ActionTimeOut);
						goto retry;
					}
					#endregion

					#region Otherwise try to refresh the page up to 5 times.  If didnt work after 5x then skip redraw.
					retries++;
					if (retries >= 5)
						return;
					_Emulator.Refresh();
					goto retry;
					#endregion
				}
				Console.SetCursorPosition(c, r);
			}
		}
		private ConsoleColor GetFieldColor(int i)
		{
			if (_ColorDepth == 2)
			{
				if (_Emulator.CurrentScreenXML.Fields[i].Attributes.FieldType == "High" &&
					_Emulator.CurrentScreenXML.Fields[i].Attributes.Protected)
					return ConsoleColor.White;
				else if (_Emulator.CurrentScreenXML.Fields[i].Attributes.FieldType == "High")
					return ConsoleColor.Red;
				else if (_Emulator.CurrentScreenXML.Fields[i].Attributes.Protected)
					return ConsoleColor.Blue;
			}
			else if (_ColorDepth == 4)
			{
				if (_Emulator.CurrentScreenXML.Fields[i].Attributes.Foreground == null)
				{
					return ConsoleColor.Green;
				}
				switch (_Emulator.CurrentScreenXML.Fields[i].Attributes.Foreground.ToLower())
				{
					case "blue":
						return ConsoleColor.Blue;
					case "turquoise":
						return ConsoleColor.Cyan;
					case "deepBlue":
						return ConsoleColor.DarkBlue;
					case "paleTurquoise":
						return ConsoleColor.DarkCyan;
					case "paleGreen":
						return ConsoleColor.DarkGreen;
					case "purple":
						return ConsoleColor.DarkMagenta;
					case "orange":
						return ConsoleColor.DarkYellow;
					case "neutralWhite":
						return ConsoleColor.Gray;
					case "green":
						return ConsoleColor.Green;
					case "pink":
						return ConsoleColor.Magenta;
					case "red":
						return ConsoleColor.Red;
					case "white":
						return ConsoleColor.White;
					case "yellow":
						return ConsoleColor.Yellow;
					case "grey":
					case "black":
					default:
						return ConsoleColor.DarkGray;
				}
			}
			return ConsoleColor.Green;
		}
		private void ClearForeColors()
		{
			for (int x = 0; x < _MaxCol; x++)
			{
				for (int y = 0; y < _MaxRow; y++)
				{
					_ForeColors[x, y] = ConsoleColor.Green;
				}
			}
		}
		private ConsoleColor GetForeColor(int x, int y)
		{
			ConsoleColor clr = _ForeColors[x - 1, y - 1];
			return clr;
		}
		private void WriteReadField(int x, int y, ConsoleColor f, ConsoleColor b, string text)
		{
			Console.SetCursorPosition(x - 1, y - 1);
			Console.BackgroundColor = f;
			Console.ForegroundColor = b;
			Console.Write(text);
			Console.ForegroundColor = f;
			Console.BackgroundColor = b;
		}
		private void WriteToField(int x, int y, ConsoleColor f, ConsoleColor b, string text)
		{
			Console.SetCursorPosition(x - 1, y - 1);
			Console.BackgroundColor = b;
			Console.ForegroundColor = f;
			Console.Write(text);
		}
		private void SetForeColor(int x, int y, int l, ConsoleColor c)
		{
			int end = x + l;
			for (int z = x; z < end; z++)
				_ForeColors[z, y] = c;
		}
		private string ReadAllText()
		{
			int lng = _MaxRow * _MaxCol;
			_Screen = _Emulator.GetText(0, 0, lng);

			//if (_Screen.ContainsAny(_Abends))
			//	throw new IbmException("The mainframe session has abended.");

			return _Screen;
		}
		private string[] ReadScreenByRows()
		{
			string screen = _Emulator.CurrentScreenXML.Dump();
			string[] rows = screen.Replace("\r\n", "\n").Split('\n');

			string paddedScreen = string.Empty;
			for (int i = 0; i < 24; i++)
			{
				paddedScreen += rows[i].PadRight(80, ' ') + "\n";
			}

			paddedScreen = paddedScreen.Substring(0, paddedScreen.Length - 2);
			rows = paddedScreen.Split('\n');
			return rows;
		}
		#endregion
	}
	/// <summary>
	/// Struct for 3270 input operations.
	/// </summary>
	public struct SimpleInput
	{
		public string Name { get; set; }
		public int X { get; set; }
		public int Y { get; set; }
		public int L { get; set; }
		public SimpleInput(string name, int x, int y, int l)
		{
			Name = name;
			X = x;
			Y = y;
			L = l;
		}
		public SimpleInput(SimpleOutput field)
		{
			this.Name = field.Name;
			this.X = field.X;
			this.Y = field.Y;
			this.L = field.Value.Length;
		}
	}
	/// <summary>
	/// Struct for 3270 output operations.
	/// </summary>
	public struct SimpleOutput
	{
		public string Name { get; set; }
		public int X { get; set; }
		public int Y { get; set; }
		public string Value { get; set; }
	}
}