# region License
"""
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
"""
# endregion
import time

import cv2
import numpy as np
import _Widget
from _Platform_Convergence import Config
from PIL import ImageGrab
from tkinter import *


def get_pixel_color(pt, use_widget=None, duration=0):
    """
    Returns the pixel color of the specified coordinate.
    :param pt: The point to look at.
    :param use_widget: If true displays the field highlighter widget.
    :param duration: The amount of time to display the widget for.
    :return: Color
    """
    image = ImageGrab.grab(bbox=(pt[0], pt[1], pt[0] + 1, pt[1] + 1))
    pixel = image.getpixel((0, 0))
    if use_widget is None:
        use_widget = Config.use_widgets_by_default
        duration = Config.default_widget_duration
    if use_widget:
        _Widget.Widget._show_widget_pt(pt, duration)
    return pixel


def get_known_color(pt, use_widget=None, duration=0):
    """
    Returns the nearest known color of the specified coordinate.
    :param pt: The point to look at.
    :param use_widget: If true displays the field highlighter widget.
    :param duration: The amount of time to display the widget for.
    :return: Color
    """
    known_colors = KnownColors.get_known_colors()
    if use_widget is None:
        use_widget = Config.use_widgets_by_default
        duration = Config.default_widget_duration
    if use_widget:
        _Widget.Widget._show_widget_pt(pt, duration)
    return _get_color(pt, known_colors)


def get_console_color(pt, use_widget=None, duration=0):
    """
    Returns the nearest console color of the specified coordinate.
    :param pt: The point to look at.
    :param use_widget: If true displays the field highlighter widget.
    :param duration: The amount of time to display the widget for.
    :return: Color
    """
    console_colors = KnownColors.get_console_colors()
    if use_widget is None:
        use_widget = Config.use_widgets_by_default
        duration = Config.default_widget_duration
    if use_widget:
        _Widget.Widget._show_widget_pt(pt, duration)
    return _get_color(pt, console_colors)


def _get_color(pt, color_list):
    """
    Gets the color at the specified point on the screen.
    :param color_list: The list of known colors to find the closest match to.
    :return: Color
    """
    lng = len(color_list)

    p = get_pixel_color(pt)

    clr = -1
    delta = 256
    m0 = 256
    m1 = 256
    m2 = 256
    c0 = 256
    c1 = 256
    c2 = 256
    # region Find closest match.
    for i in range(0, lng):
        c = color_list[i]
        d0 = abs(c.r - p[0])
        d1 = abs(c.g - p[1])
        d2 = abs(c.b - p[2])

        d = (d0 + d1 + d2) / 3
        if d < delta:
            delta = d
            clr = i
            c0 = d0
            c1 = d1
            c2 = d2
        elif d == delta:
            if (c0 < m0 and (c1 < m1 or c2 < m2)) or (c1 < m1 and c2 < m2):
                delta = d
                clr = i
                c0 = d0
                c1 = d1
                c2 = d2
    # endregion
    return color_list[clr]
    # endregion


def capture(rct, use_widget=None, duration=0):
    """
    Captures the area of the specified rectangle.
    :param rct: Tuple area rectangle to capture off the screen.
    :param use_widget: If true displays the field highlighter widget.
    :param duration: The amount of time to display the widget for.
    :return: image
    """
    image = ImageGrab.grab(bbox=(rct[0], rct[1], rct[2], rct[3]), all_screens=True)
    if use_widget is None:
        use_widget = Config.use_widgets_by_default
        duration = Config.default_widget_duration
    if use_widget:
        _Widget.Widget._show_widget_rect(rct, duration)
    return image


def capture_to_file(rct, file, use_widget=None, duration=0):
    """
    Captures the area of the screen and save it to the specified file.
    :param rct: Tuple area rectangle to capture off the screen.
    :param file: The name of the file to save the image to.
    :param use_widget: If true displays the field highlighter widget.
    :param duration: The amount of time to display the widget for.
    :return: void
    """
    image = capture(rct)
    if use_widget is None:
        use_widget = Config.use_widgets_by_default
        duration = Config.default_widget_duration
    if use_widget:
        _Widget.Widget._show_widget_rect(rct, duration)
    image.save(file)
    image.close()
    return


