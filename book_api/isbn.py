def convertISBN(isbn):
    checksum = 0
    if len(isbn) == 13 and isbn[:3] == "978":
        isbn10 = map(int, isbn[3:])

        print isbn10

        for i in range(9):
            checksum += isbn10[i] * (10 - i)
            print checksum

        isbn10[9] = ((11 - checksum % 11) % 11)
        print isbn10[9]
        return ''.join(map(str, isbn10))

    elif len(isbn) == 10:
        isbn13 = map(int, "978" + isbn)

        for i in range(12):
            if i % 2 == 0:
                checksum += int(isbn13[i])
            else:
                checksum += int(isbn13[i]) * 3
        checksum = (10 - (checksum % 10)) % 10

        isbn13[12] = checksum
        return ''.join(map(str, isbn13))
    else:
        return ""


def checkISBN(isbn):
    checksum = 0
    isbn = map(int, isbn)
    if len(isbn) == 10:
        for index in range(10):
            checksum += isbn[index] * (10-index)
        if checksum % 11 == 0:
            return True
        else:
            return False
    elif len(isbn) == 13:
        for i in range(13):
            if i % 2 == 0:
                checksum += int(isbn[i])
            else:
                checksum += int(isbn[i]) * 3

        if checksum % 10 == 0:
            return True
        else:
            return False

    else:
        return False


if __name__ == "__main__":
    x = convertISBN("8979143427")
    print checkISBN("8979143427")
    print x
    print checkISBN(convertISBN(x))
