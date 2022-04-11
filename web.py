import os

from sanic import Sanic, response
from sanic.response import json, text
import json as sys_json
import sink_reader
from shortest_url_handler_replace import Shortest_Url_Handler_Replace
from shortest_url_handler_delete import Shortest_Url_Handler_Delete

app = Sanic("detection")


@app.route("/", methods=["GET", "POST"])
async def test(request):
    return json({"hello": "world"})


# ori_url
@app.route("/filter_url_replace", methods=["POST", ])
def create_user(request):
    form_data = request.form
    ori_url = form_data['ori_url'][0]
    print('ori_url: ', ori_url)

    # 防止有些分享内容不全是地址：比如分享内容为：”爸爸去哪儿，http://www.baidu.com/“
    def handle_original_url(url: str):
        http_index_l = url.find('http')
        if http_index_l == -1:
            return False, url, "", ""
        http_index_r = http_index_l
        while http_index_r < len(url) and url[http_index_r] != ' ':
            http_index_r += 1
        return True, url[:http_index_l], url[http_index_l: http_index_r], url[http_index_r:]

    normal_flag, left_str, cut_ori_url, right_str = handle_original_url(ori_url)

    if not normal_flag:
        return json({"mes": '木有url', "url": ori_url, "similarity": str(1.0)})
    print('cut_ori_url: ', cut_ori_url)
    suh = Shortest_Url_Handler_Replace(cut_ori_url)
    mes, filted_url, similarity = suh.get_shortest_url()
    print(mes, filted_url, similarity)
    return json({"mes": mes, "url": left_str+filted_url+right_str, "similarity": str(similarity)})

@app.route("/filter_url_delete", methods=["POST", ])
def create_user(request):
    form_data = request.form
    ori_url = form_data['ori_url'][0]
    print('ori_url: ', ori_url)

    # 防止有些分享内容不全是地址：比如分享内容为：”爸爸去哪儿，http://www.baidu.com/“
    def handle_original_url(url: str):
        http_index_l = url.find('http')
        if http_index_l == -1:
            return False, url, "", ""
        http_index_r = http_index_l
        while http_index_r < len(url) and url[http_index_r] != ' ':
            http_index_r += 1
        return True, url[:http_index_l], url[http_index_l: http_index_r], url[http_index_r:]

    normal_flag, left_str, cut_ori_url, right_str = handle_original_url(ori_url)

    if not normal_flag:
        return json({"mes": '木有url', "url": ori_url, "similarity": str(1.0)})
    print('cut_ori_url: ', cut_ori_url)
    suh = Shortest_Url_Handler_Delete(cut_ori_url)
    mes, filted_url, similarity = suh.get_shortest_url()
    print(mes, filted_url, similarity)
    return json({"mes": mes, "url": left_str+filted_url+right_str, "similarity": str(similarity)})


# ori_url
@app.route("/get_sink", methods=["GET", ])
def create_user(request):
    url = os.path.join(os.path.dirname(__file__), 'data', 'base_sink.txt')
    data = sink_reader.read(url)
    return json(data)


# hook主逻辑的class
@app.route("/sink_class", methods=["GET", ])
async def create_user(request):
    # f = open(os.path.join(os.path.dirname(__file__), "data", "Remote.class"), 'rb')
    return await response.file_stream(
        os.path.join(os.path.dirname(__file__), "data", "DataHandler.class"),
        headers={'X-Serverd-By': 'YuanRenXue Python'}
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
