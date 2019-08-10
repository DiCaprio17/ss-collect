# coding=utf-8
import requests
from lxml import etree
import base64
import os


class free_ss:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
        }

        self.url_l = ["https://flywind.ml/free-ss", "https://www.youneed.win/free-ss"]

    # 获取页面全部ss  ['138.68.211.58', '14196', 'isx.yt-52004688', 'aes-256-cfb', '22:12:05', 'US',...
    def extract_all_ss(self, html_str):
        print("开始获取页面全部ss")
        html = etree.HTML(html_str)
        ss_content = html.xpath('//section//td//text()')
        # print(ss_content)
        return ss_content

    # 将原始ss数据分割好    [['138.68.211.58', '14196', 'isx.yt-52004688', 'aes-256-cfb', '22:12:05', 'US'],....
    def trans(self, content):
        print("开始将原始ss数据进行分割")
        external_l = []
        n = int(len(content) / 6)
        for i in range(n):
            internal_l = []
            for j in range(6):
                internal_l.append(content[0])
                content.pop(0)
            external_l.append(internal_l)
        # print(external_l)
        return external_l

    # 提取JP的ss
    def jp(self, all_ss):
        print("开始提取JP的ss")
        jp_ss = []
        for l in all_ss:
            if l[5] == 'JP':
                jp_ss.append(l)
        # print(jp_ss)
        return jp_ss

    # 测试ss速度，返回有效ss
    def test_speed(self, ss):
        print("开始测试ss速度")
        valid_ss = []
        for l in ss:
            try:
                # 使用popen不会出现中文乱码
                output = os.popen('ping %s' % l[0]).read()
                # 平均往返时间
                # print(int(output[-7:-3]))
                l.append(int(output[-7:-3]))
                valid_ss.append(l)
            except:
                continue
        # print(valid_ss)
        return valid_ss

    # 按ss速度从小到大排序
    def speed_sort(self, ss):
        print("开始按ss速度从小到大排序")
        for i in range(len(ss)):
            for j in range(len(ss) - i - 1):
                if ss[j][6] > ss[j + 1][6]:
                    temp = ss[j + 1][6]
                    ss[j + 1][6] = ss[j][6]
                    ss[j][6] = temp
        # print(ss)
        return ss

    # 生成ss://
    def ss_link(self, ss):
        print("开始生成ss://")
        link_l = []
        for l in ss:
            long_ss = l[3] + ":" + l[2] + "@" + l[0] + ":" + l[1]
            link = 'ss://' + base64.b64encode(long_ss.encode('utf-8')).decode('utf-8')
            link_l.append(link)
        # print(link_l)
        return link_l

    # 保存到txt
    def save2txt(self, ss):
        print("开始保存到txt")
        with open("ss.txt", "w", encoding='utf-8') as f:
            f.write(ss)

    def run(self):
        try:
            html_str = requests.get(url=self.url_l[0], headers=self.headers).content.decode()
        except:
            html_str = requests.get(url=self.url_l[1], headers=self.headers).content.decode()
        ss_content = self.extract_all_ss(html_str)
        splited_ss = self.trans(ss_content)
        get_jp_ss = self.jp(splited_ss)
        test_ss_speed = self.test_speed(get_jp_ss)
        ss_speed_sort = self.speed_sort(test_ss_speed)
        ss_link = self.ss_link(ss_speed_sort)
        self.save2txt(str(ss_link) + '\n\n' + str(ss_speed_sort))
        print(str(ss_link) + '\n\n' + str(ss_speed_sort))


if __name__ == '__main__':
    m = free_ss()
    m.run()