def find_image(file, threshold=0.9, use_widget=None, duration=0):
    """
    Searches the screen to locate image matches of the specified image file.
    :param file: The name of the file to load reference image from.
    :param threshold: The matching threshold to use when searching.
    :return: tuple(x,y,w,h)[]
    """
    if file is None or file == '':
        raise FileNotFoundError("The paramater 'file' must be populated.")

    # Load the image file to look for.
    img = cv2.imread(file)

    # region Get the screen width and height.
    tkr = Tk()
    width = tkr.winfo_screenwidth()
    height = tkr.winfo_screenheight()
    # endregion

    # Capture the screen.
    screen = np.array(ImageGrab.grab(bbox=(0, 0, width, height), all_screens=True))

    # region Seach for image file on screen and return found locations.
    haystack = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    needle = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    w, h = needle.shape[::-1]
    res = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)

    loc = np.where(res >= threshold)

    if use_widget is None:
        use_widget = Config.use_widgets_by_default
        duration = Config.default_widget_duration
    lst = list()
    for i in range(len(loc[0])):
        rect = (loc[1][i], loc[0][i], w, h)
        lst.append(rect)
        if use_widget:
            _Widget.Widget._show_widget_rect(rect, duration)

    return lst


class Color:
    """
    Class to manage screen colors.
    """
    r = 0
    g = 0
    b = 0
    name = ''

    def __init__(self, r, g, b, name=''):
        """
        Initializes a new instance of Color class.
        :param r: The red channel value.
        :param g: The green channel value.
        :param b: The blue channel value.
        :param name: If this is a known color the name of the known color will populate here.
        :return: tuple(x,y,w,h)[]
        """
        self.r = r
        self.g = g
        self.b = b
        self.name = name


