# 面向IP地址的异常域名分析挖掘与取证
![](https://img.shields.io/badge/license-WTFPL-blue.svg) ![](https://img.shields.io/github/repo-size/JX-Wang/IP-Analysis.svg) ![](https://img.shields.io/bitbucket/issues-raw/JX-Wang/IP-Analysis.svg) ![](https://img.shields.io/github/forks/JX-Wang/IP-Analysis.svg?label=Fork) ![](https://img.shields.io/github/stars/JX-Wang/IP-Analysis.svg?style=social)  
### 系统介绍
该系统主要解决的问题为分析一个IP地址的恶意性，输入一个IP或者IP段(全球)，输出该IP/段的关联域名/证书以及其恶意性，包括安全，赌博，色情，钓鱼，诈骗，恶意软件等  

### 大致思路
对于IP的恶意性判断主要采用方法的是对IP对应的域名所提供的服务进行性质判断，核心的思路大致为下图所示  
![](https://github.com/JX-Wang/IP-Analysis/blob/master/Frame/ideas.jpg)  
1. 对 IP 进行反向解析，得到可能与之绑定的域名
2. 对第1步得到域名进行DNS解析，得到IP地址后与源IP进行对比，判断一致性
3. 将第2步得到的符合条件的域名进行恶意性检测，判断域名的性质，从而判断IP的性质
4. 对恶意性域名进行取证并入库  

### 实现细节
i. 

### 实现难点
* IP反查与验证
* 海量数据存储
* 次级域名获取
* 恶意性分析与取证
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
