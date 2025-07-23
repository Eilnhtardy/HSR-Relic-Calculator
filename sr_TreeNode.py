initial_data = {
    "生命值": 5,
    "攻击力": 5,
    "防御力": 5,
    "生命值%": 5,
    "攻击力%": 5,
    "防御力%": 5,
    "速度": 2,
    "暴击率": 3,
    "暴击伤害": 3,
    "效果命中": 4,
    "效果抵抗": 4,
    "击破特攻": 4
}
class TreeNode:
    def __init__(self, node_id, data: dict, level: int, prob: float = 1.0):
        """
        node_id: 当前结点的编号。根结点编号为0；对于非根结点，为父节点字典中按插入顺序的第 k 个关键字
        data: 存放的字典
        level: 当前结点的层数，根结点层数为1
        prob: 当前结点的概率，根结点默认为1，其它子结点根据父结点计算
        """
        self.node_id = node_id     
        self.data = data           
        self.level = level         
        self.prob = prob           
        self.children = []         

    def __repr__(self): 
        return (f"TreeNode(id={self.node_id}, level={self.level}, "
                f"prob={self.prob:.4f}, keys={list(self.data.keys())})")



def get_child_data(parent_data: dict, k: int) -> dict:
    """
    返回一个新字典，其内容为父字典去掉按插入顺序排序后的第 k 个关键字对应的键值对。
    parent_data: 父字典
    k: 要删除的关键字索引(1-based)
    return: 新字典
    """
    keys = list(parent_data.keys())
    # k从1开始，删除索引为 k-1 的键值对
    new_data = {key: parent_data[key] for i, key in enumerate(keys) if i != k - 1}
    return new_data

# 修改 build_tree 函数，调整参数顺序，去掉 root_key_count 默认值
def build_tree(node: TreeNode, root_key_count: int, max_level: int = 5) -> None:
    """
    递归构建树形结构，直到达到最大层数。  
    第 i 层的每个结点有 (头结点字典关键词个数) - (i - 1) 个子结点，  
    子结点的概率由公式计算：  
      child_prob = 父节点.prob * (父节点.data 中第 child.node_id 对应的值) ÷ (父节点.data 所有值和)
    注意：非根结点的 node_id 为父节点字典中对应位置的关键字。
    node: 当前结点
    root_key_count: 头结点字典关键词的总数
    max_level: 最大层数
    """
    if node.level >= max_level:
        return

    # 使用传入的 root_key_count 参数
    num_children = root_key_count - (node.level - 1)
    parent_total = sum(node.data.values())
    keys = list(node.data.keys())
    for k in range(1, num_children + 1):
        # 非根结点的编号为父节点字典中按插入顺序的第 k 个关键字
        child_id = keys[k - 1]
        weight = node.data[child_id] / parent_total
        child_prob = node.prob * weight

        child_data = get_child_data(node.data, k)
        child_node = TreeNode(node_id=child_id, data=child_data, level=node.level + 1, prob=child_prob)
        node.children.append(child_node)

        build_tree(child_node,root_key_count, max_level)

count=1
def traverse_level_5(node: TreeNode):
    """
    递归遍历树，只处理层数为 5 的结点
    """
    global count
    if node.level == 5:
        print(count,node)
        count+=1
    else:
        for child in node.children:
            traverse_level_5(child)


def process_sub_stats(main_stat: str, sub_stat: list,in_stat):
    # 主词条main_stat，副词条列表sub_stat，初始词条的数量in_stat(3或4)
    # 新建一个头结点字典，去除关键字为 main_stat 的键值对
    new_dict = {key: value for key, value in initial_data.items() if key != main_stat}
    # 新建一个列表，是 initial_data 的关键字去除 sub_stat 和 main_stat 中的关键字后的结果
    new_list = [key for key in initial_data.keys() if key not in sub_stat and key != main_stat]
    # 创建根结点，编号设为 0，层数为 1，概率为 1.0
    root = TreeNode(node_id=0, data=new_dict, level=1, prob=1.0)
    # 构建树（此处最大层数设置为 5，可根据需要调整）
    build_tree(root, len(new_dict), max_level=5)
    print("初始",in_stat,"词条")
    # 在函数外部定义全局变量
    global j
    j = 0  # 初始化全局变量
    
    if in_stat=="4":
        def traverse_and_sum(node):
            global j  # 声明使用全局变量
            total_prob = 0
            if node.level == 5:
                node_keys = list(node.data.keys())
                if set(node_keys).issubset(set(new_list)):
                    # j += 1
                    # print(j,node)
                    total_prob += node.prob
            else:
                for child in node.children:
                    total_prob += traverse_and_sum(child)
            return total_prob
    else:  #初始三词条
        def traverse_and_sum(node):
            global j  # 同样声明使用全局变量
            total_prob = 0
            if node.level == 4:
                node_keys = list(node.data.keys())
                if set(node_keys).issubset(set(new_list)):
                    # j+=1;
                    # print(j,node)
                    total_prob += node.prob
            else:
                for child in node.children:
                    total_prob += traverse_and_sum(child)
            return total_prob
    # 遍历树的第五层，筛选符合条件的结点并求和


    total_prob = traverse_and_sum(root) * 100
    # 修改输出格式为百分比且保留 3 位小数
    print(f"筛选出的结点的 prob 总和为: {total_prob:.3f}%")
    return total_prob

if __name__ == "__main__":
    # process_sub_stats("能量恢复效率", [ "暴击率","暴击伤害"],"4") #结果为4.96%
    root = TreeNode(node_id=0, data=initial_data, level=1, prob=1.0)# 构建树（此处最大层数设置为 5，可根据需要调整）
    build_tree(root, len(initial_data), max_level=5)
    # print("----------")
    # process_sub_stats("能量恢复效率", ['速度'],"4") #结果为
    # print("----------")
    # process_sub_stats("能量恢复效率", [ "暴击率","暴击伤害"],"4") #结果为4.96%
    traverse_level_5(root)
    



