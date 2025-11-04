"""
S-AES (Simplified Advanced Encryption Standard) 实现
支持基本加解密、ASCII字符串加解密、多重加密和CBC模式
"""


class SAES:
    def __init__(self):
        #S盒
        self.S_BOX = [
            [0x9, 0x4, 0xA, 0xB],
            [0xD, 0x1, 0x8, 0x5],
            [0x6, 0x2, 0x0, 0x3],
            [0xC, 0xE, 0xF, 0x7]
        ]

        self.INV_S_BOX = [
            [0xA, 0x5, 0x9, 0xB],
            [0x1, 0x7, 0x8, 0xF],
            [0x6, 0x0, 0x2, 0x3],
            [0xC, 0x4, 0xD, 0xE]
        ]

        # 列混淆矩阵
        self.MIX_MATRIX = [
            [1, 4],
            [4, 1]
        ]

        self.INV_MIX_MATRIX = [
            [9, 2],
            [2, 9]
        ]

        # 轮常量
        self.RCON = [0x80, 0x30]

        # GF(2^4)乘法查找表
        self.GF_MULT_TABLE = {
            (0, 0): 0, (0, 1): 0, (0, 2): 0, (0, 3): 0, (0, 4): 0, (0, 5): 0, (0, 6): 0, (0, 7): 0, (0, 8): 0,
            (0, 9): 0, (0, 10): 0, (0, 11): 0, (0, 12): 0, (0, 13): 0, (0, 14): 0, (0, 15): 0,
            (1, 0): 0, (1, 1): 1, (1, 2): 2, (1, 3): 3, (1, 4): 4, (1, 5): 5, (1, 6): 6, (1, 7): 7, (1, 8): 8,
            (1, 9): 9, (1, 10): 10, (1, 11): 11, (1, 12): 12, (1, 13): 13, (1, 14): 14, (1, 15): 15,
            (2, 0): 0, (2, 1): 2, (2, 2): 4, (2, 3): 6, (2, 4): 8, (2, 5): 10, (2, 6): 12, (2, 7): 14, (2, 8): 3,
            (2, 9): 1, (2, 10): 7, (2, 11): 5, (2, 12): 11, (2, 13): 9, (2, 14): 15, (2, 15): 13,
            (3, 0): 0, (3, 1): 3, (3, 2): 6, (3, 3): 5, (3, 4): 12, (3, 5): 15, (3, 6): 10, (3, 7): 9, (3, 8): 11,
            (3, 9): 8, (3, 10): 13, (3, 11): 14, (3, 12): 7, (3, 13): 4, (3, 14): 1, (3, 15): 2,
            (4, 0): 0, (4, 1): 4, (4, 2): 8, (4, 3): 12, (4, 4): 3, (4, 5): 7, (4, 6): 11, (4, 7): 15, (4, 8): 6,
            (4, 9): 2, (4, 10): 14, (4, 11): 10, (4, 12): 5, (4, 13): 1, (4, 14): 13, (4, 15): 9,
            (5, 0): 0, (5, 1): 5, (5, 2): 10, (5, 3): 15, (5, 4): 7, (5, 5): 2, (5, 6): 13, (5, 7): 8, (5, 8): 14,
            (5, 9): 11, (5, 10): 4, (5, 11): 1, (5, 12): 9, (5, 13): 12, (5, 14): 3, (5, 15): 6,
            (6, 0): 0, (6, 1): 6, (6, 2): 12, (6, 3): 10, (6, 4): 11, (6, 5): 13, (6, 6): 7, (6, 7): 1, (6, 8): 5,
            (6, 9): 3, (6, 10): 9, (6, 11): 15, (6, 12): 14, (6, 13): 8, (6, 14): 2, (6, 15): 4,
            (7, 0): 0, (7, 1): 7, (7, 2): 14, (7, 3): 9, (7, 4): 15, (7, 5): 8, (7, 6): 1, (7, 7): 6, (7, 8): 13,
            (7, 9): 10, (7, 10): 3, (7, 11): 4, (7, 12): 2, (7, 13): 5, (7, 14): 12, (7, 15): 11,
            (8, 0): 0, (8, 1): 8, (8, 2): 3, (8, 3): 11, (8, 4): 6, (8, 5): 14, (8, 6): 5, (8, 7): 13, (8, 8): 12,
            (8, 9): 4, (8, 10): 15, (8, 11): 7, (8, 12): 10, (8, 13): 2, (8, 14): 9, (8, 15): 1,
            (9, 0): 0, (9, 1): 9, (9, 2): 1, (9, 3): 8, (9, 4): 2, (9, 5): 11, (9, 6): 3, (9, 7): 10, (9, 8): 4,
            (9, 9): 13, (9, 10): 5, (9, 11): 12, (9, 12): 6, (9, 13): 15, (9, 14): 7, (9, 15): 14,
            (10, 0): 0, (10, 1): 10, (10, 2): 7, (10, 3): 13, (10, 4): 14, (10, 5): 4, (10, 6): 9, (10, 7): 3,
            (10, 8): 15, (10, 9): 5, (10, 10): 8, (10, 11): 2, (10, 12): 1, (10, 13): 11, (10, 14): 6, (10, 15): 12,
            (11, 0): 0, (11, 1): 11, (11, 2): 5, (11, 3): 14, (11, 4): 10, (11, 5): 1, (11, 6): 15, (11, 7): 4,
            (11, 8): 7, (11, 9): 12, (11, 10): 2, (11, 11): 9, (11, 12): 13, (11, 13): 6, (11, 14): 8, (11, 15): 3,
            (12, 0): 0, (12, 1): 12, (12, 2): 11, (12, 3): 7, (12, 4): 5, (12, 5): 9, (12, 6): 14, (12, 7): 2,
            (12, 8): 10, (12, 9): 6, (12, 10): 1, (12, 11): 13, (12, 12): 15, (12, 13): 3, (12, 14): 4, (12, 15): 8,
            (13, 0): 0, (13, 1): 13, (13, 2): 9, (13, 3): 4, (13, 4): 1, (13, 5): 12, (13, 6): 8, (13, 7): 5,
            (13, 8): 2, (13, 9): 15, (13, 10): 11, (13, 11): 6, (13, 12): 3, (13, 13): 14, (13, 14): 10, (13, 15): 7,
            (14, 0): 0, (14, 1): 14, (14, 2): 15, (14, 3): 1, (14, 4): 13, (14, 5): 3, (14, 6): 2, (14, 7): 12,
            (14, 8): 9, (14, 9): 7, (14, 10): 6, (14, 11): 8, (14, 12): 4, (14, 13): 10, (14, 14): 11, (14, 15): 5,
            (15, 0): 0, (15, 1): 15, (15, 2): 13, (15, 3): 2, (15, 4): 9, (15, 5): 6, (15, 6): 4, (15, 7): 11,
            (15, 8): 1, (15, 9): 14, (15, 10): 12, (15, 11): 3, (15, 12): 8, (15, 13): 7, (15, 14): 5, (15, 15): 10
        }

    def gf_mult(self, a, b):
        """在GF(2^4)上的乘法 - 使用查找表"""
        return self.GF_MULT_TABLE.get((a, b), 0)

    def sub_nibbles(self, state, inverse=False):
        """半字节替换"""
        s_box = self.INV_S_BOX if inverse else self.S_BOX
        result = 0

        # 提取4个半字节
        nibbles = []
        for i in range(4):
            nibble = (state >> (4 * (3 - i))) & 0xF
            nibbles.append(nibble)

        # 应用S盒替换
        for i, nibble in enumerate(nibbles):
            row = (nibble >> 2) & 0x3
            col = nibble & 0x3
            sub_nibble = s_box[row][col]
            result |= (sub_nibble << (4 * (3 - i)))

        return result

    def shift_rows(self, state):
        """行移位 - 第二行循环左移1个半字节"""
        # 将状态视为2x2的半字节矩阵
        # 位置: [0,0] [0,1]
        #       [1,0] [1,1]

        # 提取半字节
        n00 = (state >> 12) & 0xF  # 第一个半字节
        n01 = (state >> 8) & 0xF  # 第二个半字节
        n10 = (state >> 4) & 0xF  # 第三个半字节
        n11 = state & 0xF  # 第四个半字节

        # 第二行循环左移：交换n10和n11
        n10, n11 = n11, n10

        # 重新组合
        result = (n00 << 12) | (n01 << 8) | (n10 << 4) | n11
        return result

    def mix_columns(self, state, inverse=False):
        """列混淆"""
        matrix = self.INV_MIX_MATRIX if inverse else self.MIX_MATRIX

        # 将状态视为2x2的半字节矩阵
        s00 = (state >> 12) & 0xF  # 第一行第一列
        s01 = (state >> 8) & 0xF  # 第一行第二列
        s10 = (state >> 4) & 0xF  # 第二行第一列
        s11 = state & 0xF  # 第二行第二列

        # 矩阵乘法在GF(2^4)上
        new_s00 = self.gf_mult(matrix[0][0], s00) ^ self.gf_mult(matrix[0][1], s10)
        new_s01 = self.gf_mult(matrix[0][0], s01) ^ self.gf_mult(matrix[0][1], s11)
        new_s10 = self.gf_mult(matrix[1][0], s00) ^ self.gf_mult(matrix[1][1], s10)
        new_s11 = self.gf_mult(matrix[1][0], s01) ^ self.gf_mult(matrix[1][1], s11)

        # 重新组合
        result = (new_s00 << 12) | (new_s01 << 8) | (new_s10 << 4) | new_s11
        return result

    def sub_word(self, word):
        """对8位字（2个半字节）进行S盒替换 - 用于密钥扩展"""
        # 提取高4位和低4位
        high_nibble = (word >> 4) & 0xF
        low_nibble = word & 0xF
        
        # 应用S盒替换
        row_high = (high_nibble >> 2) & 0x3
        col_high = high_nibble & 0x3
        sub_high = self.S_BOX[row_high][col_high]
        
        row_low = (low_nibble >> 2) & 0x3
        col_low = low_nibble & 0x3
        sub_low = self.S_BOX[row_low][col_low]
        
        # 重新组合
        return (sub_high << 4) | sub_low
    
    def rot_nib(self, word):
        """半字节循环移位 - 用于密钥扩展"""
        # 将8位字分为2个半字节并交换
        high_nibble = (word >> 4) & 0xF
        low_nibble = word & 0xF
        return (low_nibble << 4) | high_nibble

    def key_expansion(self, key):
        """密钥扩展"""
        # 将16位密钥分为2个8位字
        w0 = (key >> 8) & 0xFF
        w1 = key & 0xFF

        # 计算w2 = w0 ⊕ g(w1)
        # g(w) = RCON(i) ⊕ SubWord(RotNib(w))
        g_w1 = self.RCON[0] ^ self.sub_word(self.rot_nib(w1))
        w2 = w0 ^ g_w1

        # w3 = w2 ⊕ w1
        w3 = w2 ^ w1

        # 计算w4 = w2 ⊕ g(w3)
        g_w3 = self.RCON[1] ^ self.sub_word(self.rot_nib(w3))
        w4 = w2 ^ g_w3

        # w5 = w4 ⊕ w3
        w5 = w4 ^ w3

        # 组合成轮密钥
        k0 = (w0 << 8) | w1  # 初始轮密钥
        k1 = (w2 << 8) | w3  # 第一轮密钥
        k2 = (w4 << 8) | w5  # 第二轮密钥

        return [k0, k1, k2]

    def add_round_key(self, state, round_key):
        """轮密钥加"""
        return state ^ round_key

    def encrypt(self, plaintext, key):
        """加密函数"""
        keys = self.key_expansion(key)

        # 第0轮：初始轮密钥加
        state = self.add_round_key(plaintext, keys[0])

        # 第1轮：完整轮
        state = self.sub_nibbles(state)  # 半字节替换
        state = self.shift_rows(state)  # 行移位
        state = self.mix_columns(state)  # 列混淆
        state = self.add_round_key(state, keys[1])  # 轮密钥加

        # 第2轮：简化轮（无列混淆）
        state = self.sub_nibbles(state)  # 半字节替换
        state = self.shift_rows(state)  # 行移位
        state = self.add_round_key(state, keys[2])  # 轮密钥加

        return state

    def decrypt(self, ciphertext, key):
        """解密函数 - 加密的逆"""
        keys = self.key_expansion(key)

        # 第2轮逆
        state = self.add_round_key(ciphertext, keys[2])  # 轮密钥加
        state = self.shift_rows(state)  # 逆行移位
        state = self.sub_nibbles(state, inverse=True)  # 逆半字节替换

        # 第1轮逆
        state = self.add_round_key(state, keys[1])  # 轮密钥加
        state = self.mix_columns(state, inverse=True)  # 逆列混淆
        state = self.shift_rows(state)  # 逆行移位
        state = self.sub_nibbles(state, inverse=True)  # 逆半字节替换

        # 第0轮逆
        state = self.add_round_key(state, keys[0])  # 轮密钥加

        return state

    # ============== 第3关：ASCII字符串加解密 ==============
    
    def encrypt_ascii(self, plaintext_str, key):
        """
        ASCII字符串加密
        将字符串按2字节分组进行加密
        """
        # 将字符串转换为字节
        plaintext_bytes = plaintext_str.encode('utf-8')
        ciphertext_blocks = []
        
        # 按2字节分组加密
        for i in range(0, len(plaintext_bytes), 2):
            # 获取2字节数据
            if i + 1 < len(plaintext_bytes):
                block = (plaintext_bytes[i] << 8) | plaintext_bytes[i + 1]
            else:
                # 如果是奇数个字节，最后一个字节补0
                block = (plaintext_bytes[i] << 8)
            
            # 加密这个块
            encrypted_block = self.encrypt(block, key)
            ciphertext_blocks.append(encrypted_block)
        
        return ciphertext_blocks
    
    def decrypt_ascii(self, ciphertext_blocks, key):
        """
        ASCII字符串解密
        将密文块解密并转换回字符串
        """
        plaintext_bytes = []
        
        for block in ciphertext_blocks:
            # 解密块
            decrypted_block = self.decrypt(block, key)
            
            # 提取2个字节
            byte1 = (decrypted_block >> 8) & 0xFF
            byte2 = decrypted_block & 0xFF
            
            plaintext_bytes.append(byte1)
            if byte2 != 0:  # 如果第二个字节不是填充的0
                plaintext_bytes.append(byte2)
        
        # 转换回字符串
        try:
            return bytes(plaintext_bytes).decode('utf-8')
        except UnicodeDecodeError:
            # 如果无法解码为UTF-8，返回原始字节的十六进制表示
            return ' '.join([f"{b:02X}" for b in plaintext_bytes])

    # ============== 第4关：多重加密 ==============
    
    def double_encrypt(self, plaintext, key1, key2):
        """
        双重加密：E_K2(E_K1(P))
        使用两个16位密钥进行双重加密
        """
        temp = self.encrypt(plaintext, key1)
        ciphertext = self.encrypt(temp, key2)
        return ciphertext
    
    def double_decrypt(self, ciphertext, key1, key2):
        """
        双重解密：D_K1(D_K2(C))
        """
        temp = self.decrypt(ciphertext, key2)
        plaintext = self.decrypt(temp, key1)
        return plaintext
    
    def meet_in_middle_attack(self, plaintext, ciphertext):
        """
        中间相遇攻击
        给定明文-密文对，尝试找到密钥对(K1, K2)
        返回所有可能的密钥对列表
        """
        # 建立中间值字典：存储 E_K1(P) -> K1 的映射
        middle_values = {}
        
        print("开始中间相遇攻击...")
        print(f"明文: {plaintext:04X}, 密文: {ciphertext:04X}")
        
        # 第一阶段：对所有可能的K1，计算E_K1(P)
        for k1 in range(0x10000):  # 遍历所有16位密钥
            middle = self.encrypt(plaintext, k1)
            if middle not in middle_values:
                middle_values[middle] = []
            middle_values[middle].append(k1)
            
            if k1 % 0x1000 == 0:
                print(f"阶段1进度: {k1/0x10000*100:.1f}%")
        
        # 第二阶段：对所有可能的K2，计算D_K2(C)并查找匹配
        possible_keys = []
        for k2 in range(0x10000):  # 遍历所有16位密钥
            middle = self.decrypt(ciphertext, k2)
            if middle in middle_values:
                # 找到匹配的中间值
                for k1 in middle_values[middle]:
                    possible_keys.append((k1, k2))
            
            if k2 % 0x1000 == 0:
                print(f"阶段2进度: {k2/0x10000*100:.1f}%")
        
        print(f"找到 {len(possible_keys)} 个可能的密钥对")
        return possible_keys
    
    def triple_encrypt_32bit(self, plaintext, key1, key2):
        """
        三重加密（32位密钥模式）：E_K1(D_K2(E_K1(P)))
        使用EDE模式
        """
        temp1 = self.encrypt(plaintext, key1)
        temp2 = self.decrypt(temp1, key2)
        ciphertext = self.encrypt(temp2, key1)
        return ciphertext
    
    def triple_decrypt_32bit(self, ciphertext, key1, key2):
        """
        三重解密（32位密钥模式）：D_K1(E_K2(D_K1(C)))
        """
        temp1 = self.decrypt(ciphertext, key1)
        temp2 = self.encrypt(temp1, key2)
        plaintext = self.decrypt(temp2, key1)
        return plaintext
    
    def triple_encrypt_48bit(self, plaintext, key1, key2, key3):
        """
        三重加密（48位密钥模式）：E_K3(D_K2(E_K1(P)))
        使用三个独立的密钥
        """
        temp1 = self.encrypt(plaintext, key1)
        temp2 = self.decrypt(temp1, key2)
        ciphertext = self.encrypt(temp2, key3)
        return ciphertext
    
    def triple_decrypt_48bit(self, ciphertext, key1, key2, key3):
        """
        三重解密（48位密钥模式）：D_K1(E_K2(D_K3(C)))
        """
        temp1 = self.decrypt(ciphertext, key3)
        temp2 = self.encrypt(temp1, key2)
        plaintext = self.decrypt(temp2, key1)
        return plaintext

    # ============== 第5关：CBC模式 ==============
    
    def cbc_encrypt(self, plaintext_blocks, key, iv):
        """
        CBC模式加密
        plaintext_blocks: 明文块列表（每个块16位）
        key: 16位密钥
        iv: 16位初始向量
        返回: 密文块列表
        """
        ciphertext_blocks = []
        previous_block = iv
        
        for plaintext_block in plaintext_blocks:
            # XOR当前明文块与前一个密文块（或IV）
            xor_result = plaintext_block ^ previous_block
            # 加密XOR结果
            ciphertext_block = self.encrypt(xor_result, key)
            ciphertext_blocks.append(ciphertext_block)
            # 更新前一个密文块
            previous_block = ciphertext_block
        
        return ciphertext_blocks
    
    def cbc_decrypt(self, ciphertext_blocks, key, iv):
        """
        CBC模式解密
        ciphertext_blocks: 密文块列表（每个块16位）
        key: 16位密钥
        iv: 16位初始向量
        返回: 明文块列表
        """
        plaintext_blocks = []
        previous_block = iv
        
        for ciphertext_block in ciphertext_blocks:
            # 解密密文块
            decrypted_block = self.decrypt(ciphertext_block, key)
            # XOR解密结果与前一个密文块（或IV）
            plaintext_block = decrypted_block ^ previous_block
            plaintext_blocks.append(plaintext_block)
            # 更新前一个密文块
            previous_block = ciphertext_block
        
        return plaintext_blocks
    
    def string_to_blocks(self, text):
        """
        将字符串转换为16位块列表
        """
        text_bytes = text.encode('utf-8')
        blocks = []
        
        for i in range(0, len(text_bytes), 2):
            if i + 1 < len(text_bytes):
                block = (text_bytes[i] << 8) | text_bytes[i + 1]
            else:
                # 奇数个字节时，最后一个字节后补0
                block = (text_bytes[i] << 8)
            blocks.append(block)
        
        return blocks
    
    def blocks_to_string(self, blocks):
        """
        将16位块列表转换为字符串
        """
        text_bytes = []
        
        for block in blocks:
            byte1 = (block >> 8) & 0xFF
            byte2 = block & 0xFF
            text_bytes.append(byte1)
            if byte2 != 0:
                text_bytes.append(byte2)
        
        try:
            return bytes(text_bytes).decode('utf-8')
        except UnicodeDecodeError:
            return ' '.join([f"{b:02X}" for b in text_bytes])


