# btFrame
这是一个策略回测框架，正在继续编写中

简单框架结构说明：

heart(负责初始化，数据派发) :启动项

------>> 

ogran(单个组织作为一个策略整体，由一个或者若干个neuron组成) ：由organConfig.xml配置所序的neuron

------>> 

neuron（单个策略的单元化神经元）:放置在在文件夹baseneuron下，需要自行按照格式放置所需的单个策略，并在baseneuron.xml里配置所需的属性

------>> 

result:最后的输出结果会以pd.pickle的格式放在result目录下

