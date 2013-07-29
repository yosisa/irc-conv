# -*- coding: utf-8 -*-
# Core idea of this module are borrowed from:
#   http://loqui.sourcearchive.com/documentation/0.5.2-1ubuntu1/loqui__codeconv__tools_8c_source.html
# If you can read Japanese articles, see:
#   http://sunnyone41.blogspot.jp/2013/03/loqui-055loquiiso-2022-jp.html

ISO_2022_JP_TYPE_ASCII = 1
ISO_2022_JP_TYPE_JISX_0201_1976 = 2
ISO_2022_JP_TYPE_JISX_0201_KANA = 3
ISO_2022_JP_TYPE_JISX_0208_1978 = 4
ISO_2022_JP_TYPE_JISX_0208_1983 = 5

JIS_13KU_TABLE = [
    0x0000, 0x2460, 0x2461, 0x2462, 0x2463, 0x2464, 0x2465, 0x2466,
    0x2467, 0x2468, 0x2469, 0x246a, 0x246b, 0x246c, 0x246d, 0x246e,
    0x246f, 0x2470, 0x2471, 0x2472, 0x2473, 0x2160, 0x2161, 0x2162,
    0x2163, 0x2164, 0x2165, 0x2166, 0x2167, 0x2168, 0x2169, 0x0000,
    0x3349, 0x3314, 0x3322, 0x334d, 0x3318, 0x3327, 0x3303, 0x3336,
    0x3351, 0x3357, 0x330d, 0x3326, 0x3323, 0x332b, 0x334a, 0x333b,
    0x339c, 0x339d, 0x339e, 0x338e, 0x338f, 0x33c4, 0x33a1, 0x0000,
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x337b,
    0x301d, 0x301f, 0x2116, 0x33cd, 0x2121, 0x32a4, 0x32a5, 0x32a6,
    0x32a7, 0x32a8, 0x3231, 0x3232, 0x3239, 0x337e, 0x337d, 0x337c,
    0x2252, 0x2261, 0x222b, 0x222e, 0x2211, 0x221a, 0x22a5, 0x2220,
    0x221f, 0x22bf, 0x2235, 0x2229, 0x222a, 0x0000, 0x0000, 0x0000
]

ISO_2022_JP_TYPE_MAP = {
    '(J': ISO_2022_JP_TYPE_JISX_0201_1976,
    '(I': ISO_2022_JP_TYPE_JISX_0201_KANA,
    '(B': ISO_2022_JP_TYPE_ASCII,
    '$@': ISO_2022_JP_TYPE_JISX_0208_1978,
    '$B': ISO_2022_JP_TYPE_JISX_0208_1983
}

ISO_2022_JP_SHIFT_OUT = chr(0x0E)
ISO_2022_JP_SHIFT_IN = chr(0x0F)
ISO_2022_ESC = chr(0x1B)

HALFWIDTH_KATAKANA_UCS4_OFFSET = 0xFF60
HALFWIDTH_KATAKANA_7BIT_OFFSET = 0x20
HALFWIDTH_KATAKANA_8BIT_OFFSET = 0xA0

ERROR_STRING = '[!]'


def jis_to_unicode(text):
    dst = ''
    src = list(text)
    ctx = ISO_2022_JP_TYPE_ASCII
    shift_out_mode = False

    while src:
        c = src.pop(0)

        if c in ('\r', '\n'):
            dst += c
            ctx = ISO_2022_JP_TYPE_ASCII
            continue

        if c == ISO_2022_ESC:
            c1 = src.pop(0)
            c2 = src.pop(0)
            ctx = ISO_2022_JP_TYPE_MAP.get(c1 + c2, ISO_2022_JP_TYPE_ASCII)
            continue

        if ctx in (ISO_2022_JP_TYPE_JISX_0208_1983,
                   ISO_2022_JP_TYPE_JISX_0208_1978):
            if src[0] == ISO_2022_ESC:
                continue

            c1 = src.pop(0)
            c = ord(c) | 0x80
            c1 = ord(c1) | 0x80

            if c == 0xAD and 0xA1 <= c1 <= 0xFC:
                code = JIS_13KU_TABLE[c1 - 0xA0]
                if code != 0:
                    dst += unichr(code)
                else:
                    dst += ERROR_STRING
            else:
                char = chr(c) + chr(c1)
                dst += char.decode('euc-jp')
        elif ctx == ISO_2022_JP_TYPE_JISX_0201_KANA:
            if is_iso_2022_jp_7bit_halfwidth_kana(c):
                dst += unichr(HALFWIDTH_KATAKANA_UCS4_OFFSET -
                              HALFWIDTH_KATAKANA_7BIT_OFFSET + ord(c))
            else:
                dst += ERROR_STRING
        elif ctx == ISO_2022_JP_TYPE_JISX_0201_1976:
            if c == ISO_2022_JP_SHIFT_OUT:
                shift_out_mode = True
            elif c == ISO_2022_JP_SHIFT_IN:
                shift_out_mode = False
            elif shift_out_mode and is_iso_2022_jp_7bit_halfwidth_kana(c):
                dst += unichr(HALFWIDTH_KATAKANA_UCS4_OFFSET -
                              HALFWIDTH_KATAKANA_7BIT_OFFSET + ord(c))
            elif is_iso_2022_jp_8bit_halfwidth_kana(c):
                dst += unichr(HALFWIDTH_KATAKANA_UCS4_OFFSET -
                              HALFWIDTH_KATAKANA_8BIT_OFFSET + ord(c))
            elif is_ascii(c):
                dst += c
            else:
                dst += ERROR_STRING
        elif is_ascii(c):
            dst += c
        else:
            dst += ERROR_STRING

    return dst


def jis_to_utf8(text):
    return jis_to_unicode(text).encode('utf-8')


def is_ascii(char):
    return 0x00 <= ord(char) <= 0x7F


def is_iso_2022_jp_7bit_halfwidth_kana(char):
    return 0x20 < ord(char) <= 0x5F


def is_iso_2022_jp_8bit_halfwidth_kana(char):
    return 0xA0 < ord(char) <= 0xDF


if __name__ == '__main__':
    import sys
    for filename in sys.argv[1:]:
        with open(filename, 'rb') as f:
            print jis_to_utf8(f.read())
