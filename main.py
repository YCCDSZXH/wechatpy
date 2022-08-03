import markdown
import wechatlib as wx

appid = ""
secert = ""
wx = wx.wechat(appid, secert)
token = wx.token
html = markdown.markdown(open("测试文章.md", "r").read(), extensions=["markdown.extensions.extra", "markdown.extensions.codehilite", "markdown.extensions.tables"])

id = wx.upload_post("测试标题3", "YCCD", html, "")
wx.send_to_all(id)