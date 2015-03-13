# -*- coding: utf-8 -*-
import unittest

def convertISBN(isbn):
    checksum = 0
    if len(isbn) == 13 and isbn[:3] == "978":
        isbn10 = map(int, isbn[3:])

        for i in range(9):
            checksum += isbn10[i] * (10 - i)

        isbn10[9] = ((11 - checksum % 11) % 11)

        return ''.join(map(str, isbn10))
    elif len(isbn) == 10:
        isbn13 = map(int, "978" + isbn)

        for i in range(12):
            if i % 2 == 0:
                checksum += int(isbn13[i])
            else:
                checksum += int(isbn13[i]) * 3
        isbn13[12] = (10 - (checksum % 10)) % 10

        return ''.join(map(str, isbn13))
    else:
        return ""


def checkISBN(isbn):
    checksum = 0
    isbn = map(int, isbn)
    if len(isbn) == 10:
        for index in range(10):
            checksum += isbn[index] * (10-index)
        return checksum % 11 == 0
    elif len(isbn) == 13:
        for i in range(13):
            if i % 2 == 0:
                checksum += int(isbn[i])
            else:
                checksum += int(isbn[i]) * 3

        return checksum % 10 == 0

    else:
        return False


class TestISBN(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == "__main__":
    isbn = str(raw_input())
    print(convertISBN(isbn))