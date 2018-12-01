# -*- coding: utf-8 -*-
import hashlib

mvUrl="https://www.cnblogs.com/xunbu7/p/8074417.html"
mvId = hashlib.md5(mvUrl.encode(encoding='UTF-8')).hexdigest()
print(mvId)