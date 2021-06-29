#region License
/* 
 *
 * Simple3270 - A simple implementation of the TN3270/TN3270E protocol for Python and C#
 *
 * Copyright (c) 2004-2020 Michael Warriner
 * Modifications (c) as per Git change history
 * Modifications (c) 2009-2021 Ziglag the Orc
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
namespace Simple3270.TN3270
{

	internal class Tables
	{
		public static readonly byte[] Ascii2Cg = new byte[]
		{
			/*00*/	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
			/*08*/	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
			/*10*/	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
			/*18*/	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
			/*20*/	0x10, 0x19, 0x13, 0x2c, 0x1a, 0x2e, 0x30, 0x12,
			/*28*/	0x0d, 0x0c, 0xbf, 0x35, 0x33, 0x31, 0x32, 0x14,
			/*30*/	0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27,
			/*38*/	0x28, 0x29, 0x34, 0xbe, 0x09, 0x11, 0x08, 0x18,
			/*40*/	0x2d, 0xa0, 0xa1, 0xa2, 0xa3, 0xa4, 0xa5, 0xa6,
			/*48*/	0xa7, 0xa8, 0xa9, 0xaa, 0xab, 0xac, 0xad, 0xae,
			/*50*/	0xaf, 0xb0, 0xb1, 0xb2, 0xb3, 0xb4, 0xb5, 0xb6,
			/*58*/	0xb7, 0xb8, 0xb9, 0x0a, 0x15, 0x0b, 0x3a, 0x2f,
			/*60*/	0x3d, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86,
			/*68*/	0x87, 0x88, 0x89, 0x8a, 0x8b, 0x8c, 0x8d, 0x8e,
			/*70*/	0x8f, 0x90, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96,
			/*78*/	0x97, 0x98, 0x99, 0x0f, 0x16, 0x0e, 0x3b, 0x00,
			/*80*/	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
			/*88*/	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
			/*90*/	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
			/*98*/	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
			/*a0*/	0x01, 0x6e, 0x1b, 0x1c, 0x1f, 0x1d, 0x17, 0x2b,
			/*a8*/	0x3c, 0xd0, 0x6a, 0x6c, 0x36, 0x07, 0xd1, 0x37,
			/*b0*/	0x38, 0xd6, 0x68, 0x69, 0x3e, 0x54, 0x1e, 0x39,
			/*b8*/	0x3f, 0x67, 0x6b, 0x6d, 0x4b, 0x4c, 0x4d, 0x6f,
			/*c0*/	0x60, 0x7a, 0x75, 0x65, 0x70, 0xbc, 0xba, 0xbd,
			/*c8*/	0x61, 0x7b, 0x76, 0x71, 0x62, 0x7c, 0x77, 0x72,
			/*d0*/	0xd7, 0x7f, 0x63, 0x7d, 0x78, 0x66, 0x73, 0x5b,
			/*d8*/	0xbb, 0x64, 0x7e, 0x79, 0x74, 0x48, 0xd9, 0x2a,
			/*e0*/	0x40, 0x5a, 0x55, 0x45, 0x50, 0x9c, 0x9a, 0x4f,
			/*e8*/	0x41, 0x4a, 0x56, 0x51, 0x42, 0x5c, 0x57, 0x52,
			/*f0*/	0xf7, 0x5f, 0x43, 0x5d, 0x58, 0x46, 0x53, 0x9d,
			/*f8*/	0x9b, 0x44, 0x5e, 0x59, 0x4e, 0x49, 0xf9, 0x47
		};


		public static readonly byte[] Cg2Ascii = new byte[]
		{
			/*00*/	0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0xad,
			/*08*/	0x3e, 0x3c, 0x5b, 0x5d, 0x29, 0x28, 0x7d, 0x7b,
			/*10*/	0x20, 0x3d, 0x27, 0x22, 0x2f, 0x5c, 0x7c, 0xa6,
			/*18*/	0x3f, 0x21, 0x24, 0xa2, 0xa3, 0xa5, 0xb6, 0xa4,
			/*20*/	0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37,
			/*28*/	0x38, 0x39, 0xdf, 0xa7, 0x23, 0x40, 0x25, 0x5f,
			/*30*/	0x26, 0x2d, 0x2e, 0x2c, 0x3a, 0x2b, 0xac, 0xaf,
			/*38*/	0xb0, 0xb7, 0x5e, 0x7e, 0xa8, 0x60, 0xb4, 0xb8,
			/*40*/	0xe0, 0xe8, 0xec, 0xf2, 0xf9, 0xe3, 0xf5, 0xff,
			/*48*/	0xdd, 0xfd, 0xe9, 0xbc, 0xbd, 0xbe, 0xfc, 0xe7,
			/*50*/	0xe4, 0xeb, 0xef, 0xf6, 0xb5, 0xe2, 0xea, 0xee,
			/*58*/	0xf4, 0xfb, 0xe1, 0xd7, 0xed, 0xf3, 0xfa, 0xf1,
			/*60*/	0xc0, 0xc8, 0xcc, 0xd2, 0xd9, 0xc3, 0xd5, 0xb9,
			/*68*/	0xb2, 0xb3, 0xaa, 0xba, 0xab, 0xbb, 0xa1, 0xbf,
			/*70*/	0xc4, 0xcb, 0xcf, 0xd6, 0xdc, 0xc2, 0xca, 0xce,
			/*78*/	0xd4, 0xdb, 0xc1, 0xc9, 0xcd, 0xd3, 0xda, 0xd1,
			/*80*/	0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68,
			/*88*/	0x69, 0x6a, 0x6b, 0x6c, 0x6d, 0x6e, 0x6f, 0x70,
			/*90*/	0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78,
			/*98*/	0x79, 0x7a, 0xe6, 0xf8, 0xe5, 0xf7, 0x3b, 0x2a,
			/*a0*/	0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48,
			/*a8*/	0x49, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e, 0x4f, 0x50,
			/*b0*/	0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58,
			/*b8*/	0x59, 0x5a, 0xc6, 0xd8, 0xc5, 0xc7, 0x3b, 0x2a,
			/*c0*/	0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
			/*c8*/	0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
			/*d0*/	0xa9, 0xae, 0x20, 0x20, 0x20, 0x20, 0xb1, 0xd0,
			/*d8*/	0x20, 0xde, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
			/*e0*/	0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
			/*e8*/	0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
			/*f0*/	0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0xf0,
			/*f8*/	0x20, 0xfe, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20
		};


		public static readonly byte[] Ebc2Cg = new byte[]
		{
			/*00*/	0x00, 0xdf, 0xdf, 0xdf, 0xdf, 0xdf, 0xdf, 0xdf,
			/*08*/	0xdf, 0xdf, 0xdf, 0xdf, 0x02, 0x03, 0xdf, 0xdf,
			/*10*/	0xdf, 0xdf, 0xdf, 0xdf, 0xdf, 0x04, 0xdf, 0xdf,
			/*18*/	0xdf, 0x05, 0xdf, 0xdf, 0x9f, 0xdf, 0x9e, 0xdf,
			/*20*/	0xdf, 0xdf, 0xdf, 0xdf, 0xdf, 0xdf, 0xdf, 0xdf,
			/*28*/	0xdf, 0xdf, 0xdf, 0xdf, 0xdf, 0xdf, 0xdf, 0xdf,
			/*30*/	0xdf, 0xdf, 0xdf, 0xdf, 0xdf, 0xdf, 0xdf, 0xdf,
			/*38*/	0xdf, 0xdf, 0xdf, 0xdf, 0xdf, 0xdf, 0xdf, 0xdf,
			/*40*/	0x10, 0x01, 0x55, 0x50, 0x40, 0x5a, 0x45, 0x9c,
			/*48*/	0x4f, 0x5f, 0x1b, 0x32, 0x09, 0x0d, 0x35, 0x16,
			/*50*/	0x30, 0x4a, 0x56, 0x51, 0x41, 0x5c, 0x57, 0x52,
			/*58*/	0x42, 0x2a, 0x19, 0x1a, 0xbf, 0x0c, 0xbe, 0x36,
			/*60*/	0x31, 0x14, 0x75, 0x70, 0x60, 0x7a, 0x65, 0xbc,
			/*68*/	0xbd, 0x7f, 0x17, 0x33, 0x2e, 0x2f, 0x08, 0x18,
			/*70*/	0x9b, 0x7b, 0x76, 0x71, 0x61, 0x7c, 0x77, 0x72,
			/*78*/	0x62, 0x3d, 0x34, 0x2c, 0x2d, 0x12, 0x11, 0x13,
			/*80*/	0xbb, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86,
			/*88*/	0x87, 0x88, 0x6c, 0x6d, 0xf7, 0x49, 0xf9, 0xd6,
			/*90*/	0x38, 0x89, 0x8a, 0x8b, 0x8c, 0x8d, 0x8e, 0x8f,
			/*98*/	0x90, 0x91, 0x6a, 0x6b, 0x9a, 0x3f, 0xba, 0x1f,
			/*a0*/	0x54, 0x3b, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97,
			/*a8*/	0x98, 0x99, 0x6e, 0x6f, 0xd7, 0x48, 0xd9, 0xd1,
			/*b0*/	0x3a, 0x1c, 0x1d, 0x39, 0xd0, 0x2b, 0x1e, 0x4b,
			/*b8*/	0x4c, 0x4d, 0x0a, 0x0b, 0x37, 0x3c, 0x3e, 0x5b,
			/*c0*/	0x0f, 0xa0, 0xa1, 0xa2, 0xa3, 0xa4, 0xa5, 0xa6,
			/*c8*/	0xa7, 0xa8, 0x07, 0x58, 0x53, 0x43, 0x5d, 0x46,
			/*d0*/	0x0e, 0xa9, 0xaa, 0xab, 0xac, 0xad, 0xae, 0xaf,
			/*d8*/	0xb0, 0xb1, 0x67, 0x59, 0x4e, 0x44, 0x5e, 0x47,
			/*e0*/	0x15, 0x9d, 0xb2, 0xb3, 0xb4, 0xb5, 0xb6, 0xb7,
			/*e8*/	0xb8, 0xb9, 0x68, 0x78, 0x73, 0x63, 0x7d, 0x66,
			/*f0*/	0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27,
			/*f8*/	0x28, 0x29, 0x69, 0x79, 0x74, 0x64, 0x7e, 0x06
		};

		public static readonly byte[] Ebc2Cg0 = Tables.Ebc2Cg;
		public static readonly byte[] Cg2Ebc = new byte[] 
		 {
			 /*00*/	0x00, 0x41, 0x0c, 0x0d, 0x15, 0x19, 0xff, 0xca,
			 /*08*/	0x6e, 0x4c, 0xba, 0xbb, 0x5d, 0x4d, 0xd0, 0xc0,
			 /*10*/	0x40, 0x7e, 0x7d, 0x7f, 0x61, 0xe0, 0x4f, 0x6a,
			 /*18*/	0x6f, 0x5a, 0x5b, 0x4a, 0xb1, 0xb2, 0xb6, 0x9f,
			 /*20*/	0xf0, 0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7,
			 /*28*/	0xf8, 0xf9, 0x59, 0xb5, 0x7b, 0x7c, 0x6c, 0x6d,
			 /*30*/	0x50, 0x60, 0x4b, 0x6b, 0x7a, 0x4e, 0x5f, 0xbc,
			 /*38*/	0x90, 0xb3, 0xb0, 0xa1, 0xbd, 0x79, 0xbe, 0x9d,
			 /*40*/	0x44, 0x54, 0x58, 0xcd, 0xdd, 0x46, 0xcf, 0xdf,
			 /*48*/	0xad, 0x8d, 0x51, 0xb7, 0xb8, 0xb9, 0xdc, 0x48,
			 /*50*/	0x43, 0x53, 0x57, 0xcc, 0xa0, 0x42, 0x52, 0x56,
			 /*58*/	0xcb, 0xdb, 0x45, 0xbf, 0x55, 0xce, 0xde, 0x49,
			 /*60*/	0x64, 0x74, 0x78, 0xed, 0xfd, 0x66, 0xef, 0xda,
			 /*68*/	0xea, 0xfa, 0x9a, 0x9b, 0x8a, 0x8b, 0xaa, 0xab,
			 /*70*/	0x63, 0x73, 0x77, 0xec, 0xfc, 0x62, 0x72, 0x76,
			 /*78*/	0xeb, 0xfb, 0x65, 0x71, 0x75, 0xee, 0xfe, 0x69,
			 /*80*/	0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88,
			 /*88*/	0x89, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97,
			 /*90*/	0x98, 0x99, 0xa2, 0xa3, 0xa4, 0xa5, 0xa6, 0xa7,
			 /*98*/	0xa8, 0xa9, 0x9c, 0x70, 0x47, 0xe1, 0x1e, 0x1c,
			 /*a0*/	0xc1, 0xc2, 0xc3, 0xc4, 0xc5, 0xc6, 0xc7, 0xc8,
			 /*a8*/	0xc9, 0xd1, 0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7,
			 /*b0*/	0xd8, 0xd9, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7,
			 /*b8*/	0xe8, 0xe9, 0x9e, 0x80, 0x67, 0x68, 0x5e, 0x5c,
			 /*c0*/	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
			 /*c8*/	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
			 /*d0*/	0xb4, 0xaf, 0x00, 0x00, 0x00, 0x00, 0x8f, 0xac,
			 /*d8*/	0x00, 0xae, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
			 /*e0*/	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
			 /*e8*/	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
			 /*f0*/	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x8c,
			 /*f8*/	0x00, 0x8e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
		 };


		public static readonly byte[] Cg2Ebc0 = Cg2Ebc;
		public static readonly byte[] Ebc2Ascii = new byte[]
		{
			/*00*/	0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
			/*08*/	0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
			/*10*/	0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
			/*18*/	0x20, 0x20, 0x20, 0x20, 0x2a, 0x20, 0x3b, 0x20,
			/*20*/	0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
			/*28*/	0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
			/*30*/	0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
			/*38*/	0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
			/*40*/	0x20, 0x20, 0xe2, 0xe4, 0xe0, 0xe1, 0xe3, 0xe5,
			/*48*/	0xe7, 0xf1, 0xa2, 0x2e, 0x3c, 0x28, 0x2b, 0x7c,
			/*50*/	0x26, 0xe9, 0xea, 0xeb, 0xe8, 0xed, 0xee, 0xef,
			/*58*/	0xec, 0xdf, 0x21, 0x24, 0x2a, 0x29, 0x3b, 0xac,
			/*60*/	0x2d, 0x2f, 0xc2, 0xc4, 0xc0, 0xc1, 0xc3, 0xc5,
			/*68*/	0xc7, 0xd1, 0xa6, 0x2c, 0x25, 0x5f, 0x3e, 0x3f,
			/*70*/	0xf8, 0xc9, 0xca, 0xcb, 0xc8, 0xcd, 0xce, 0xcf,
			/*78*/	0xcc, 0x60, 0x3a, 0x23, 0x40, 0x27, 0x3d, 0x22,
			/*80*/	0xd8, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67,
			/*88*/	0x68, 0x69, 0xab, 0xbb, 0xf0, 0xfd, 0xfe, 0xb1,
			/*90*/	0xb0, 0x6a, 0x6b, 0x6c, 0x6d, 0x6e, 0x6f, 0x70,
			/*98*/	0x71, 0x72, 0xaa, 0xba, 0xe6, 0xb8, 0xc6, 0xa4,
			/*a0*/	0xb5, 0x7e, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78,
			/*a8*/	0x79, 0x7a, 0xa1, 0xbf, 0xd0, 0xdd, 0xde, 0xae,
			/*b0*/	0x5e, 0xa3, 0xa5, 0xb7, 0xa9, 0xa7, 0xb6, 0xbc,
			/*b8*/	0xbd, 0xbe, 0x5b, 0x5d, 0xaf, 0xa8, 0xb4, 0xd7,
			/*c0*/	0x7b, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47,
			/*c8*/	0x48, 0x49, 0xad, 0xf4, 0xf6, 0xf2, 0xf3, 0xf5,
			/*d0*/	0x7d, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e, 0x4f, 0x50,
			/*d8*/	0x51, 0x52, 0xb9, 0xfb, 0xfc, 0xf9, 0xfa, 0xff,
			/*e0*/	0x5c, 0xf7, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58,
			/*e8*/	0x59, 0x5a, 0xb2, 0xd4, 0xd6, 0xd2, 0xd3, 0xd5,
			/*f0*/	0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37,
			/*f8*/	0x38, 0x39, 0xb3, 0xdb, 0xdc, 0xd9, 0xda, 0x20
		};


		public static readonly byte[] Ascii2Uc = new byte[]
		{
			/*00*/	0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
			/*08*/	0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
			/*10*/	0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
			/*18*/	0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
			/*20*/	0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27,
			/*28*/	0x28, 0x29, 0x2a, 0x2b, 0x2c, 0x2d, 0x2e, 0x2f,
			/*30*/	0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37,
			/*38*/	0x38, 0x39, 0x3a, 0x3b, 0x3c, 0x3d, 0x3e, 0x3f,
			/*40*/	0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47,
			/*48*/	0x48, 0x49, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e, 0x4f,
			/*50*/	0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57,
			/*58*/	0x58, 0x59, 0x5a, 0x5b, 0x5c, 0x5d, 0x5e, 0x5f,
			/*60*/	0x60, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47,
			/*68*/	0x48, 0x49, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e, 0x4f,
			/*70*/	0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57,
			/*78*/	0x58, 0x59, 0x5a, 0x7b, 0x7c, 0x7d, 0x7e, 0x7f,
			/*80*/	0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87,
			/*88*/	0x88, 0x89, 0x8a, 0x8b, 0x8c, 0x8d, 0x8e, 0x8f,
			/*90*/	0x90, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97,
			/*98*/	0x98, 0x99, 0x9a, 0x9b, 0x9c, 0x9d, 0x9e, 0x9f,
			/*a0*/	0xa0, 0xa1, 0xa2, 0xa3, 0xa4, 0xa5, 0xa6, 0xa7,
			/*a8*/	0xa8, 0xa9, 0xaa, 0xab, 0xac, 0xad, 0xae, 0xaf,
			/*b0*/	0xb0, 0xb1, 0xb2, 0xb3, 0xb4, 0xb5, 0xb6, 0xb7,
			/*b8*/	0xb8, 0xb9, 0xba, 0xbb, 0xbc, 0xbd, 0xbe, 0xbf,
			/*c0*/	0xc0, 0xc1, 0xc2, 0xc3, 0xc4, 0xc5, 0xc6, 0xc7,
			/*c8*/	0xc8, 0xc9, 0xca, 0xcb, 0xcc, 0xcd, 0xce, 0xcf,
			/*d0*/	0xd0, 0xd1, 0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7,
			/*d8*/	0xd8, 0xd9, 0xda, 0xdb, 0xdc, 0xdd, 0xde, 0xdf,
			/*e0*/	0xc0, 0xc1, 0xc2, 0xc3, 0xc4, 0xc5, 0xc6, 0xc7,
			/*e8*/	0xc8, 0xc9, 0xca, 0xcb, 0xcc, 0xcd, 0xce, 0xcf,
			/*f0*/	0xd0, 0xd1, 0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xf7,
			/*f8*/	0xd8, 0xd9, 0xda, 0xdb, 0xdc, 0xdd, 0xde, 0xff
		};


		// From Toy mainframe code
		// Translation stuff
		public static readonly byte[] A2E = new byte[] 
		{
			/*    0     1     2     3     4     5     6     7     8     9     a     b     c     d     e     f */
			/*0*/ 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
			/*1*/ 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1D, 0x1e, 0x1F,
			/*2*/ 0x40, 0x5A, 0x7F, 0x7B, 0x5B, 0x6C, 0x50, 0x7D, 0x4D, 0x5D, 0x5C, 0x4E, 0x6B, 0x60, 0x4B, 0x61,
			/*3*/ 0xF0, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0x7A, 0x5E, 0x4C, 0x7E, 0x6E, 0x6F,
			/*4*/ 0x7C, 0xC1, 0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8, 0xC9, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6,
			/*5*/ 0xD7, 0xD8, 0xD9, 0xE2, 0xE3, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8, 0xE9, 0xAD, 0xE0, 0xBD, 0x5F, 0x6D,
			/*6*/ 0x79, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96,
			/*7*/ 0x97, 0x98, 0x99, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7, 0xA8, 0xA9, 0xC0, 0x4F, 0xD0, 0xA1, 0x07,
			/*8*/ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
			/*9*/ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
			/*a*/ 0x41, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
			/*b*/ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
			/*c*/ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
			/*d*/ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
			/*e*/ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
			/*f*/ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF
		};

		public static readonly byte[] E2A = new byte[] 
		{                                     
			/*    0     1     2     3     4     5     6     7     8     9     a     b     c     d     e     f */
			/*0*/ 0x00, 0x01, 0x02, 0x03, 0xFF, 0x09, 0xFF, 0x7F, 0xFF, 0xFF, 0xFF, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
			/*1*/ 0x10, 0x11, 0x12, 0x13, 0xFF, 0xFF, 0x08, 0xFF, 0x18, 0x19, 0xFF, 0xFF, 0xFF, 0x1D, 0xFF, 0x1F,
			/*2*/ 0xFF, 0xFF, 0x1C, 0xFF, 0xFF, 0x0A, 0x17, 0x1B, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x05, 0x06, 0x07,
			/*3*/ 0xFF, 0xFF, 0x16, 0xFF, 0xFF, 0x1E, 0xFF, 0x04, 0xFF, 0xFF, 0xFF, 0xFF, 0x14, 0x15, 0xFF, 0x1A,
			/*4*/ 0x20, 0xA0, 0xE2, 0xE4, 0xE0, 0xE1, 0xE3, 0xE5, 0xE7, 0xF1, 0x5B, 0x2E, 0x3C, 0x28, 0x2B, 0x7C,
			/*5*/ 0x26, 0xE8, 0xEA, 0xEB, 0xE8, 0xED, 0xEE, 0xEF, 0xEC, 0xDF, 0x5D, 0x24, 0x2A, 0x29, 0x3B, 0x5E,
			/*6*/ 0x2D, 0x2F, 0xC2, 0xC4, 0xC0, 0xC1, 0xC3, 0xC5, 0xC7, 0xD1, 0x7C, 0x2C, 0x25, 0x5F, 0x3E, 0x3F,
			/*7*/ 0xF8, 0xC9, 0xCA, 0xCB, 0xC8, 0xCD, 0xCE, 0xCF, 0xCC, 0x60, 0x3A, 0x23, 0x40, 0x27, 0x3D, 0x22,
			/*8*/ 0xD8, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0xAB, 0xBB, 0xF0, 0xFF, 0xFE, 0xB1,
			/*9*/ 0xB0, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E, 0x6F, 0x70, 0x71, 0x72, 0xAA, 0xBA, 0xE6, 0xB8, 0xC6, 0xA4,
			/*a*/ 0xB5, 0x7E, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0xA1, 0xBF, 0xD0, 0x5B, 0xDE, 0xAE,
			/*b*/ 0xA2, 0xA3, 0xA5, 0x20, 0x20, 0xA7, 0xB6, 0xBC, 0xBD, 0xBE, 0xAC, 0x7C, 0xAF, 0x5D, 0xB4, 0xFF,
			/*c*/ 0x7B, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0xAD, 0xF4, 0xF6, 0xF2, 0xF3, 0xF5,
			/*d*/ 0x7D, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E, 0x4F, 0x50, 0x51, 0x52, 0x31, 0xFB, 0xFC, 0xF9, 0xFA, 0xFF,
			/*e*/ 0x5C, 0x20, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0xB2, 0xD4, 0xD6, 0xD2, 0xD3, 0xD5,
			/*f*/ 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0xB3, 0xDB, 0xDC, 0xD9, 0xDA, 0xA0
		};

	}
}
