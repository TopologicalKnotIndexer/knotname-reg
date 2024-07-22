# 假设输入的扭结名称是合法的扭结名称
# 从标准输入读入全部内容作为扭结名称，输出正则化后的版本到标准输出

import sys
from AmphichiralChecker import knotname_reg

def main():
    input_data = sys.stdin.read().strip() # 输入一个扭结名称
    print(knotname_reg(input_data))       # 输出正则化之后的版本

if __name__ == "__main__":
    main()