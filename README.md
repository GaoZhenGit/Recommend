## BLDA_TIFMF推荐算法 ##


----------

 - 算法简介
 本算法适用于微博或者推特等单向社交网络的用户推荐。能够自动提取数据库中的用户边关系，并按照设定的比例进行抽取测试集，并使用相关评估标准对推荐结果进行评估。本算法使用并行计算。
 - 代码运行环境
本实验代码需要的运行环境为：`Python2.7`，并安装库`Scipy`、`Numpy`、`LDA`；`Java1.7`或以上；`Linux`或`Windows`系统
 - 运行方式
通过在`sr`c文件夹下的`py.sh`或者`py.bat`启动文件进行运行，在运行时输入参数即可，以`py.bat`为例：
```
    py.bat database //根据sql从数据库获取用户边数据，格式化
    py.bat lda //推荐第一阶段，使用lda将用户分类到社区
    py.bat mf  //推荐第二阶段，为每个社区计算推荐结果并输出最终结果
    py.bat con //推荐结果评估，为现有结果评估，并输出评估文件
```
上述为基本推荐操作，按照顺序执行即可。以上命令行执行包括多个多个步骤，而这些步骤可以通过另外的参数进行单独执行：
```
    py.bat lda_executor //执行lda算法模型
    py.bat lda_filter //根据设定的阈值，对p(t|f)进行过滤
    py.bat mf_matrix //根据lda结果生成社区矩阵
    py.bat mf_mf //对每个社区矩阵做协同过滤矩阵分解
    py.bat mf_score //矩阵分解向乘
    py.bat mf_result //所有矩阵统计合并，输出推荐结果
```
输入需要从使用者的数据库读取，通过自定sql语句来读取数据：每行代表着一个现有关系，第一个为关注者id，第二个为被关注者id；  
输出结果在`src/data/mfDir/result/score_edge.txt`中，每行代表着一个推荐结果，第一个为关注者id，第二个为被关注者id；  
配置文件为`src/constant/__init__.py`，包括算法参数的设置。
 - 注意事项
本程序采用多进程运行，若需要关闭，则需要手动修改代码；  
本程序相对需要更多的空间资源，所以需要使用者关注计算数据量的大小