新建 txt 文件：
```
Windows Registry Editor Version 5.00
[HKEY_CURRENT_USER\Software\Microsoft\InputMethod\Settings\CHS]
"LangBar Force On"=dword:00000000
"Enable Double Pinyin"=dword:00000001
"EmoticonTipTriggerCount"=dword:00000001
"HapLastDownloadTime"=hex(b):eb,69,29,59,00,00,00,00
"UserDefinedDoublePinyinScheme0"="FlyPY*2*^*iuvdjhcwfg xmlnpbksqszxkrltvyovt"
"DoublePinyinScheme"=dword:0000000a
"UDLLastUpdatedTime"="2017-05-27 22:01:40"
"UDLCount"=dword:0000018b
"UDLVisibleCount"=dword:0000018b
```
重命名为.reg 后缀的文件，在双击运行之前，记住要备份自己的注册表。

需要备份注册表路径为：
```
计算机\HKEY_CURRENT_USER\Software\Microsoft\InputMethod\Settings\CHS
```
最后，运行刚才保存的 reg 文件即可。
