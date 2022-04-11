import random
import string

if __name__ == '__main__':
    str = ''.join(random.sample(string.ascii_letters + string.digits, 20))
    print(str)