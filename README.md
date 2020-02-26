# Spider-AnJuKeHouseInformation<br>  
根据客户需求，编写安居客二手房信息爬虫，并利用pd、plt进行分析，最后根据标题文本生成词云。

## 简单记录过程与问题吧<br>  

### 1. 爬虫部分<br>
* 爬虫是由requests+xpath组成，因为数据量比较小（3000）所以直接用xlwt、xlrd存储在excel中。<br>  
* 大致的思路就是先获取主页html文本，利用xpath解析出每个二手房的链接，然后根据每个二手房的链接得到具体信息，再将具体信息用xptah解析。<br>  
* 页面跳转方式很简单，利用url翻页跳转，html标签中含有每个二手房的具体链接。<br>  
* 在爬取过程中，发现不是每个请求都是200，所以要做好异常处理，我的方法就是：主页与具体页面分别做 try except（未考虑数据抓取时重复，但该考虑）。<br>  
* 储存过程就是老代码了，不表。<br>  
  
### 2. 词云部分<br>
* 轮子，不表。<br>  
  
### 3. 数据分析部分<br>
* 主要用的就是 pandas ，图表使用matplotlib<br>  
* 有一个图表中文显示问题需提出：<br>  
  ` import matplotlib.pyplot as plt`<br>  
  ` plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签`<br>  
  ` plt.rcParams['axes.unicode_minus']=False #用来正常显示负号`<br>  
  做图前需要这两行代码。<br>  
* 余下的分析都在朱皮特文件中，需求注释很全，省略<br>  
  
  
