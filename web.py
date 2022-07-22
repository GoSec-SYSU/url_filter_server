import os

from sanic import Sanic, response
from sanic.response import json, text
import json as sys_json
import sink_reader
# from shortest_url_handler_replace import Shortest_Url_Handler_Replace
# from shortest_url_handler_delete import Shortest_Url_Handler_Delete
# import link_detection
from dao import mysql
import _thread

app = Sanic("detection")


@app.route("/", methods=["GET", "POST"])
async def test(request):
    return json({"hello": "world"})


# ori_url
@app.route("/filter_url_replace", methods=["POST", ])
def create_user(request):
    # return json({"mes": 'fff', "url": '爸爸打我', "similarity": 'ffff'})
    form_data = request.form
    print('form_data: ', form_data)
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
    return json({"mes": mes, "url": left_str + filted_url + right_str, "similarity": str(similarity)})


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
    return json({"mes": mes, "url": left_str + filted_url + right_str, "similarity": str(similarity)})


# ori_url
@app.route("/get_sink", methods=["GET", ])
def create_user(request):
    url = os.path.join(os.path.dirname(__file__), 'data', 'base_sink.txt')
    data = sink_reader.read(url)
    return json(data)


def insert_collect(package_name, method_sign, xpos_id, content):
    # target_file = ['first_leak_hook.txt', 'third_leak_hook.txt', 'share_type_deob.txt', 'main_platform_deob.txt']
    target_type = ''
    print('sink_reader.type: ', sink_reader.type)
    print('type: ', sink_reader.type[method_sign]['sink_method'])
    print('from: ', sink_reader.type[method_sign]['from'])
    conn = mysql()
    sink_method = sink_reader.type[method_sign]['sink_method']
    sql = 'what the hell'
    if sink_reader.type[method_sign]['from'] == 'first_leak_hook.txt':
        target_type = 'ASI_first'
        sql = "insert into dynamic_url(package_name, user, sink_method, method_sign, content, {}) values('{}', '{}', '{}', '{}', '{}', 1)".format(
            target_type, package_name, xpos_id, sink_method, method_sign, content)
    elif sink_reader.type[method_sign]['from'] == 'third_leak_hook.txt':
        target_type = 'ASI_third'
        sql = "insert into dynamic_url(package_name, user, sink_method, method_sign, content, {}) values('{}', '{}', '{}', '{}', '{}', 1)".format(
            target_type, package_name, xpos_id, sink_method, method_sign, content)
    elif sink_reader.type[method_sign]['from'] == 'share_type_deob.txt':
        target_type = 'SCM'
        sql = "insert into dynamic_url(package_name, user, sink_method, method_sign, content, {}, IS_SCM) values('{}', '{}', '{}', '{}', '{}', 1, 1)".format(
            target_type, package_name, xpos_id, sink_method, method_sign, content)
    elif sink_reader.type[method_sign]['from'] == 'main_platform_deob.txt':
        target_type = 'SCM'
        sql = "insert into dynamic_url(package_name, user, sink_method, method_sign, content, {}, HTS_SCM) values('{}', '{}', '{}', '{}', '{}', 1, 1)".format(
            target_type, package_name, xpos_id, sink_method, method_sign, content)
    elif sink_reader.type[method_sign]['from'] == 'clip.txt':
        target_type = 'SCM'
        sql = "insert into dynamic_url(package_name, user, sink_method, method_sign, content, {}, TS_SCM) values('{}', '{}', '{}', '{}', '{}', 1, 1)".format(
            target_type, package_name, xpos_id, sink_method, method_sign, content)
    print('sql: ', sql)
    conn.query(sql)
    conn.close()


# share_content_collect_url
@app.route("/share_content_collect_url", methods=["POST", ])
def create_user(request):
    form_data = request.form
    package_name = form_data['package_name'][0]
    method_sign = form_data['method_sign'][0]
    xpos_id = form_data['xpos_id'][0]
    sink_method = form_data['sink_method'][0]
    content = form_data['link'][0]
    print('share_content_collect_url: ', sink_method, ' ', method_sign, ', ', xpos_id, ', ', content)
    # 加锁
    # err, link = link_detection.handle_original_url(content)
    # if link == '':
    #     return json('{"mes": "empty"}')
    # domain = link_detection.get_domain(link)

    insert_collect(package_name, method_sign, xpos_id, content)
    return json('{"mes": "200"}')

    # temp
    print('domain: ', domain)
    # buff_d: package_name -> sign -> domain -> xpose_id -> link
    link_detection.lock.acquire()
    if package_name not in link_detection.buff_d:
        link_detection.buff_d[package_name] = dict()
    if method_sign not in link_detection.buff_d[package_name]:
        link_detection.buff_d[package_name][method_sign] = dict()
    if domain not in link_detection.buff_d[package_name][method_sign]:
        link_detection.buff_d[package_name][method_sign][domain] = dict()
    if xpos_id not in link_detection.buff_d[package_name][method_sign][domain]:
        link_detection.buff_d[package_name][method_sign][domain][xpos_id] = []
    link_detection.buff_d[package_name][method_sign][domain][xpos_id].append(content)
    if len(link_detection.buff_d[package_name][method_sign][domain]) == 2:  # 有两个xpose_id
        sum = 0
        task = {'package_name': package_name, 'link': []}
        for key, value in link_detection.buff_d[package_name][method_sign][domain].items():
            if len(value) >= 2:
                sum += 1
                task['link'].append(value)
        if sum == 2:
            link_detection.task_l.append(task)
            del link_detection.buff_d[package_name][method_sign][domain]
    # 释放锁
    link_detection.lock.release()
    return json('{"mes": "200"}')


# ori_url
@app.route("/get_sink_by_package_name", methods=["POST", ])
def create_user(request):
    form_data = request.form
    package_name = form_data['package_name'][0]
    print('package_name: ', package_name)
    url = os.path.join(os.path.dirname(__file__), 'data', 'top300_metadata')
    data = sink_reader.read_by_package_name(url, package_name)
    print('data: ', data)
    return json(data)


# get_error
@app.route("/get_error", methods=["GET", ])
def get_error(request):
    form_data = request.form
    error = form_data['error'][0]
    print('error: ', error)
    return json({"ok": 123})


# hook主逻辑的class
@app.route("/sink_class", methods=["GET", ])
async def create_user(request):
    # f = open(os.path.join(os.path.dirname(__file__), "data", "Remote.class"), 'rb')
    return await response.file_stream(
        os.path.join(os.path.dirname(__file__), "data", "DataHandler.class"),
        headers={'X-Serverd-By': 'YuanRenXue Python'}
    )


# error
@app.route("/error", methods=["POST", ])
async def error(request):
    form_data = request.form
    print(form_data)
    error = form_data['error'][0]
    print('ori_url: ', error)
    return json({"code": 200})


# log
@app.route("/log", methods=["POST", ])
async def log(request):
    form_data = request.form
    print(form_data)
    log = form_data['log'][0]
    print('log: ', log)
    return json({"code": 200})


if __name__ == "__main__":
    # _thread.start_new_thread(link_detection.fun(), ())
    # print('asd')
    app.run(host="0.0.0.0", port=5000)
