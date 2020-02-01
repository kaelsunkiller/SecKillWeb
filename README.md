# SecKillWeb
SecKillWeb for auto snap up

## Version 0.1
* Python 3.7<br>
* Selenium==3.141.0

Support `multi-user` and `multi-task`. Only support [**网易优选**](https://you.163.com) for now.

## 使用方法
### 安装环境
各平台都需要安装python3.x以上版本，具体安装方法请自行搜索<br>
请确保python环境变量添加正确，在命令行中可用<br>
各平台使用命令行安装requirement.txt<br>
* 如windows右键开始菜单打开命令行，输入：<br>
`cd your-path/SecKillWeb/`<br>
`python install -r requirement.txt`
* 其他环境同理

### 下载Chromedrive
到[**chromedrive**](http://npm.taobao.org/mirrors/chromedriver/)将chromedriver.exe移动到python安装目录（含有python.exe的文件夹）
版本查看请在`Chrome→设置→关于Chrome`查看

### 用户配置
使用`笔记本程序`或`notepad++`编辑`config.ini`文件<br>

[items-url]<br>
便签下为需要抢购的商品页面链接，如 http://you.163.com/item/detail?id=3988533 ，打开商品页面取到`id`后的数字即可<br>
建议使用`http`协议，如复杂链接为`https`开头，请自行更换<br>

[items-prefer]<br>
需要抢购物品的页面选项，即商品样式，可选，每行代表[items-url]标签中对应位置商品的选项<br>
![](https://github.com/kaelsunkiller/SecKillWeb/blob/master/readme/1.PNG)<br>
可为字符串（即中文或英文文字，应与商品描述最下方的选项图片一致，不确定的可只写主要部分，如“黑色外衣”和“白色外衣”两个选项，则可写“黑色”或“白色”即可）<br>
![](https://github.com/kaelsunkiller/SecKillWeb/blob/master/readme/2.PNG)<br>
也可为数字（需为纯数字，否则认定为字符串，标识选项位置，表示目标选项在选项条中为第几个，如“黑色”可写为0，“白色”可写为1，注：位置数从0开始）<br>
若需要则需要全部填写，不需要则删除[items-prefer]及标签下内容，程序会按网页默认选项购买<br>

[user-info]<br>
用户信息，两行为一组，分别为登录用户名和密码（目前使用手机号和密码，请自行设置），支持多用户并发，可根据硬件配置自行调整<br>
也可删除此标签，则使用人工登录，此时需要使用图形化界面（见[config-params]），程序会在打开浏览器时等待10分钟，用户可自行操作登录<br>

[config-params]<br>
程序配置参数<br>
check_delay_top=10    定时循环刷新页面间隔最大值<br>
check_delay_btm=2     定时循环刷新页面间隔最大值<br>
always_circle=0       是否一直循环，1为是，0为否<br>
time_out=24           如非一直循环，循环最大时间数，单位小时<br>
multi_user=1          若人工登录，需要指定多用户人数<br>
headless=1            是否使用图形化界面，为0时将后台运行，看不到浏览器界面<br>

### 运行

在`SecKillWeb`主文件夹下运行命令行代码：<br>
`python SecKillWeb.py`
如需终止，在终端中按下`ctrl`+`c`（windows）或`ctrl`+`c`（Mac），等待片刻即可

## License
Copyright (c) 2020, kaelsunkiller. For more details please see [**LICENSE.md**](https://github.com/kaelsunkiller/SecKillWeb/blob/master/LICENSE)