class KnownColors:
    """
    An enumerate list of known colors.
    """
    ALICE_BLUE = Color(240, 248, 255, 'AliceBlue')
    ANTIQUE_WHITE = Color(250, 235, 215, 'AntiqueWhite')
    AQUA = Color(0, 255, 255, 'Aqua')
    AQUAMARINE = Color(127, 255, 212, 'Aquamarine')
    AZURE = Color(240, 255, 255, 'Azure')
    BEIGE = Color(245, 245, 220, 'Beige')
    BISQUE = Color(255, 228, 196, 'Bisque')
    BLACK = Color(0, 0, 0, 'Black')
    BLANCHED_ALMOND = Color(255, 235, 205, 'BlanchedAlmond')
    BLUE = Color(0, 0, 255, 'Blue')
    BLUE_VIOLET = Color(138, 43, 226, 'BlueViolet')
    BROWN = Color(165, 42, 42, 'Brown')
    BURLY_WOOD = Color(222, 184, 135, 'BurlyWood')
    CADET_BLUE = Color(95, 158, 160, 'CadetBlue')
    CHARTREUSE = Color(127, 255, 0, 'Chartreuse')
    CHOCOLATE = Color(210, 105, 30, 'Chocolate')
    CORAL = Color(255, 127, 80, 'Coral')
    CORN_FLOWER_BLUE = Color(100, 149, 237, 'CornflowerBlue')
    CORNSILK = Color(255, 248, 220, 'Cornsilk')
    CRIMSON = Color(220, 20, 60, 'Crimson')
    CYAN = Color(0, 255, 255, 'Cyan')
    DARK_BLUE = Color(0, 0, 139, 'DarkBlue')
    DARK_CYAN = Color(0, 139, 139, 'DarkCyan')
    DARK_GOLDENROD = Color(184, 134, 11, 'DarkGoldenrod')
    DARK_GRAY = Color(169, 169, 169, 'DarkGray')
    DARK_GREEN = Color(0, 100, 0, 'DarkGreen')
    DARK_KHAKI = Color(189, 183, 107, 'DarkKhaki')
    DARK_MAGENTA = Color(139, 0, 139, 'DarkMagenta')
    DARK_OLIVE_GREEN = Color(85, 107, 47, 'DarkOliveGreen')
    DARK_ORANGE = Color(255, 140, 0, 'DarkOrange')
    DARK_ORCHID = Color(153, 50, 204, 'DarkOrchid')
    DARK_RED = Color(139, 0, 0, 'DarkRed')
    DARK_SALMON = Color(233, 150, 122, 'DarkSalmon')
    DARK_SEA_GREEN = Color(143, 188, 139, 'DarkSeaGreen')
    DARK_SLATE_BLUE = Color(72, 61, 139, 'DarkSlateBlue')
    DARK_SLATE_GRAY = Color(47, 79, 79, 'DarkSlateGray')
    DARK_TURQUOISE = Color(0, 206, 209, 'DarkTurquoise')
    DARK_VIOLET = Color(148, 0, 211, 'DarkViolet')
    DEEP_PINK = Color(255, 20, 147, 'DeepPink')
    DEEP_SKY_BLUE = Color(0, 191, 255, 'DeepSkyBlue')
    DIM_GRAY = Color(105, 105, 105, 'DimGray')
    DODGER_BLUE = Color(30, 144, 255, 'DodgerBlue')
    FIRE_BRICK = Color(178, 34, 34, 'Firebrick')
    FLORAL_WHITE = Color(255, 250, 240, 'FloralWhite')
    FOREST_GREEN= Color(34, 139, 34, 'ForestGreen')
    FUCHSIA = Color(255, 0, 255, 'Fuchsia')
    GAINSBORO = Color(220, 220, 220, 'Gainsboro')
    GHOST_WHITE = Color(248, 248, 255, 'GhostWhite')
    GOLD = Color(255, 215, 0, 'Gold')
    GOLDENROD = Color(218, 165, 32, 'Goldenrod')
    GRAY = Color(128, 128, 128, 'Gray')
    GREEN = Color(0, 128, 0, 'Green')
    GREEN_YELLOW = Color(173, 255, 47, 'GreenYellow')
    HONEYDEW = Color(240, 255, 240, 'Honeydew')
    HOT_PINK = Color(255, 105, 180, 'HotPink')
    INDIAN_RED = Color(205, 92, 92, 'IndianRed')
    INDIGO = Color(75, 0, 130, 'Indigo')
    IVORY = Color(255, 255, 240, 'Ivory')
    KHAKI = Color(240, 230, 140, 'Khaki')
    LAVENDER = Color(230, 230, 250, 'Lavender')
    LAVENDER_BLUSH = Color(255, 240, 245, 'LavenderBlush')
    LAWN_GREEN = Color(124, 252, 0, 'LawnGreen')
    LEMON_CHIFFON = Color(255, 250, 205, 'LemonChiffon')
    LIGHT_BLUE = Color(173, 216, 230, 'LightBlue')
    LIGHT_CORAL = Color(240, 128, 128, 'LightCoral')
    LIGHT_CYAN = Color(224, 255, 255, 'LightCyan')
    LIGHT_GOLDENROD_YELLOW = Color(250, 250, 210, 'LightGoldenrodYellow')
    LIGHT_GRAY = Color(211, 211, 211, 'LightGray')
    LIGHT_GREEN = Color(144, 238, 144, 'LightGreen')
    LIGHT_PINK = Color(255, 182, 193, 'LightPink')
    LIGHT_SALMON = Color(255, 160, 122, 'LightSalmon')
    LIGHT_SEA_GREEN = Color(32, 178, 170, 'LightSeaGreen')
    LIGHT_SKY_BLUE = Color(135, 206, 250, 'LightSkyBlue')
    LIGHT_SLATE_GRAY = Color(119, 136, 153, 'LightSlateGray')
    LIGHT_STEEL_BLUE = Color(176, 196, 222, 'LightSteelBlue')
    LIGHT_YELLOW = Color(255, 255, 224, 'LightYellow')
    LIME = Color(0, 255, 0, 'Lime')
    LIME_GREEN = Color(50, 205, 50, 'LimeGreen')
    LINEN = Color(250, 240, 230, 'Linen')
    MAGENTA = Color(255, 0, 255, 'Magenta')
    MAROON = Color(128, 0, 0, 'Maroon')
    MEDIUM_AQUAMARINE = Color(102, 205, 170, 'MediumAquamarine')
    MEDIUM_BLUE = Color(0, 0, 205, 'MediumBlue')
    MEDIUM_ORCHID = Color(186, 85, 211, 'MediumOrchid')
    MEDIUM_PURPLE = Color(147, 112, 219, 'MediumPurple')
    MEDIUM_SEA_GREEN = Color(60, 179, 113, 'MediumSeaGreen')
    MEDIUM_SLATE_BLUE = Color(123, 104, 238, 'MediumSlateBlue')
    MEDIUM_SPRING_GREEN = Color(0, 250, 154, 'MediumSpringGreen')
    MEDIUM_TURQUOISE = Color(72, 209, 204, 'MediumTurquoise')
    MEDIUM_VIOLET_RED = Color(199, 21, 133, 'MediumVioletRed')
    MIDNIGHT_BLUE = Color(25, 25, 112, 'MidnightBlue')
    MINT_CREAM = Color(245, 255, 250, 'MintCream')
    MISTY_ROSE = Color(255, 228, 225, 'MistyRose')
    MOCCASIN = Color(255, 228, 181, 'Moccasin')
    NAVAJO_WHITE = Color(255, 222, 173, 'NavajoWhite')
    NAVY = Color(0, 0, 128, 'Navy')
    OLD_LACE = Color(253, 245, 230, 'OldLace')
    OLIVE = Color(128, 128, 0, 'Olive')
    OLIVE_DRAB = Color(107, 142, 35, 'OliveDrab')
    ORANGE = Color(255, 165, 0, 'Orange')
    ORANGE_RED = Color(255, 69, 0, 'OrangeRed')
    ORCHID = Color(218, 112, 214, 'Orchid')
    PALE_GOLDENROD = Color(238, 232, 170, 'PaleGoldenrod')
    PALE_GREEN = Color(152, 251, 152, 'PaleGreen')
    PALE_TURQUOISE = Color(175, 238, 238, 'PaleTurquoise')
    PALE_VIOLET_RED = Color(219, 112, 147, 'PaleVioletRed')
    PAPAYA_WHIP = Color(255, 239, 213, 'PapayaWhip')
    PEACH_PUFF = Color(255, 218, 185, 'PeachPuff')
    PERU = Color(205, 133, 63, 'Peru')
    PINK = Color(255, 192, 203, 'Pink')
    PLUM = Color(221, 160, 221, 'Plum')
    POWDER_BLUE = Color(176, 224, 230, 'PowderBlue')
    PURPLE = Color(128, 0, 128, 'Purple')
    RED = Color(255, 0, 0, 'Red')
    ROSY_BROWN = Color(188, 143, 143, 'RosyBrown')
    ROYAL_BLUE = Color(65, 105, 225, 'RoyalBlue')
    SADDLE_BROWN = Color(139, 69, 19, 'SaddleBrown')
    SALMON = Color(250, 128, 114, 'Salmon')
    SANDY_BROWN = Color(244, 164, 96, 'SandyBrown')
    SEA_GREEN = Color(46, 139, 87, 'SeaGreen')
    SEA_SHELL = Color(255, 245, 238, 'SeaShell')
    SIENNA = Color(160, 82, 45, 'Sienna')
    SILVER = Color(192, 192, 192, 'Silver')
    SKY_BLUE = Color(135, 206, 235, 'SkyBlue')
    SLATE_BLUE = Color(106, 90, 205, 'SlateBlue')
    SLATE_GRAY = Color(112, 128, 144, 'SlateGray')
    SNOW = Color(255, 250, 250, 'Snow')
    SPRING_GREEN = Color(0, 255, 127, 'SpringGreen')
    STEEL_BLUE = Color(70, 130, 180, 'SteelBlue')
    TAN = Color(210, 180, 140, 'Tan')
    TEAL = Color(0, 128, 128, 'Teal')
    THISTLE = Color(216, 191, 216, 'Thistle')
    TOMATO = Color(255, 99, 71, 'Tomato')
    TURQUOISE = Color(64, 224, 208, 'Turquoise')
    VIOLET = Color(238, 130, 238, 'Violet')
    WHEAT = Color(245, 222, 179, 'Wheat')
    WHITE = Color(255, 255, 255, 'White')
    WHITE_SMOKE = Color(245, 245, 245, 'WhiteSmoke')
    YELLOW = Color(255, 255, 0, 'Yellow')
    YELLOW_GREEN = Color(154, 205, 50, 'YellowGreen')

    @staticmethod
    def get_console_colors():
        """
        Returns a list of the 16 console colors.
        :return: Color[]
        """
        cc = list()
        cc.append(KnownColors.BLACK)
        cc.append(KnownColors.WHITE)
        cc.append(KnownColors.GRAY)
        cc.append(KnownColors.RED)
        cc.append(KnownColors.GREEN)
        cc.append(KnownColors.BLUE)
        cc.append(KnownColors.MAGENTA)
        cc.append(KnownColors.CYAN)
        cc.append(KnownColors.DARK_RED)
        cc.append(KnownColors.DARK_GREEN)
        cc.append(KnownColors.DARK_BLUE)
        cc.append(KnownColors.DARK_MAGENTA)
        cc.append(KnownColors.DARK_CYAN)
        cc.append(KnownColors.YELLOW)
        cc.append(KnownColors.ORANGE)
        cc.append(KnownColors.DARK_GRAY)
        return cc

    @staticmethod
    def get_known_colors():
        """
        Returns a list of all known colors.
        :return: Color[]
        """
        kc = list()
        kc.append(KnownColors.ALICE_BLUE)
        kc.append(KnownColors.ANTIQUE_WHITE)
        kc.append(KnownColors.AQUA)
        kc.append(KnownColors.AQUAMARINE)
        kc.append(KnownColors.AZURE)
        kc.append(KnownColors.BEIGE)
        kc.append(KnownColors.BISQUE)
        kc.append(KnownColors.BLACK)
        kc.append(KnownColors.BLANCHED_ALMOND)
        kc.append(KnownColors.BLUE)
        kc.append(KnownColors.BLUE_VIOLET)
        kc.append(KnownColors.BROWN)
        kc.append(KnownColors.BURLY_WOOD)
        kc.append(KnownColors.CADET_BLUE)
        kc.append(KnownColors.CHARTREUSE)
        kc.append(KnownColors.CHOCOLATE)
        kc.append(KnownColors.CORAL)
        kc.append(KnownColors.CORN_FLOWER_BLUE)
        kc.append(KnownColors.CORNSILK)
        kc.append(KnownColors.CRIMSON)
        kc.append(KnownColors.CYAN)
        kc.append(KnownColors.DARK_BLUE)
        kc.append(KnownColors.DARK_CYAN)
        kc.append(KnownColors.DARK_GOLDENROD)
        kc.append(KnownColors.DARK_GRAY)
        kc.append(KnownColors.DARK_GREEN)
        kc.append(KnownColors.DARK_KHAKI)
        kc.append(KnownColors.DARK_MAGENTA)
        kc.append(KnownColors.DARK_OLIVE_GREEN)
        kc.append(KnownColors.DARK_ORANGE)
        kc.append(KnownColors.DARK_ORCHID)
        kc.append(KnownColors.DARK_RED)
        kc.append(KnownColors.DARK_SALMON)
        kc.append(KnownColors.DARK_SEA_GREEN)
        kc.append(KnownColors.DARK_SLATE_BLUE)
        kc.append(KnownColors.DARK_SLATE_GRAY)
        kc.append(KnownColors.DARK_TURQUOISE)
        kc.append(KnownColors.DARK_VIOLET)
        kc.append(KnownColors.DEEP_PINK)
        kc.append(KnownColors.DEEP_SKY_BLUE)
        kc.append(KnownColors.DIM_GRAY)
        kc.append(KnownColors.DODGER_BLUE)
        kc.append(KnownColors.FIRE_BRICK)
        kc.append(KnownColors.FLORAL_WHITE)
        kc.append(KnownColors.FOREST_GREEN)
        kc.append(KnownColors.FUCHSIA)
        kc.append(KnownColors.GAINSBORO)
        kc.append(KnownColors.GHOST_WHITE)
        kc.append(KnownColors.GOLD)
        kc.append(KnownColors.GOLDENROD)
        kc.append(KnownColors.GRAY)
        kc.append(KnownColors.GREEN)
        kc.append(KnownColors.GREEN_YELLOW)
        kc.append(KnownColors.HONEYDEW)
        kc.append(KnownColors.HOT_PINK)
        kc.append(KnownColors.INDIAN_RED)
        kc.append(KnownColors.INDIGO)
        kc.append(KnownColors.IVORY)
        kc.append(KnownColors.KHAKI)
        kc.append(KnownColors.LAVENDER)
        kc.append(KnownColors.LAVENDER_BLUSH)
        kc.append(KnownColors.LAWN_GREEN)
        kc.append(KnownColors.LEMON_CHIFFON)
        kc.append(KnownColors.LIGHT_BLUE)
        kc.append(KnownColors.LIGHT_CORAL)
        kc.append(KnownColors.LIGHT_CYAN)
        kc.append(KnownColors.LIGHT_GOLDENROD_YELLOW)
        kc.append(KnownColors.LIGHT_GRAY)
        kc.append(KnownColors.LIGHT_GREEN)
        kc.append(KnownColors.LIGHT_PINK)
        kc.append(KnownColors.LIGHT_SALMON)
        kc.append(KnownColors.LIGHT_SEA_GREEN)
        kc.append(KnownColors.LIGHT_SKY_BLUE)
        kc.append(KnownColors.LIGHT_SLATE_GRAY)
        kc.append(KnownColors.LIGHT_STEEL_BLUE)
        kc.append(KnownColors.LIGHT_YELLOW)
        kc.append(KnownColors.LIME)
        kc.append(KnownColors.LIME_GREEN)
        kc.append(KnownColors.LINEN)
        kc.append(KnownColors.MAGENTA)
        kc.append(KnownColors.MAROON)
        kc.append(KnownColors.MEDIUM_AQUAMARINE)
        kc.append(KnownColors.MEDIUM_BLUE)
        kc.append(KnownColors.MEDIUM_ORCHID)
        kc.append(KnownColors.MEDIUM_PURPLE)
        kc.append(KnownColors.MEDIUM_SEA_GREEN)
        kc.append(KnownColors.MEDIUM_SLATE_BLUE)
        kc.append(KnownColors.MEDIUM_SPRING_GREEN)
        kc.append(KnownColors.MEDIUM_TURQUOISE)
        kc.append(KnownColors.MEDIUM_VIOLET_RED)
        kc.append(KnownColors.MIDNIGHT_BLUE)
        kc.append(KnownColors.MINT_CREAM)
        kc.append(KnownColors.MISTY_ROSE)
        kc.append(KnownColors.MOCCASIN)
        kc.append(KnownColors.NAVAJO_WHITE)
        kc.append(KnownColors.NAVY)
        kc.append(KnownColors.OLD_LACE)
        kc.append(KnownColors.OLIVE)
        kc.append(KnownColors.OLIVE_DRAB)
        kc.append(KnownColors.ORANGE)
        kc.append(KnownColors.ORANGE_RED)
        kc.append(KnownColors.ORCHID)
        kc.append(KnownColors.PALE_GOLDENROD)
        kc.append(KnownColors.PALE_GREEN)
        kc.append(KnownColors.PALE_TURQUOISE)
        kc.append(KnownColors.PALE_VIOLET_RED)
        kc.append(KnownColors.PAPAYA_WHIP)
        kc.append(KnownColors.PEACH_PUFF)
        kc.append(KnownColors.PERU)
        kc.append(KnownColors.PINK)
        kc.append(KnownColors.PLUM)
        kc.append(KnownColors.POWDER_BLUE)
        kc.append(KnownColors.PURPLE)
        kc.append(KnownColors.RED)
        kc.append(KnownColors.ROSY_BROWN)
        kc.append(KnownColors.ROYAL_BLUE)
        kc.append(KnownColors.SADDLE_BROWN)
        kc.append(KnownColors.SALMON)
        kc.append(KnownColors.SANDY_BROWN)
        kc.append(KnownColors.SEA_GREEN)
        kc.append(KnownColors.SEA_SHELL)
        kc.append(KnownColors.SIENNA)
        kc.append(KnownColors.SILVER)
        kc.append(KnownColors.SKY_BLUE)
        kc.append(KnownColors.SLATE_BLUE)
        kc.append(KnownColors.SLATE_GRAY)
        kc.append(KnownColors.SNOW)
        kc.append(KnownColors.SPRING_GREEN)
        kc.append(KnownColors.STEEL_BLUE)
        kc.append(KnownColors.TAN)
        kc.append(KnownColors.TEAL)
        kc.append(KnownColors.THISTLE)
        kc.append(KnownColors.TOMATO)
        kc.append(KnownColors.TURQUOISE)
        kc.append(KnownColors.VIOLET)
        kc.append(KnownColors.WHEAT)
        kc.append(KnownColors.WHITE)
        kc.append(KnownColors.WHITE_SMOKE)
        kc.append(KnownColors.YELLOW)
        kc.append(KnownColors.YELLOW_GREEN)
        return kc
