URL脱敏流程 

# 流程图 

![流程图](E:%5CPycharmProjects%5Cdetection%5C%E6%B5%81%E7%A8%8B%E5%9B%BE-1649334789617.jpg)

# 脱敏流程 

1. 输入原始URL，截取网页面，然后利用OCR提取其网页文字，最后获取源码+title，将三者作为ground truth保留。  
2. URL遍历器依次由简到繁抽取参数，生成更短的URL，比如对于https://www.baidu.com/?name=xinxin&age=21，会依次过滤成https://www.baidu.com/、https://www.baidu.com/?name=xinxin等等，每一次生成url后都会走一遍以下的流程。 
3. 用OCR方式提取网页的文本，将其拼接成一串字符串，然后利用文本相似度算法（余弦相似度）计算相似度，当相似度大于40%则直接跳到第7步，大于10%则走下一步，否则直接认为当前url不符合，返回第2步抽取下一个url。 
4. 用open-cv中的三直方图算法计算网页相似度，目前阈值设成80%，大于阈值会直接到第7步，大于70%则走下一步，否则直接认为当前url不符合，返回第2步。 
5. 用余弦相似度算法检测源码相似度，代码相似度达90%且网页title相同则进入第7步，否则走下一步。 
6. 若3、4和5步都无法检测，且遍历超过1024次直接认为当前url无法脱敏，程序结束，否则返回第2步。 
7. 将当前url参数特征存储起来，用作下一次使用，下一次如果碰到同样的url和参数就不用再走一次流程了，提高用户响应  

# 目前效果 

![效果图](E:%5CPycharmProjects%5Cdetection%5C%E6%95%88%E6%9E%9C%E5%9B%BE.png)

​		对于113个有用标注的脱敏测试中，共有103个完全脱敏成功，占91%，为完全脱敏有8个，占7%。脱敏失败的有2个，占2%左右，其中失败的原因是拼多多的界面不管怎么脱敏都只有登陆界面，另外一个马蜂窝旅行则是验证码界面，导致脱敏失败，**这个问题之后再想办法解决，暂时pending中** 