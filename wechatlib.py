import re
import requests
class wechat():
    def get_access_token(self, appid, secert):
        res = requests.get(
            "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + appid + "&secret=" + secert)
        print("成功获取access_token: ", res.json()["access_token"])
        print("过期时间: ", res.json()["expires_in"])
        return res.json()["access_token"]

    def __init__(self, appid, secert):
        self.token = self.get_access_token(appid, secert)

    def upload_intext_img_bypath(self, path):
        res = requests.post(
            f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={self.token}", files={"media": open(path, "rb")})
        print(res.json())

    def upload_intext_img_byurl(self, url):
        img = requests.get(url).content
        f = open("test.jpg", "wb")
        f.write(img)
        f.close()
        res = requests.post(
            f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={self.token}", files={"media": open("test.jpg", "rb")})
        return res.json()["url"]

    def upload_thumb_img(self, path):
        res = requests.post(
            f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={self.token}&type=image", files={"media": open(path, "rb")})
        return res.json()

    def get_firstimg_asthumb(self, content):
        first_img = re.findall(r'src="(.*?)"', content)
        # print(first_img)
        img = requests.get(first_img[0]).content
        f = open("test.jpg", "wb")
        f.write(img)
        f.close()
        id = self.upload_thumb_img("test.jpg")["media_id"]
        print(id)
        return id

    def get_all_count(self):
        res = requests.get(
            f" https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token={self.token}")
        print(res.json())

    def get_image_mediaid(self):
        data = {
            "type": "image",
            "offset": 0,
            "count": 100
        }
        res = requests.post(
            f"https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={self.token}&type=image", json=data)
        print(res.json())

    def upload_post(self, title, author, content, thumb_media_id=""):
        if thumb_media_id == "":
            thumb_media_id = self.get_firstimg_asthumb(content)
        print(thumb_media_id)
        tmp = {
            "articles": [
                {
                    "title": title,
                    "author": author,
                    "content": content,
                    "thumb_media_id": thumb_media_id,
                }
            ]
        }
        res = requests.post(
            f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={self.token}", json=tmp)
        # res = requests.post(
        #     f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={self.token}", json={"media_id": res.json()["media_id"]})
        print(res.json()['media_id'])

    def send_to_all(self, media_id):
        tmp = {
            "filter": {
                "is_to_all": True,
                "tag_id": 2
            },
            "mpnews": {
                "media_id": media_id
            },
            "msgtype": "mpnews",
            "send_ignore_reprint": 0
        }
        res = requests.post(
            f"https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token={self.token}", json=tmp)
        print(res.json())
