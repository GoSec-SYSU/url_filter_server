# 导入easyocr
import easyocr
import os


def ocr_word_getter(path):
    # 创建reader对象
    reader = easyocr.Reader(['ch_sim', 'en'])
    # 读取图像
    result = reader.readtext(os.path.join(path))
    # 结果
    words = ""
    for i in result:
        word = i[1]
        words += word
    return words


if __name__ == '__main__':
    print(ocr_word_getter(
        os.path.join(os.getcwd(), 'screenshot', 'http...baby.qubaobei.com.yunqi.ios2.share_view.php', 'baby.png')))
