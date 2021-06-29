using System;
using System.Collections.Generic;
using System.Text;

namespace Transmissions
{
    public static class Extensions
    {
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
    }
}
