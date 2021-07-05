from PIL import Image, ImageSequence, ImageDraw, ImageFont
import numpy
import os

class dogeGenerater:
    def __init__(self, gifDataPath, fontPath):
        # 保存变量
        self.fontPath = fontPath

        # 载入gif,拆分出每一页,放到迭代器里保存起来
        gif = Image.open(gifDataPath)
        self.iter = ImageSequence.Iterator(gif)

        # 获得通用的左侧图 背景图
        imgs = [frame.copy() for frame in ImageSequence.Iterator(gif)]
        # 取得第一张,用第一张作为左中的例子
        img = imgs[0]

        imgl = img.crop((0,0,30,86))
        self.imgl = imgl.convert('RGBA')

        self.imgc0 = img.crop((30,0,50,86))
        pass


    def draw(self, txt):
        # 计算出中间部分长度,并适当拉伸
        length = len(txt) * 43
        imgc = self.imgc0.resize((length, 86)).convert("RGBA")
        # 处理中间部分图片
        txtDraw = ImageDraw.Draw(imgc)
        fontStyle = ImageFont.truetype(self.fontPath, 43, encoding="utf-8")
        txtDraw.text((0, 20), txt, (0,0,0), font=fontStyle)
        self.imgc = imgc
        # 新建文件夹
        if not os.path.exists("./out"):
            os.mkdir("./out")
        # 循环处理
        index = 1
        # 新建列表保存数据
        imgs = []
        for frame in self.iter:
            # 切出右侧图片
            imgr = frame.crop((50,0,125,86))
            imgr = imgr.convert('RGBA')
            
            # 拼接
            npconcat = numpy.concatenate((self.imgl,self.imgc,imgr),axis=1)
            npconcat = Image.fromarray(npconcat)

            npconcat.save(f"out/{index}.png" )
            imgs.append(npconcat)
            index += 1
        imgs[0].save('out.gif', save_all=True, append_images=imgs[1:], transparency=25)


    
#     # 把图片流重新生成GIF动图
#     # imgs[0].save('out.gif', save_all=True, append_images=imgs[1:])



if __name__ == "__main__":
    dogeGenerater0 = dogeGenerater("./innerData/doge.gif", "./innerData/FangZhengHeiTiJianTi-1.ttf")
    dogeGenerater0.draw("嗯嗯")
