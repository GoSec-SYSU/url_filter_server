import os

from sanic import Sanic
from sanic.response import json, text
import json as sys_json
# from shortest_url_handler import Shortest_Url_Handler

app = Sanic("detection")

@app.route("/", methods=["GET", "POST"])
async def test(request):
    return json({"hello": "world"})

# ori_url
@app.route("/filter_url", methods=["POST", ])
def create_user(request):
    form_data = request.form
    ori_url = form_data['ori_url'][0]
    print(ori_url)
    suh = Shortest_Url_Handler(ori_url)
    mes, url, similarity = suh.get_shortest_url()
    print(mes, url, similarity)
    return json({"mes": mes, "url": url, "similarity": str(similarity)})

# ori_url
@app.route("/get_sink", methods=["GET", ])
def create_user(request):
    f = open(os.path.join(os.path.dirname(__file__), "files", "metadata.json"))
    data = sys_json.load(f)
    return json(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
