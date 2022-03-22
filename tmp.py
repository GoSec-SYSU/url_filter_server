import crypt

if __name__ == '__main__':
    salt = crypt.mksalt(crypt.METHOD_SHA512)
    hash = crypt.crypt("helloworld", salt)
    print(hash)