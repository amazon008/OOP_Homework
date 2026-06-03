class LogicCoTuong:
    def __init__(self):
        self.ban_co = [
            ['bX', 'bM', 'bT', 'bS', 'bK', 'bS', 'bT', 'bM', 'bX'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', 'bP', '--', '--', '--', '--', '--', 'bP', '--'],
            ['bC', '--', 'bC', '--', 'bC', '--', 'bC', '--', 'bC'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['rC', '--', 'rC', '--', 'rC', '--', 'rC', '--', 'rC'],
            ['--', 'rP', '--', '--', '--', '--', '--', 'rP', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['rX', 'rM', 'rT', 'rS', 'rK', 'rS', 'rT', 'rM', 'rX']
        ]
        self.luot_di = "Do"

    def kiem_tra_luat_xe(self, hang_cu, cot_cu, hang_moi, cot_moi):
        if hang_cu != hang_moi and cot_cu != cot_moi: return False 
        if hang_cu == hang_moi: 
            for c in range(min(cot_cu, cot_moi) + 1, max(cot_cu, cot_moi)):
                if self.ban_co[hang_cu][c] != '--': return False
        else: 
            for h in range(min(hang_cu, hang_moi) + 1, max(hang_cu, hang_moi)):
                if self.ban_co[h][cot_cu] != '--': return False
        return True

    def kiem_tra_luat_ma(self, hang_cu, cot_cu, hang_moi, cot_moi):
        d_hang = hang_moi - hang_cu
        d_cot = cot_moi - cot_cu
        if (abs(d_hang) == 2 and abs(d_cot) == 1) or (abs(d_hang) == 1 and abs(d_cot) == 2):
            if abs(d_hang) == 2:
                if self.ban_co[hang_cu + (1 if d_hang > 0 else -1)][cot_cu] != '--': return False 
            else:
                if self.ban_co[hang_cu][cot_cu + (1 if d_cot > 0 else -1)] != '--': return False 
            return True 
        return False 

    def kiem_tra_luat_tuong(self, hang_cu, cot_cu, hang_moi, cot_moi, quan_cu):
        if abs(hang_moi - hang_cu) == 2 and abs(cot_moi - cot_cu) == 2:
            if quan_cu.startswith('r') and hang_moi < 5: return False 
            if quan_cu.startswith('b') and hang_moi > 4: return False 
            if self.ban_co[(hang_cu + hang_moi) // 2][(cot_cu + cot_moi) // 2] != '--': return False 
            return True 
        return False 

    def kiem_tra_luat_phao(self, hang_cu, cot_cu, hang_moi, cot_moi, quan_muc_tieu):
        if hang_cu != hang_moi and cot_cu != cot_moi: return False 
        so_quan_can = 0 
        if hang_cu == hang_moi: 
            for c in range(min(cot_cu, cot_moi) + 1, max(cot_cu, cot_moi)):
                if self.ban_co[hang_cu][c] != '--': so_quan_can += 1
        else: 
            for h in range(min(hang_cu, hang_moi) + 1, max(hang_cu, hang_moi)):
                if self.ban_co[h][cot_cu] != '--': so_quan_can += 1
        return so_quan_can == 0 if quan_muc_tieu == '--' else so_quan_can == 1

    def kiem_tra_luat_sy(self, hang_cu, cot_cu, hang_moi, cot_moi, quan_cu):
        if abs(hang_moi - hang_cu) == 1 and abs(cot_moi - cot_cu) == 1:
            if cot_moi < 3 or cot_moi > 5: return False
            if quan_cu.startswith('r') and (hang_moi < 7 or hang_moi > 9): return False
            if quan_cu.startswith('b') and (hang_moi < 0 or hang_moi > 2): return False
            return True 
        return False

    def kiem_tra_luat_vua(self, hang_cu, cot_cu, hang_moi, cot_moi, quan_cu):
        if abs(hang_moi - hang_cu) + abs(cot_moi - cot_cu) == 1:
            if cot_moi < 3 or cot_moi > 5: return False
            if quan_cu.startswith('r') and (hang_moi < 7 or hang_moi > 9): return False
            if quan_cu.startswith('b') and (hang_moi < 0 or hang_moi > 2): return False
            return True 
        return False

    def kiem_tra_luat_chot(self, hang_cu, cot_cu, hang_moi, cot_moi, quan_cu):
        d_hang = hang_moi - hang_cu
        d_cot = abs(cot_moi - cot_cu)
        if abs(d_hang) + d_cot != 1: return False
        if quan_cu.startswith('r'): 
            if d_hang > 0: return False
            if hang_cu >= 5 and d_cot > 0: return False
        else:
            if d_hang < 0: return False
            if hang_cu <= 4 and d_cot > 0: return False
        return True

    def kiem_tra_lo_mat_tuong(self):
        hang_do = cot_do = hang_den = cot_den = -1
        for i in range(10):
            for j in range(9):
                if self.ban_co[i][j] == 'rK': hang_do, cot_do = i, j
                elif self.ban_co[i][j] == 'bK': hang_den, cot_den = i, j
        if cot_do == -1 or cot_den == -1: return False
        if cot_do == cot_den:
            for h in range(min(hang_do, hang_den) + 1, max(hang_do, hang_den)):
                if self.ban_co[h][cot_do] != '--': return False 
            return True 
        return False

    # ================= CÁC HÀM MỚI BỔ SUNG =================

    def tim_tuong(self, phe):
        """Tìm toạ độ Tướng của phe chỉ định"""
        quan_tuong = 'rK' if phe == 'Do' else 'bK'
        for i in range(10):
            for j in range(9):
                if self.ban_co[i][j] == quan_tuong:
                    return i, j
        return -1, -1

    def kiem_tra_bi_chieu(self, phe_bi_chieu):
        """Kiểm tra xem Tướng của phe truyền vào có đang bị quân địch nào nhắm tới không"""
        hang_t, cot_t = self.tim_tuong(phe_bi_chieu)
        if hang_t == -1: return [] # Lỗi không thấy tướng
        
        phe_tan_cong = 'Den' if phe_bi_chieu == 'Do' else 'Do'
        prefix_tan_cong = 'b' if phe_tan_cong == 'Den' else 'r'
        ke_tan_cong = []

        for r in range(10):
            for c in range(9):
                quan = self.ban_co[r][c]
                if quan.startswith(prefix_tan_cong):
                    hop_le = False
                    if quan.endswith('X'): hop_le = self.kiem_tra_luat_xe(r, c, hang_t, cot_t)
                    elif quan.endswith('M'): hop_le = self.kiem_tra_luat_ma(r, c, hang_t, cot_t)
                    elif quan.endswith('P'): hop_le = self.kiem_tra_luat_phao(r, c, hang_t, cot_t, self.ban_co[hang_t][cot_t])
                    elif quan.endswith('C'): hop_le = self.kiem_tra_luat_chot(r, c, hang_t, cot_t, quan)
                    
                    if hop_le: ke_tan_cong.append((r, c))
                    
        return ke_tan_cong # Trả về danh sách toạ độ các quân địch đang chiếu

    def kiem_tra_chieu_bi(self, phe_bi_chieu):
        """Kiểm tra xem phe này có bị chiếu bí (hết đường cứu) chưa"""
        # Nếu đang không bị chiếu thì không thể gọi là chiếu bí
        ke_tan_cong = self.kiem_tra_bi_chieu(phe_bi_chieu)
        if len(ke_tan_cong) == 0:
            return False, []
            
        prefix_phong_thu = 'r' if phe_bi_chieu == 'Do' else 'b'
        
        # Thử đi tất cả các quân của phe bị chiếu đến mọi ô trên bàn cờ
        for r in range(10):
            for c in range(9):
                quan = self.ban_co[r][c]
                if quan.startswith(prefix_phong_thu):
                    for r_moi in range(10):
                        for c_moi in range(9):
                            quan_muc_tieu = self.ban_co[r_moi][c_moi]
                            if quan_muc_tieu.startswith(prefix_phong_thu): continue
                            
                            hop_le = False
                            if quan.endswith('X'): hop_le = self.kiem_tra_luat_xe(r, c, r_moi, c_moi)
                            elif quan.endswith('M'): hop_le = self.kiem_tra_luat_ma(r, c, r_moi, c_moi)
                            elif quan.endswith('T'): hop_le = self.kiem_tra_luat_tuong(r, c, r_moi, c_moi, quan)
                            elif quan.endswith('P'): hop_le = self.kiem_tra_luat_phao(r, c, r_moi, c_moi, quan_muc_tieu)
                            elif quan.endswith('S'): hop_le = self.kiem_tra_luat_sy(r, c, r_moi, c_moi, quan)
                            elif quan.endswith('K'): hop_le = self.kiem_tra_luat_vua(r, c, r_moi, c_moi, quan)
                            elif quan.endswith('C'): hop_le = self.kiem_tra_luat_chot(r, c, r_moi, c_moi, quan)
                            
                            if hop_le:
                                # Giả lập thử nước đi này
                                self.ban_co[r][c] = '--'
                                self.ban_co[r_moi][c_moi] = quan
                                
                                lo_mat = self.kiem_tra_lo_mat_tuong()
                                van_bi_chieu = len(self.kiem_tra_bi_chieu(phe_bi_chieu)) > 0
                                
                                # Hoàn tác lại bàn cờ
                                self.ban_co[r][c] = quan
                                self.ban_co[r_moi][c_moi] = quan_muc_tieu
                                
                                # Nếu có 1 nước đi không làm lộ mặt tướng VÀ thoát được chiếu -> Chưa Bí!
                                if not lo_mat and not van_bi_chieu:
                                    return False, []
        
        # Nếu kịch bản đi tới đây, nghĩa là đã thử mọi cách nhưng vẫn chết -> Chiếu bí!
        return True, ke_tan_congclass LogicCoTuong:
    def __init__(self):
        self.ban_co = [
            ['bX', 'bM', 'bT', 'bS', 'bK', 'bS', 'bT', 'bM', 'bX'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', 'bP', '--', '--', '--', '--', '--', 'bP', '--'],
            ['bC', '--', 'bC', '--', 'bC', '--', 'bC', '--', 'bC'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['rC', '--', 'rC', '--', 'rC', '--', 'rC', '--', 'rC'],
            ['--', 'rP', '--', '--', '--', '--', '--', 'rP', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['rX', 'rM', 'rT', 'rS', 'rK', 'rS', 'rT', 'rM', 'rX']
        ]
        self.luot_di = "Do"

    def kiem_tra_luat_xe(self, hang_cu, cot_cu, hang_moi, cot_moi):
        if hang_cu != hang_moi and cot_cu != cot_moi: return False 
        if hang_cu == hang_moi: 
            for c in range(min(cot_cu, cot_moi) + 1, max(cot_cu, cot_moi)):
                if self.ban_co[hang_cu][c] != '--': return False
        else: 
            for h in range(min(hang_cu, hang_moi) + 1, max(hang_cu, hang_moi)):
                if self.ban_co[h][cot_cu] != '--': return False
        return True

    def kiem_tra_luat_ma(self, hang_cu, cot_cu, hang_moi, cot_moi):
        d_hang = hang_moi - hang_cu
        d_cot = cot_moi - cot_cu
        if (abs(d_hang) == 2 and abs(d_cot) == 1) or (abs(d_hang) == 1 and abs(d_cot) == 2):
            if abs(d_hang) == 2:
                if self.ban_co[hang_cu + (1 if d_hang > 0 else -1)][cot_cu] != '--': return False 
            else:
                if self.ban_co[hang_cu][cot_cu + (1 if d_cot > 0 else -1)] != '--': return False 
            return True 
        return False 

    def kiem_tra_luat_tuong(self, hang_cu, cot_cu, hang_moi, cot_moi, quan_cu):
        if abs(hang_moi - hang_cu) == 2 and abs(cot_moi - cot_cu) == 2:
            if quan_cu.startswith('r') and hang_moi < 5: return False 
            if quan_cu.startswith('b') and hang_moi > 4: return False 
            if self.ban_co[(hang_cu + hang_moi) // 2][(cot_cu + cot_moi) // 2] != '--': return False 
            return True 
        return False 

    def kiem_tra_luat_phao(self, hang_cu, cot_cu, hang_moi, cot_moi, quan_muc_tieu):
        if hang_cu != hang_moi and cot_cu != cot_moi: return False 
        so_quan_can = 0 
        if hang_cu == hang_moi: 
            for c in range(min(cot_cu, cot_moi) + 1, max(cot_cu, cot_moi)):
                if self.ban_co[hang_cu][c] != '--': so_quan_can += 1
        else: 
            for h in range(min(hang_cu, hang_moi) + 1, max(hang_cu, hang_moi)):
                if self.ban_co[h][cot_cu] != '--': so_quan_can += 1
        return so_quan_can == 0 if quan_muc_tieu == '--' else so_quan_can == 1

    def kiem_tra_luat_sy(self, hang_cu, cot_cu, hang_moi, cot_moi, quan_cu):
        if abs(hang_moi - hang_cu) == 1 and abs(cot_moi - cot_cu) == 1:
            if cot_moi < 3 or cot_moi > 5: return False
            if quan_cu.startswith('r') and (hang_moi < 7 or hang_moi > 9): return False
            if quan_cu.startswith('b') and (hang_moi < 0 or hang_moi > 2): return False
            return True 
        return False

    def kiem_tra_luat_vua(self, hang_cu, cot_cu, hang_moi, cot_moi, quan_cu):
        if abs(hang_moi - hang_cu) + abs(cot_moi - cot_cu) == 1:
            if cot_moi < 3 or cot_moi > 5: return False
            if quan_cu.startswith('r') and (hang_moi < 7 or hang_moi > 9): return False
            if quan_cu.startswith('b') and (hang_moi < 0 or hang_moi > 2): return False
            return True 
        return False

    def kiem_tra_luat_chot(self, hang_cu, cot_cu, hang_moi, cot_moi, quan_cu):
        d_hang = hang_moi - hang_cu
        d_cot = abs(cot_moi - cot_cu)
        if abs(d_hang) + d_cot != 1: return False
        if quan_cu.startswith('r'): 
            if d_hang > 0: return False
            if hang_cu >= 5 and d_cot > 0: return False
        else:
            if d_hang < 0: return False
            if hang_cu <= 4 and d_cot > 0: return False
        return True

    def kiem_tra_lo_mat_tuong(self):
        hang_do = cot_do = hang_den = cot_den = -1
        for i in range(10):
            for j in range(9):
                if self.ban_co[i][j] == 'rK': hang_do, cot_do = i, j
                elif self.ban_co[i][j] == 'bK': hang_den, cot_den = i, j
        if cot_do == -1 or cot_den == -1: return False
        if cot_do == cot_den:
            for h in range(min(hang_do, hang_den) + 1, max(hang_do, hang_den)):
                if self.ban_co[h][cot_do] != '--': return False 
            return True 
        return False

    def tim_tuong(self, phe):
        quan_tuong = 'rK' if phe == 'Do' else 'bK'
        for i in range(10):
            for j in range(9):
                if self.ban_co[i][j] == quan_tuong:
                    return i, j
        return -1, -1

    def kiem_tra_bi_chieu(self, phe_bi_chieu):
        hang_t, cot_t = self.tim_tuong(phe_bi_chieu)
        if hang_t == -1: return [] 
        
        phe_tan_cong = 'Den' if phe_bi_chieu == 'Do' else 'Do'
        prefix_tan_cong = 'b' if phe_tan_cong == 'Den' else 'r'
        ke_tan_cong = []

        for r in range(10):
            for c in range(9):
                quan = self.ban_co[r][c]
                if quan.startswith(prefix_tan_cong):
                    hop_le = False
                    if quan.endswith('X'): hop_le = self.kiem_tra_luat_xe(r, c, hang_t, cot_t)
                    elif quan.endswith('M'): hop_le = self.kiem_tra_luat_ma(r, c, hang_t, cot_t)
                    elif quan.endswith('P'): hop_le = self.kiem_tra_luat_phao(r, c, hang_t, cot_t, self.ban_co[hang_t][cot_t])
                    elif quan.endswith('C'): hop_le = self.kiem_tra_luat_chot(r, c, hang_t, cot_t, quan)
                    
                    if hop_le: ke_tan_cong.append((r, c))
                    
        return ke_tan_cong 

    def kiem_tra_chieu_bi(self, phe_bi_chieu):
        ke_tan_cong = self.kiem_tra_bi_chieu(phe_bi_chieu)
        if len(ke_tan_cong) == 0:
            return False, []
            
        prefix_phong_thu = 'r' if phe_bi_chieu == 'Do' else 'b'
        
        for r in range(10):
            for c in range(9):
                quan = self.ban_co[r][c]
                if quan.startswith(prefix_phong_thu):
                    ds_nuoc_cuu_gia = self.lay_cac_nuoc_di_hop_le(r, c)
                    if len(ds_nuoc_cuu_gia) > 0:
                        return False, [] # Chỉ cần 1 quân có 1 nước đi cứu được Tướng là chưa Bí
                        
        return True, ke_tan_cong

    # ================= HÀM MỚI TẠO GỢI Ý NƯỚC ĐI =================
    def lay_cac_nuoc_di_hop_le(self, hang, cot):
        """Trả về danh sách tọa độ (hàng, cột) mà quân cờ có thể đi tới"""
        ds_hop_le = []
        quan_cu = self.ban_co[hang][cot]
        if quan_cu == '--': return ds_hop_le

        phe_cua_quan = 'Do' if quan_cu.startswith('r') else 'Den'
        prefix_phe = 'r' if phe_cua_quan == 'Do' else 'b'

        # Quét toàn bộ bàn cờ xem ô nào đi được
        for r_moi in range(10):
            for c_moi in range(9):
                quan_muc_tieu = self.ban_co[r_moi][c_moi]
                
                if quan_muc_tieu.startswith(prefix_phe): 
                    continue # Bỏ qua ô có quân cùng phe
                    
                hop_le = False
                if quan_cu.endswith('X'): hop_le = self.kiem_tra_luat_xe(hang, cot, r_moi, c_moi)
                elif quan_cu.endswith('M'): hop_le = self.kiem_tra_luat_ma(hang, cot, r_moi, c_moi)
                elif quan_cu.endswith('T'): hop_le = self.kiem_tra_luat_tuong(hang, cot, r_moi, c_moi, quan_cu)
                elif quan_cu.endswith('P'): hop_le = self.kiem_tra_luat_phao(hang, cot, r_moi, c_moi, quan_muc_tieu)
                elif quan_cu.endswith('S'): hop_le = self.kiem_tra_luat_sy(hang, cot, r_moi, c_moi, quan_cu)
                elif quan_cu.endswith('K'): hop_le = self.kiem_tra_luat_vua(hang, cot, r_moi, c_moi, quan_cu)
                elif quan_cu.endswith('C'): hop_le = self.kiem_tra_luat_chot(hang, cot, r_moi, c_moi, quan_cu)

                if hop_le:
                    # Giả lập đi thử xem có bị lỗi tự sát/lộ mặt tướng không
                    self.ban_co[hang][cot] = '--'
                    self.ban_co[r_moi][c_moi] = quan_cu
                    
                    lo_mat = self.kiem_tra_lo_mat_tuong()
                    bi_chieu = len(self.kiem_tra_bi_chieu(phe_cua_quan)) > 0
                    
                    # Hoàn tác
                    self.ban_co[hang][cot] = quan_cu
                    self.ban_co[r_moi][c_moi] = quan_muc_tieu
                    
                    # Nếu nước đi an toàn -> Đưa vào danh sách gợi ý
                    if not lo_mat and not bi_chieu:
                        ds_hop_le.append((r_moi, c_moi))
                        
        return ds_hop_le