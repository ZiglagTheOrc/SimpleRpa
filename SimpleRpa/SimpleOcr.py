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
import sys
import cv2
import json
import numpy as np
from _Platform_Convergence import Config
from _Widget import Widget
from PIL import ImageGrab

maps = list()


def add_font(path):
    """
    Loads the font mapping at the specified path.
    :param path: The path to the font map folder.
    :return: void
    """
    # region Deserialize json file.
    if sys.platform == 'win32':
        fm = '\\'
    else:
        fm = '/'

    f = open(path + fm + "font_map.json", 'r')
    js = f.read()
    f.close()
    wr = json.loads(js)
    # endregion

    # region If already loaded exit now.
    l = len(maps)
    for i in range(l):
        if wr['name'] == maps[i].name:
            return "{\"response\":\"SUCCESS\"}"
    # endregion

    # region Load font map files and add to list of maps.
    fmp = Map()
    fmp.name = wr['name']
    l = len(wr['fonts'])
    for i in range(l):
        js0 = str(wr['fonts'][i])
        fnt = json.loads(str.replace(js0, "'", "\""))
        fmp.character.append(fnt['character'])
        fn = path + fm + fnt['filename']
        img = cv2.imread(fn, cv2.IMREAD_COLOR)  # np.array(Image.open(fn))
        bmp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        fmp.image.append(bmp)

    maps.append(fmp)
    return "{\"response\":\"SUCCESS\"}"
    # endregion


def perform_ocr(fontmaps, rect, ocr_threshold, capture_threshold, use_widget=None, duration=0):
    """
    Captures the screen at the specified rect and perform quick ocr using specified font maps.
    :param fontmaps: The list of fontmaps to look for.
    :param rect: Rectangular tuple area of the screen to capture.
    :param ocr_threshold: The matching threshold to use.
    :param capture_threshold: The threshold to use when reducing image to monochrome.
    :return: str
    """
    image = __capture(rect, capture_threshold)
    chars = __get_chars(image, fontmaps, ocr_threshold)
    if use_widget is None:
        use_widget = Config.use_widgets_by_default
        if duration == 0:
            duration = Config.default_widget_duration
    if use_widget:
        Widget._show_widget_rect(rect, duration)
    if len(chars) == 0:
        return '';
    data = __sort_chars(chars)
    text = __get_text(data)
    return text


# TODO: Is this the same as screen?
def __capture(rect, threshold):
    """
    Captures the specified area of the screen.
    :param rect: The rectangular tuple area of the screen to grab.
    :param threshold: The matching threshold to use.
    :return: Image
    """
    # region Get screen print and reduce to mnochrome
    bitmap = ImageGrab.grab(bbox=(rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3]), all_screens=True)
    image = np.array(bitmap)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1]
    # endregion

    # region Check to see if image needs inverted if so do it.
    whites = cv2.countNonZero(image) * 1.2
    blacks = rect[0] * rect[1] - whites

    #if whites > blacks:
    #    image = image.__invert__()

    #cv2.imwrite("z:\\ss.bmp", image)
    return image


def __get_chars(image, fontmaps, threshold):
    """
    Gets a list of all present characters in the image.
    :param fontmaps: The fontmap(s) to match against.
    :param threshold: The matching threshold to use.
    :return: Character[]
    """
    chars = list()
    # region If they gave us a string make it a list.
    if isinstance(fontmaps, str):
        fm = fontmaps
        fontmaps = list()
        fontmaps.append(fm)
    # endregion
    l0 = len(maps)
    l1 = len(fontmaps)
    for m in range(l0):
        for f in range(l1):
            if maps[m].name == fontmaps[f]:
                l3 = len(maps[m].image)
                for i in range(l3):
                    bmp = maps[m].image[i]
                    res = cv2.matchTemplate(image, bmp, cv2.TM_CCOEFF_NORMED)
                    loc = np.where(res >= threshold)
                    for pt in zip(*loc[::-1]):
                        char = Character()
                        char.left = pt[0]
                        char.top = pt[1]
                        char.width = bmp.shape[1]
                        char.height = bmp.shape[0]
                        char.char = maps[m].character[i]
                        chars.append(char)
    return chars


def __sort_chars(chars):
    """
    Takes the provided list of characters and sorts them into the order in which they appear.
    :param chars: The list of characters.
    :return: numpy.Array
    """
    # region convert list to numpy array and sort into groups
    l = len(chars)
    data = np.zeros((l, 5))
    for i in range(l):
        data[(i, 0)] = chars[i].left
        data[(i, 1)] = chars[i].top
        data[(i, 2)] = chars[i].width
        data[(i, 3)] = chars[i].height
        data[(i, 4)] = ord(chars[i].char)
    data = np.array(sorted(data, key=lambda x: (x[1], x[0])))
    # endregion

    # region Sort into precise order
    ln = data[(0, 1)]
    target = 13
    for i in range(l):
        if data[(i, 1)] - ln > target:
            ln = data[(i, 1)]
        else:
            data[(i, 1)] = ln
    data = np.array(sorted(data, key=lambda x: (x[1], x[0])))
    # endregion

    return data


def __get_text(data):
    """
    Creates a text string from a presorted list of characters.
    :param data: The numpy.array of presorted characters to use.
    :return: string
    """
    # region Convert to text
    txt = ''
    l = len(data)
    y = data[(0, 1)]
    is_end_of_line = False
    for i in range(l):
        char = int(data[(i, 4)])
        if data[(i, 1)] != y:
            txt += "\r\n"
            y = data[(i, 1)]
            is_end_of_line = True
        if i > 0 and not is_end_of_line:
            margin = data[(i - 1, 0)] + data[(i - 1, 3)]
            margin = data[(i, 0)] - margin
            if margin > 6:
                txt += chr(char)
                txt += " "
                continue

        txt += chr(char)
        is_end_of_line = False
    return txt
    # endregion


class Map:
    """
    Class to provide the structure for font map objects.
    """
    name = "",
    character = list()
    image = list()


class Character:
    """
    Class to provide structure for character objects.
    """
    left = 0
    top = 0
    width = 0
    height = 0
    char = ''
