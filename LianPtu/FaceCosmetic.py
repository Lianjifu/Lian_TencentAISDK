# #!/usr/bin/python
# encoding=utf-8
import requests
import time
import hashlib
import base64
import uuid
from urllib import urlencode
import json

# 给定图片和美妆编码，对原图进行人脸美妆特效处理
class FaceCosmetic:

    def __init__(self):
        # 人脸美妆接口
	    self.face_cosmetic_url = "https://api.ai.qq.com/fcgi-bin/ptu/ptu_facecosmetic"      
	    # 腾讯AI开放平台应用key
        self.ai_qq_app_key = "you_app_key"                                       
	    # 腾讯AI开放平台应用id
        self.ai_qq_app_id = "you_app_id"
        # 图片路径                                             
	    self.image_url = "image/321.jpg"
        # 选择美妆编码
        self.cosmetic = 21

    # 腾讯AI开放平台-Facemerge接口鉴权签名
    def get_sign(self, para):
        # 签名的key有严格要求，按照key升序排列
        data = sorted(para.items(), key=lambda item: item[0])
        s = urlencode(data)
        # app_key最后加
        s += '&app_key=' + self.ai_qq_app_key
        # 计算md5报文信息
        md5 = hashlib.md5()
        md5.update(s)
        digest = md5.hexdigest()
        return digest.upper()

    # 读取图片数据
    def read_image(self):
        raw_data = open(self.image_url, "rb").read()
        image_data = base64.b64encode(raw_data)
        return image_data

    # 生成随机字符串16位
    def nonce_str(self):
        nonce_str = ''.join(str(uuid.uuid4()).split('-'))[0:16]
        return nonce_str

    # 发送post数据
    def request_url(self):
        image_data = self.read_image()
        nonce_str = self.nonce_str()
        data = {
            'app_id': self.ai_qq_app_id,
            'image': image_data,
            'cosmetic': self.cosmetic,  
            'time_stamp': str(int(time.time())),
            'nonce_str': nonce_str,
        }
        data["sign"] = self.get_sign(data)
        res = requests.post(self.face_cosmetic_url, data=data)
        return res

    def get_image(self):
    	res = self.request_url()
    	res_ret = res.json()["ret"]
        print res_ret
    	if res_ret == 0:
        	res_image = base64.b64decode(res.json()['data']['image'])
        	# 保存图片
        	img = open("image_out/out.jpg","wb")
        	img.write(res_image)
        	img.close()
        else:
        	return res_ret


if __name__ == '__main__':
	face = FaceCosmetic()
	face.get_image()