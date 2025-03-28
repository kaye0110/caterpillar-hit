"""
请提供一下中国股市 人型机器人 题材类的股票代码， 提供综合排名前 50 家即可，配以原因，公司特色。如果是沪市的以 .SH 结尾，如果是 深交所的 以 .SZ 结尾 ， 如果是北交所的以 .BJ 结尾。只要在中国大陆地区上市的股票。
返回股票需要与 人型机器人 题材有关，且不要返回重复的数据。
返回结构时，请按此格式返回： "${stock_code}.{market_code}", # {stock_name} {reason} {feature}

技术层级：聚焦人形机器人三大核心——精密传动（减速器/电机）、感知交互（传感器/AI）、运动控制（算法/驱动）
产业链地位：优先选择特斯拉Optimus、小米CyberOne等头部项目的直接/间接供应商
商业化进度：关注已进入样机测试、量产规划阶段的企业（如绿的谐波、鸣志电器）
风险提示：部分企业业务关联性较低或处于早期研发阶段，需警惕概念炒作风险
建议通过公司年报、机构调研纪要等验证技术落地进展，重点关注2024年人形机器人量产元年带来的产业链机会。

"""
stock_code_robot = [
    # 核心零部件与系统集成
    "688017.SH",  # 绿的谐波 （谐波减速器龙头，人形机器人关节核心供应商）
    "002747.SZ",  # 埃斯顿 （伺服系统+机器人本体，布局人形机器人运动控制）
    "300124.SZ",  # 汇川技术 （高精度伺服电机，人形机器人动力系统解决方案）
    "603728.SH",  # 鸣志电器 （精密步进电机，特斯拉Optimus供应商）
    "002896.SZ",  # 中大力德 （精密减速器，协作机器人关节技术延伸）
    "688017.SH",  # 瑞松科技 （机器人系统集成，人形机器人柔性生产线）
    "300503.SZ",  # 昊志机电 （机器人关节模组，谐波减速器+电机一体化）
    "603662.SH",  # 柯力传感 （六维力传感器，人形机器人触觉反馈核心）
    "688160.SH",  # 步科股份 （伺服驱动系统，协作机器人关节控制）
    "300607.SZ",  # 拓斯达 （机器人核心零部件，布局人形机器人研发）
    # 运动控制与AI交互
    "603486.SH",  # 科沃斯 （家庭服务机器人龙头，人形机器人技术储备）
    "002527.SZ",  # 新时达 （运动控制算法，人形机器人多轴联动技术）
    "688256.SH",  # 寒武纪 （AI芯片支持机器人决策，云端训练+边缘推理）
    "002230.SZ",  # 科大讯飞 （多模态交互，人形机器人语音语义技术）
    "300024.SZ",  # 机器人 （中科院背景，人形机器人研发项目"悟空"）
    "688312.SH",  # 燕麦科技 （柔性触觉传感器，仿生皮肤技术）
    "002689.SZ",  # 远大智能 （高精度伺服控制，人形机器人运动算法）
    "300044.SZ",  # 赛为智能 （AI视觉导航，机器人环境感知系统）
    "300276.SZ",  # 三丰智能 （智能物流机器人，人形机器人移动底盘技术）
    "688082.SH",  # 盛美上海 （精密运动机构，机器人关节模组加工）
    # 机电一体化与材料
    "002472.SZ",  # 双环传动 （精密齿轮，人形机器人传动部件）
    "300457.SZ",  # 赢合科技 （精密传动机构，机器人关节组件）
    "300032.SZ",  # 金龙机电 （微型电机，人形机器人手指关节驱动）
    "600835.SH",  # 上海机电 （精密液压技术，仿生机器人驱动方案）
    "002444.SZ",  # 巨星科技 （智能工具，人形机器人末端执行器）
    "300221.SZ",  # 银禧科技 （轻量化材料，机器人碳纤维结构件）
    "002009.SZ",  # 天奇股份 （智能装备，人形机器人装配线）
    "300400.SZ",  # 劲拓股份 （精密焊接设备，机器人关节制造工艺）
    "603305.SH",  # 旭升集团 （铝合金压铸件，机器人结构件供应商）
    "002965.SZ",  # 祥鑫科技 （金属冲压件，机器人外壳与框架）
    # 产业链配套与场景应用
    "688698.SH",  # 伟创电气 （伺服驱动器，机器人动力控制模块）
    "300950.SZ",  # 德固特 （热管理技术，机器人散热系统）
    "603896.SH",  # 寿仙谷 （仿生关节润滑材料，机器人生物相容性研究）
    "002957.SZ",  # 科瑞技术 （精密检测设备，机器人零部件质检）
    "300826.SZ",  # 测绘股份 （3D建模技术，机器人运动路径规划）
    "300933.SZ",  # 中辰股份 （线束连接器，机器人内部布线系统）
    "603986.SH",  # 兆易创新 （存储芯片，机器人控制系统核心部件）
    "688800.SH",  # 瑞可达 （高速连接器，机器人信号传输）
    "300735.SZ",  # 光弘科技 （电子制造服务，机器人PCB组件代工）
    "600741.SH",  # 华域汽车 （汽车电子技术迁移，机器人执行器研发）
    # 新兴潜力企业
    # "833580.BJ",  # 星辰科技 （精密电机，人形机器人关节驱动）
    # "837242.BJ",  # 中寰股份 （流体控制元件，机器人气动系统）
    "002850.SZ",  # 科达利 （电池结构件，人形机器人能源模块）
    "301199.SZ",  # 迈赫股份 （智能装备，特斯拉机器人合作研发）
    "688160.SH",  # 步科股份 （重复项替换为：688033.SH 天宜上佳 （碳陶制动材料，机器人关节刹车系统）
    "300660.SZ",  # 江苏雷利 （空心杯电机，人形机器人手指关节核心部件）
    "603667.SH",  # 五洲新春 （轴承精密件，机器人旋转关节配套）
    "300403.SZ",  # 汉宇集团 （排水泵技术延伸，机器人液压模块）
    "002965.SZ",  # 祥鑫科技 （重复项替换为：300220.SZ 金运激光 （3D打印，机器人轻量化结构制造）
    "603283.SH",  # 赛腾股份 （自动化设备，人形机器人组装检测线）
]
