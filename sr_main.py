import time
import tkinter as tk
from tkinter import ttk
# 导入模仪器器模块
import sr_TreeNode

# UI常量配置
UI_CONFIG = {
    'WINDOW_TITLE': '星穹铁道仪器计算器',
    'WINDOW_SIZE': '800x600',
    'COMBOBOX_WIDTH': 13,   #下拉框长度
    'PADDING_Y': 10,
    'PADDING_X': (10, 5),
    'STICKY_E': 'e',
    'STICKY_W': 'w'
}

# 定义仪器位置和对应的主词条选项
instrument_positions = {
    "未选择": ["未选择"],
    "头部": ["生命值"],
    "手部": ["攻击力"],
    "躯干": ["未选择", "生命值%", "攻击力%", "防御力%", "暴击率", "暴击伤害", "治疗量加成", "效果命中", "效果命中"],
    "脚部": ["未选择", "生命值%", "攻击力%", "防御力%", "速度"],
    "位面球": ["未选择", "生命值%", "攻击力%", "防御力%", "物理伤害加成", "火元素伤害加成", "冰元素伤害加成", "雷元素伤害加成", "风元素伤害加成", "量子伤害加成", "虚数伤害加成"],
    "连结绳": ["未选择", "生命值%", "攻击力%", "防御力%", "击破特攻", "能量恢复效率"]
}

# 添加仪器位置对应的概率
instrument_probabilities = {
    "未选择": {
        "probability": 1.0,
        "main_stats": {"未选择": 1.0}
    },
    "头部": {
        "probability": 0.25,
        "main_stats": {"生命值": 1.0}
    },
    "手部": {
        "probability": 0.25,
        "main_stats": {"攻击力": 1.0}
    },
    "躯干": {
        "probability": 0.25,
        "main_stats": {
            "未选择": 1.0,
            "生命值%": 0.2,
            "攻击力%": 0.2,
            "防御力%": 0.2,
            "暴击率": 0.1,
            "暴击伤害": 0.1,
            "治疗量加成": 0.1,
            "效果命中": 0.1
        }
    },
    "脚部": {
        "probability": 0.25,
        "main_stats": {
            "未选择": 1.0,
            "生命值%": 0.29167,
            "攻击力%": 0.29167,
            "防御力%": 0.29167,
            "速度": 0.125
        }
    },
    "连结绳": {
        "probability": 0.5,
        "main_stats": {
            "未选择": 1.0,
            "生命值%": 0.26333,
            "攻击力%": 0.26333,
            "防御力%": 0.26333,
            "击破特攻": 0.15,
            "能量恢复效率": 0.06
        }
    },
    "位面球": {
        "probability": 0.5,
        "main_stats": {
            "未选择": 1.0,
            "生命值%": 0.12333,
            "攻击力%": 0.12333,
            "防御力%": 0.12333,
            "物理伤害加成": 0.09,
            "火元素伤害加成": 0.09,
            "冰元素伤害加成": 0.09,
            "雷元素伤害加成": 0.09,
            "风元素伤害加成": 0.09,
            "量子伤害加成": 0.09,
            "虚数伤害加成": 0.09
        }
    }
}

# 副词条选项
sub_stat_options = ["生命值", "攻击力", "防御力", "生命值%", "攻击力%", "防御力%", "速度", "暴击率", "暴击伤害", "效果命中", "效果抵抗", "击破特攻"]

