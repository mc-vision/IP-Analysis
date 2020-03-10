### DNS验证模块儿
----------

#### 功能
将RabbitMQ接收到的 ```(IP, [domain0, domain1])```, 这样的数据结构进行解析，然后将数据打包发送至下一个消息队列，发送的数据结构如下 ```(string(ip), string(domain), list[domain's ip])```

> 待添加功能 -> 若前后的IP地址不一致，则将新的IP地址放入消息队列中再次进行探测

#### 主要代码
> dns_verfication.py  # 通过RabbitMQ接收数据，回调函数指向obtaining_domain_ip()  

> resolving_ip_cname_by_dns.py  # 含有obtaining_domain_ip()方法，进行DNS解析  

#### Contact
Author @ [junxiongwang](http://wudly.cn)  
Mail：wjx.wud@gmail.com