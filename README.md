# 面向IP地址的异常域名分析挖掘与取证
![](https://img.shields.io/badge/license-WTFPL-blue.svg) ![](https://img.shields.io/github/repo-size/JX-Wang/IP-Analysis.svg) ![](https://img.shields.io/bitbucket/issues-raw/JX-Wang/IP-Analysis.svg) ![](https://img.shields.io/github/forks/JX-Wang/IP-Analysis.svg?label=Fork) ![](https://img.shields.io/github/stars/JX-Wang/IP-Analysis.svg?style=social)  
### 系统介绍
该系统主要解决的问题为分析一个IP地址的恶意性，输入一个IP或者IP段(全球)，输出该IP/段的关联域名/证书以及其恶意性，包括安全，赌博，色情，钓鱼，诈骗，恶意软件等  

### 大致思路
对于IP的恶意性判断主要采用方法的是对IP对应的域名所提供的服务进行性质判断，核心的思路大致为下图所示  
![](https://github.com/JX-Wang/IP-Analysis/blob/master/Frame/ideas_new.jpg)  
1. 对 IP 进行反向解析，得到可能与之绑定的域名
2. 对第1步得到域名进行DNS解析，得到IP地址后与源IP进行对比，判断一致性
3. 将第2步得到的符合条件的域名进行恶意性检测，判断域名的性质，从而判断IP的性质
4. 对恶意性域名进行取证并入库  

### 实现细节
#### 1. IP反向解析
目前的IP反向解析有三种思路: PTR，证书和第三方获取; 目前数据质量最好的获取方式是从第三方获取，数据量大而且准确度较高，PTR和证书有数据，但缺点是数据量小且质量稍差，但是还是有很大的参考价值；
#### 2. DNS验证
DNS验证模块主要使用DNS探测域名的A记录，从而来比对IP的一致性;
#### 3. 恶意性检测
主要采用基于第三方的域名检测，例如百度，360，Macfee等等,也会采用网站的文本分析，图像识别等方式来
#### 4. 取证
主要对恶意域名进行网页快照的信息取证

### 实现难点
* IP反查与验证，如何提高反查的有效性
* 海量数据存储，巨大的数据增量如何处理
* 次级域名获取，如何实现高效的次级域名获取
* 恶意性分析与取证，如何实现多种恶意性的鉴别
### 系统架构
![](https://github.com/JX-Wang/IP-Analysis/blob/master/Frame/new_frame_2.jpg)   

### 主要数据流
![](https://github.com/JX-Wang/IP-Analysis/blob/master/Frame/pattern1.jpg)  

### 详细设计
![](https://github.com/JX-Wang/IP-Analysis/blob/master/Frame/pattern1.jpg)  

### 数据库设计
![](https://developing)  

### 使用到的技术
* Python2.x
* MySQL5.7.x
* Kafka
* Zookeeper
* ElasticSearch
* 其他web类 还未计划
