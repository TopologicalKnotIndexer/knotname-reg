import os
import re

class AmphichiralChecker:
    def __init__(self) -> None: # 用于从名字集合中消弭事实上的非手性扭结的 m 前缀
        pass                    # 必要时需要对名字重新按照字典序排序
        self.name1_to_name2        = {}
        self.dir_now               = os.path.dirname(os.path.abspath(__file__))
        self.data_dir              = os.path.join(self.dir_now, "data")
        self.name_pair_file        = os.path.join(self.data_dir, "name_pair.txt")
        self.amphichiral_list_file = os.path.join(self.data_dir, "amphichiral_list.txt")
        self.amphichiral_list      = []
        self.load_name_pair_file()
        self.load_amphichiral_list_file()

    def load_amphichiral_list_file(self): # 这里拿到的都是 name2
        for line in open(self.amphichiral_list_file):
            line = line.strip()
            if line == "": continue
            self.amphichiral_list.append(line)

    def load_name_pair_file(self): # 构造一个部分正确的名字映射
        for line in open(self.name_pair_file):
            line = line.strip()
            if line == "": continue
            n2, n1 = [x.strip() for x in line.split()]
            self.name1_to_name2[n1] = n2

    def is_amphichiral_prime(self, raw_prime_name: str) -> bool:
        raw_prime_name = raw_prime_name.lower().replace("k", "K")               # 检查一个素扭结是否 “一定是” 非手性的
        if self.name1_to_name2.get(raw_prime_name) is not None:
            return self.name1_to_name2[raw_prime_name] in self.amphichiral_list # 如果你不想做任何筛查，那就返回 False，这对程序的正确性没有影响
        else:
            return False # 对于较大扭结拒绝判断，直接假设他是手性的

    def is_prime_knot_name_format(self, knotname: str) -> bool: # 检查标准素扭结的名称格式
        return re.match("^(m|)k\d+(a|n)\d+$", knotname.lower()) is not None

    def simplify_prime_name(self, prime_name: str):
        assert self.is_prime_knot_name_format(prime_name)
        raw_name = prime_name[1:] if prime_name[0] == 'm' else prime_name # 如果 m 存在，则删除掉 m

        if self.is_amphichiral_prime(raw_name): # 对于非手性，返回去掉 m 之后的结果
            return raw_name
        else:
            return prime_name

    def simplify_knot_name(self, knot_name: str) -> str:
        assert isinstance(knot_name, str)
        if knot_name.find(',') == -1:
            return self.simplify_prime_name(knot_name) # 本身就是素扭结
        arr = []
        for prime_name in knot_name.split(','): # 本身不是素扭结
            arr.append(self.simplify_prime_name(prime_name.strip()))
        return ",".join(sorted(arr))

    def erase_m_if_possible(self, knot_name_list: list):
        assert isinstance(knot_name_list, list)
        arr = []
        for knot_name in knot_name_list:
            arr.append(self.simplify_knot_name(knot_name))
        return sorted(list(set(arr)))

def knotname_reg(knot_name: str) -> str: # 对扭结名称进行正则化，考虑非手性扭结的命名重复
    amp_checker = AmphichiralChecker()
    return amp_checker.simplify_knot_name(knot_name).replace("k", "K")

if __name__ == "__main__": # 测试
    print(knotname_reg("mk6a3,mk4a1"))