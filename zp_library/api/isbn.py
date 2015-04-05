# -*- coding: utf-8 -*-

def convertISBN(isbn):
    checksum = 0
    if len(isbn) == 13 and isbn[:3] == "978":
        isbn10 = map(int, isbn[3:-1])

        for i in range(9):
            checksum += isbn10[i] * (10 - i)

        check_digit = ((11 - checksum % 11) % 11)
        if check_digit == 10:
            check_digit = "X"
        isbn10.append(check_digit)

        return ''.join(map(str, isbn10))
    elif len(isbn) == 10:
        isbn13 = map(int, "978" + isbn[:-1])
        for i in range(12):
            if i % 2 == 0:
                checksum += int(isbn13[i])
            else:
                checksum += int(isbn13[i]) * 3
        check_digit = (10 - (checksum % 10)) % 10
        isbn13.append(check_digit)
        return ''.join(map(str, isbn13))
    else:
        return ""


def checkISBN(isbn):
    checksum = 0
    # isbn = map(int, isbn)
    if len(isbn) == 10:
        isbn10 = map(int, isbn[:-1])
        for index in range(9):
            checksum += isbn10[index] * (10-index)
        if isbn[-1] in ["x", "X"]:
            checksum += 10
        else:
            checksum += int(isbn[-1])
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

if __name__ == "__main__":
    print checkISBN("9788981722821")
    print checkISBN("898172282X")
    print convertISBN("9788981722821")
    print convertISBN("9788981722821") == "898172282X"
    print convertISBN("898172282X")
    print convertISBN("898172282X") == "9788981722821"
