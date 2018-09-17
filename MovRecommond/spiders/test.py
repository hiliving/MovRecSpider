import re
list = ['\xa0', '\r\n']
if len("".join(list).strip())==0:
    print("----------00000000000000-----------",len("".join(list).strip()))
# mv_time = '发布时间：2018-08-05'
# time =re.search(r"(\d{4}-\d{1,2}-\d{1,2})", mv_time).group(0)
# print(time)