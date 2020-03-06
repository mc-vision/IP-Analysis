### 恶意域名鉴定模块儿
----------

#### 功能
将RabbitMQ中接收到的数据进行解析，得到域名，并对其进行恶意性验证，并将结果以 ```(string(domain), string(malicious_type))``` 的形式返回给下一个RabbitQM消费者

#### 主要代码
主要是通过第三方进行鉴定，根据代码文件名选择鉴定方式

#### Contact
Author @ [junxiongwang](http://wudly.cn)  
Mail：wjx.wud@gmail.com