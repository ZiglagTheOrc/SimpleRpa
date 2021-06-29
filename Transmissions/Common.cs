using System;
using System.Collections.Generic;
using System.Text;

namespace Transmissions
{
    internal static class Common
    {
        public static byte[] ProcessBytePackage(dynamic response, byte[] key, byte[] iv)
        {
            if (response["response"] == "EXCEPTION")
                throw new Exception(response["content"].ToString());
            string encrypted = response["content"];
            string elng = response["length"];
            byte[] blng = Convert.FromBase64String(elng);
            string slng = Encoding.UTF8.GetString(blng);
            int lng = Convert.ToInt32(slng);
            byte[] content = Steganography.DecryptToBytes(encrypted, key, iv, lng);
            int diff = content.Length - lng;
            byte[] array = new byte[lng];
            Buffer.BlockCopy(content, diff, array, 0, lng);
            return content;
        }
    }
}