class RelicSimulator:
    def __init__(self):#初始化仪器模拟器，设置窗口、框架、控件并初始化默认值

        self.setup_window()
        self.setup_frames()
        self.setup_controls()
        self.sub_stat_frames = []
        self.initialize_default_values()

    def setup_window(self):
        """设置主窗口的基本属性，包括标题、大小和可调整性"""
        self.root = tk.Tk()
        self.root.title(UI_CONFIG['WINDOW_TITLE'])
        
        # 设置窗口大小并居中
        window_width = 800
        window_height = 600
        
        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 计算居中位置
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        self.root.resizable(True, True)
        
        # 添加窗口图标
        self.root.iconbitmap('图标.ico')

    def setup_frames(self):#设置主要框架布局，包括左侧控件区、分隔线和右侧计算结果区"""
        self.left_frame = tk.Frame(self.root)
        self.right_frame = tk.Frame(self.root)
        self.separator = tk.Frame(self.root, bg="gray", width=2)
        
        self.left_frame.pack(side="left", fill="y")
        self.separator.pack(side="left", fill="y")
        self.right_frame.pack(side="left", fill="both", expand=True)

    def create_combobox_with_label(self, parent, row, text, values, callback=None, show_checkbox=True):
        """创建带标签和复选框的下拉框组件
        Args:
            parent: 父级容器
            row: 行号
            text: 标签文本
            values: 下拉框选项列表
            callback: 下拉框选择事件回调函数
            show_checkbox: 是否显示复选框
        Returns:
            tuple: (下拉框对象, 复选框变量)
        """

        label = ttk.Label(parent, text=text)
        label.grid(row=row, column=0, pady=UI_CONFIG['PADDING_Y'], padx=UI_CONFIG['PADDING_X'], sticky=UI_CONFIG['STICKY_E'])
        
        combobox = ttk.Combobox(parent, values=values, width=UI_CONFIG['COMBOBOX_WIDTH'])
        combobox.grid(row=row, column=1, pady=UI_CONFIG['PADDING_Y'], padx=5, sticky=UI_CONFIG['STICKY_W'])
        
        if callback:
            combobox.bind("<<ComboboxSelected>>", callback)
        
        checkbox_var = None
        if show_checkbox:
            checkbox_var = tk.BooleanVar()
            
            def on_checkbox_click():
                pass
            
            checkbox = tk.Checkbutton(parent, variable=checkbox_var, command=on_checkbox_click)
            checkbox.grid(row=row, column=2, pady=UI_CONFIG['PADDING_Y'], padx=5, sticky=UI_CONFIG['STICKY_W'])
        
        return combobox, checkbox_var

    def setup_controls(self):
        # 设置仪器位置选择
        self.position_combobox, self.position_checkbox = self.create_combobox_with_label(
            self.left_frame, 0, "选择仪器位置:", 
            list(instrument_positions.keys()), 
            self.on_position_selected
        )

        # 设置主词条选择
        self.main_stat_combobox, self.main_stat_checkbox = self.create_combobox_with_label(
            self.left_frame, 1, "选择主词条:", 
            [], 
            self.on_main_stat_selected
        )

        # 设置初始词条数选择
        self.initial_stat_combobox, self.initial_stat_checkbox = self.create_combobox_with_label(
            self.left_frame, 2, "选择初始词条数:", 
            ["未选择", 3, 4], 
            self.on_initial_stat_selected
        )

        # 设置副词条数选择
        self.sub_stat_count_combobox, self.sub_stat_count_checkbox = self.create_combobox_with_label(
            self.left_frame, 3, "选择包含副词条数:", 
            list(range(0, 5)),  # 修改为0-4
            self.on_sub_stat_count_selected
        )

        # 设置按钮和计算结果区域
        self.setup_buttons_and_log()

    def start_simulation(self):
        # 获取所有复选框的状态
        checkboxes = [
            self.position_checkbox.get(),
            self.main_stat_checkbox.get(),
            self.initial_stat_checkbox.get(),
            self.sub_stat_count_checkbox.get()
        ]
        
        # 检查是否有复选框被勾选
        if not any(checkboxes):
            self.log_text.insert(tk.END, "请至少勾选一个作为刷取遗器的目标\n---------------------------------\n")
            self.log_text.see(tk.END)
            return
        
        # 生成二进制数
        binary_num = ''.join('1' if x else '0' for x in checkboxes)
        
        start_time = time.time()
        position = self.position_combobox.get()
        main_stat = self.main_stat_combobox.get()
        in_stat = self.initial_stat_combobox.get()
        sub_stats_count = self.sub_stat_count_combobox.get()  # 这行代码缺失了
        
        selected_sub_stats = [combobox.get() for _, combobox in self.sub_stat_frames if combobox.get()]
        # 添加初始词条数概率计算

        # 获取位置概率和主属性概率并计算总概率
        # 1.仪器位置初始概率
        position_prob: float = 1.0  
        if self.position_checkbox.get():  # 判断仪器位置复选框是否被勾选
            position_prob = float(instrument_probabilities[position]["probability"])
        # 2.主词条初始概率
        main_stat_prob: float = 1.0  
        if self.main_stat_checkbox.get():  # 判断主词条复选框是否被勾选
            main_stat_prob = float(instrument_probabilities[position]["main_stats"][main_stat])
        # 3.初始3/4词条概率
        initial_34_prob: float = 1.0
        if self.initial_stat_checkbox.get():#判断初始3/4副词条数是否被勾选
            if in_stat == "未选择":
                initial_34_prob = 1.0
            elif int(in_stat) == 3:
                initial_34_prob = 0.8
            elif int(in_stat) == 4:
                initial_34_prob = 0.2
        # 4.副词条词条初始概率
        initial_stat_prob: float = 100.0
        prob1: float = 1.0
        prob2: float = 1.0
        if self.sub_stat_count_checkbox.get():  # 判断副词条数复选框是否被勾选
            if in_stat == "未选择":  #初始词条为未选择时
                prob1 = float(sr_TreeNode.process_sub_stats(main_stat, selected_sub_stats, "3"))
                prob2 = float(sr_TreeNode.process_sub_stats(main_stat, selected_sub_stats, "4"))
                initial_stat_prob = prob1*0.8 + prob2*0.2
                print(f"副词条未选择计算过程： {prob1} * 0.8 + {prob2} * 0.2 = {initial_stat_prob}")
            else:
                initial_stat_prob = float(sr_TreeNode.process_sub_stats(main_stat, selected_sub_stats, in_stat))            

        result: float = position_prob * main_stat_prob * initial_34_prob * initial_stat_prob   # 将各个概率计入总概率
        #    总概率    =  仪器位置概率  *    主词条概率   *  初始3/4词条概率 *     副词条概率
        print(f"计算过程: {position_prob} * {main_stat_prob} * {initial_34_prob} * {initial_stat_prob} = {result}")
        elapsed_time = time.time() - start_time

        # 构建输出信息
        output_parts1 = ""  # 存放二进制数为0的部分
        output_parts2 = ""  # 存放二进制数为1的部分
        
        # 构建基础字符串
        position_str = f"的{self.position_combobox.get()}遗器"  # 修改为"的+仪器位置"
        main_stat_str = f"主词条为{main_stat}"
        initial_stat_str = f"初始词条数为{in_stat}"
        sub_stats_str = ""
        
        # 根据复选框状态分配字符串，仪器位置始终放在最后
        parts_list = []
        # 2.判断主词条
        if main_stat != "未选择":   #主词条不是未选择时
            if checkboxes[1]:  # 主词条勾选时
                output_parts2 += main_stat_str
            else:
                output_parts1 += (", " if output_parts1 else "") + main_stat_str
        # 3.判断初始词条数
        if in_stat != "未选择":   #初始词条数不是未选择时
            if checkboxes[2]:  # 初始词条数
                output_parts2 += (", " if output_parts2 else "") + initial_stat_str
            else:
                output_parts1 += (", " if output_parts1 else "") + initial_stat_str      
        # 4.判断副词条数   
        if sub_stats_count != "0":     #副词条数不是0
            sub_stats_str = f"副词条包含{', '.join(selected_sub_stats)}"
            if checkboxes[3]:  # 包含副词条勾选时
                output_parts2 += (", " if output_parts2 else "") + sub_stats_str
            else:
                output_parts1 += (", " if output_parts1 else "") + sub_stats_str
        #1.仪器位置判断            始终放在最后*****************************************************************************
        if position != "未选择":   #仪器位置不是未选择时
            
            if checkboxes[0]:
                output_parts2 += position_str
                # 判断是否为连结绳或位面球
                if position in ["连结绳", "位面球"]:
                    output_parts1 += "的内圈遗器"   # 其他位置属于内圈
                else:
                    output_parts1 += "的外圈遗器"   # 连结绳和位面球属于外圈
            else:
                output_parts1 += position_str   #没选
            

        log_message = (
            # f"{binary_num}\n平均需要刷取{1/result*100:.2f}个"
            f"平均需要刷取{1/result*100:.2f}个"
            f"{output_parts1}{'，' if output_parts1 else ''}"
            f"才能获取到"
            f"{output_parts2}\n"
            f"概率为: {result:.4g}%\n"
            # f"时间: {elapsed_time:.2f}s\n"
            f"---------------------------------\n"
        )
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)

    def setup_buttons_and_log(self):
        button_frame = tk.Frame(self.right_frame)
        button_frame.pack(pady=10, padx=10, anchor="w")

        start_button = ttk.Button(button_frame, text="计算", command=self.start_simulation)
        start_button.pack(side=tk.LEFT, padx=10)

        preset_button = ttk.Button(button_frame, text="清除", command=self.preset_1)
        preset_button.pack(side=tk.LEFT, padx=10)

        log_label = ttk.Label(self.right_frame, text="计算结果:")
        log_label.pack(padx=10, anchor="w")

        # 创建一个带滚动条的框架
        log_frame = tk.Frame(self.right_frame)
        log_frame.pack(padx=(10,0), fill="both", expand=True)

        # 创建滚动条
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 创建文本框并关联滚动条
        self.log_text = tk.Text(log_frame, yscrollcommand=scrollbar.set)
        self.log_text.pack(side=tk.LEFT, fill="both", expand=True)
        
        # 设置滚动条的命令
        scrollbar.config(command=self.log_text.yview)

    def initialize_default_values(self):
        self.position_combobox.set(list(instrument_positions.keys())[0])
        self.initial_stat_combobox.set("未选择")  # 修改默认值为"未选择"
        self.sub_stat_count_combobox.set(0)
        self.on_position_selected(None)

    def update_sub_stats(self):
        main_stat = self.main_stat_combobox.get()
        filtered_options = [opt for opt in sub_stat_options if opt != main_stat]
        selected_stats = [combobox.get() for _, combobox in self.sub_stat_frames if combobox.get()]

        for _, combobox in self.sub_stat_frames:
            current = combobox.get()
            available = [opt for opt in filtered_options if opt not in selected_stats or opt == current]
            combobox['values'] = available

    def create_sub_stat_controls(self, count):
        # 清除现有的副词条控件和标签
        for frame, combobox in self.sub_stat_frames:
            if frame is not None:
                frame.destroy()
            if combobox is not None:
                combobox.destroy()
        
        # 清除可能存在的额外标签
        for widget in self.left_frame.grid_slaves():
            if isinstance(widget, ttk.Label) and widget.grid_info()['row'] >= 4:
                widget.destroy()
            elif isinstance(widget, ttk.Combobox) and widget.grid_info()['row'] >= 4:
                widget.destroy()
                
        self.sub_stat_frames.clear()

        # 创建新的副词条控件
        main_stat = self.main_stat_combobox.get()
        filtered_options = [opt for opt in sub_stat_options if opt != main_stat]

        for i in range(count):
            # 创建标签
            label = ttk.Label(self.left_frame, text=f"副词条{i + 1}:")
            label.grid(row=4 + i, column=0, pady=UI_CONFIG['PADDING_Y'], padx=UI_CONFIG['PADDING_X'], sticky=UI_CONFIG['STICKY_E'])
            
            # 创建下拉框
            combobox = ttk.Combobox(self.left_frame, values=filtered_options, width=UI_CONFIG['COMBOBOX_WIDTH'])
            combobox.grid(row=4 + i, column=1, pady=UI_CONFIG['PADDING_Y'], padx=5, sticky=UI_CONFIG['STICKY_W'])
            combobox.set(filtered_options[min(i, len(filtered_options)-1)])
            combobox.bind("<<ComboboxSelected>>", lambda e: self.update_sub_stats())
            
            # 将frame和combobox添加到列表中
            self.sub_stat_frames.append((None, combobox))

        self.update_sub_stats()

    def on_position_selected(self, event):
        selected_position = self.position_combobox.get()
        self.main_stat_combobox['values'] = instrument_positions[selected_position]
        self.main_stat_combobox.set(instrument_positions[selected_position][0])
        self.on_sub_stat_count_selected(None)

    def on_main_stat_selected(self, event):
        self.on_sub_stat_count_selected(None)

    def on_initial_stat_selected(self, event):
        """初始词条数选择事件处理函数，更新副词条数的可选范围"""
        initial_stat = self.initial_stat_combobox.get()
        if initial_stat == "未选择":
            self.sub_stat_count_combobox['values'] = list(range(0, 5))  # 设置为0-4
            if int(self.sub_stat_count_combobox.get()) > 4:
                self.sub_stat_count_combobox.set(1)
        else:
            initial_count = int(initial_stat)
            self.sub_stat_count_combobox['values'] = list(range(0, initial_count + 1))
            
            if initial_count < int(self.sub_stat_count_combobox.get()):
                self.sub_stat_count_combobox.set(1)
        self.on_sub_stat_count_selected(None)

    def on_sub_stat_count_selected(self, event):
        count = int(self.sub_stat_count_combobox.get())
        self.create_sub_stat_controls(count)

    def preset_1(self):
        # 清除计算结果文本框内容
        self.log_text.delete(1.0, tk.END)
        # 预设
        # self.position_combobox.set("连结绳")
        # self.on_position_selected(None)
        # self.main_stat_combobox.set("能量恢复效率")
        # self.initial_stat_combobox.set(4)
        # self.sub_stat_count_combobox.set(2)
        # self.on_sub_stat_count_selected(None)
        
        # if len(self.sub_stat_frames) > 0:
        #     self.sub_stat_frames[0][1].set("暴击率")
        # if len(self.sub_stat_frames) > 1:
        #     self.sub_stat_frames[1][1].set("暴击伤害")
        
        # self.update_sub_stats()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RelicSimulator()
    app.run()