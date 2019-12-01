# IP恶意性分析系统
![](https://img.shields.io/badge/license-WTFPL-blue.svg) ![](https://img.shields.io/github/repo-size/JX-Wang/IP-Analysis.svg) ![](https://img.shields.io/bitbucket/issues-raw/JX-Wang/IP-Analysis.svg) ![](https://img.shields.io/github/forks/JX-Wang/IP-Analysis.svg?label=Fork) ![](https://img.shields.io/github/stars/JX-Wang/IP-Analysis.svg?style=social)  
### 系统介绍
该系统主要解决的问题为分析一个IP地址的恶意性，输入一个IP或者IP段(全球)，输出该IP/段的关联域名/证书以及其恶意性，包括安全，赌博，色情，钓鱼，诈骗，恶意软件等  

### 实现难点
* IP反查与验证
* 海量数据存储
* 次级域名获取
* 恶意性分析与取证
### 系统架构
![](https://github.com/JX-Wang/IP-Analysis/blob/master/frame/new_frame_2.jpg)   

### 主要数据流
![](https://github.com/JX-Wang/IP-Analysis/blob/master/frame/pattern1.jpg)  

### 详细设计
![](https://github.com/JX-Wang/IP-Analysis/blob/master/frame/pattern1.jpg)  

### 数据库设计
![](https://developing)  

### 使用到的技术
* Python2.x
* MySQL5.7.x
* Kafka
* Zookeeper
* ElasticSearch
* 其他web类 还未计划
