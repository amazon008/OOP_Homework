import tkinter as tk
from tkinter import messagebox
from logic import LogicCoTuong  

# Tự động kiểm tra và import Pillow để xử lý ảnh JPG
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

CHINESE_CHARS = {
    'rK': '帥', 'rS': '仕', 'rT': '相', 'rX': '車', 'rM': '傌', 'rP': '炮', 'rC': '兵', 
    'bK': '將', 'bS': '士', 'bT': '象', 'bX': '車', 'bM': '馬', 'bP': '砲', 'bC': '卒' 
}

# ================= CLASS NÚT TÙY CHỈNH BO TRÒN TỚI BẾN =================
class NutBoGoc(tk.Canvas):
    def __init__(self, parent, text, command, mau_nen="#1cd153", mau_chu="white", mau_bg_cha="#fdfaf6", width=240, height=48, radius=24, font=("Arial", 14, "bold"), state=tk.NORMAL):
        super().__init__(parent, width=width, height=height, bg=mau_bg_cha, highlightthickness=0, bd=0)
        self.command = command
        self.mau_nen = mau_nen
        self.mau_disabled = "#e2e8f0"
        self.state = state
        self.text = text
        self.font = font
        self.mau_chu = mau_chu
        self.radius = radius
        self.width = width
        self.height = height
        self.is_pressed = False
        
        self.ve_nut()
        
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
    def ve_nut(self):
        self.delete("all")
        x1, y1, x2, y2 = 0, 0, self.width, self.height
        
        # Tọa độ đa giác để tạo đường cong Bezier cho Canvas
        points = [
            x1+self.radius, y1, x1+self.radius, y1, 
            x2-self.radius, y1, x2-self.radius, y1, 
            x2, y1, x2, y1+self.radius, x2, y1+self.radius, 
            x2, y2-self.radius, x2, y2-self.radius, 
            x2, y2, x2-self.radius, y2, x2-self.radius, y2, 
            x1+self.radius, y2, x1+self.radius, y2, 
            x1, y2, x1, y2-self.radius, x1, y2-self.radius, 
            x1, y1+self.radius, x1, y1+self.radius, 
            x1, y1
        ]
        color = self.mau_nen if self.state == tk.NORMAL else self.mau_disabled
        text_color = self.mau_chu if self.state == tk.NORMAL else "#94a3b8"
        
        self.rect_id = self.create_polygon(points, fill=color, smooth=True)
        self.text_id = self.create_text(self.width/2, self.height/2, text=self.text, font=self.font, fill=text_color)

    def config_state(self, state):
        self.state = state
        self.ve_nut()

    def _on_press(self, event):
        if self.state == tk.NORMAL and not self.is_pressed:
            self.is_pressed = True
            self.move(self.rect_id, 0, 2)
            self.move(self.text_id, 0, 2)
        
    def _on_release(self, event):
        if self.state == tk.NORMAL and self.is_pressed:
            self.is_pressed = False
            self.move(self.rect_id, 0, -2)
            self.move(self.text_id, 0, -2)
            if self.command:
                self.command()
                
    def _on_enter(self, event):
        if self.state == tk.NORMAL:
            self.config(cursor="hand2")
            self.itemconfig(self.rect_id, fill="#19b849") # Đổi sang xanh đậm hơn khi di chuột
            
    def _on_leave(self, event):
        if self.state == tk.NORMAL:
            self.config(cursor="")
            self.itemconfig(self.rect_id, fill=self.mau_nen)


# ================= GIAO DIỆN CHÍNH =================
class CoTuongGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Cờ Tướng - Xiangqi Style")
        self.root.geometry("600x780") 
        self.root.configure(bg="#fdfaf6") 
        
        self.game = LogicCoTuong()
        self.hang_cu = -1 
        self.cot_cu = -1
        self.goi_y_di = [] 
        self.lich_su_di = [] 
        self.game_over = False
        self.ke_tan_cong = [] 
        self.vua_bi_diet = () 
        
        self.cell_size = 60
        self.margin = 50
        
        self.ten_nguoi_choi_1 = "Người chơi 1"
        self.ten_nguoi_choi_2 = "Người chơi 2"
        
        self.bg_image = None
        if HAS_PIL:
            try:
                img = Image.open("pexels-jayce-q-132128526-34313319.jpg")
                img = img.resize((600, 780), Image.Resampling.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Không thể tải ảnh nền: {e}")
        
        self.khung_giao_dien = tk.Frame(self.root, bg="#fdfaf6")
        self.khung_giao_dien.pack(fill=tk.BOTH, expand=True)
        
        self.man_hinh_bat_dau()

    def xoa_khung_giao_dien(self):
        for widget in self.khung_giao_dien.winfo_children():
            widget.destroy()

    def man_hinh_bat_dau(self):
        self.xoa_khung_giao_dien()
        
        if self.bg_image:
            self.canvas_bg = tk.Canvas(self.khung_giao_dien, width=600, height=780, highlightthickness=0, bd=0)
            self.canvas_bg.pack(fill=tk.BOTH, expand=True)
            self.canvas_bg.create_image(0, 0, image=self.bg_image, anchor="nw")
            
            # Vẽ nút Bắt Đầu trực tiếp lên hình nền để không bị lẹm khung trắng
            self._ve_nut_bat_dau_tren_nen(self.canvas_bg)
        else:
            # Fallback nếu không có ảnh
            btn_bat_dau = NutBoGoc(self.khung_giao_dien, "Bắt Đầu Chơi", self.man_hinh_chon_che_do, 
                                   mau_nen="#1cd153", mau_chu="white", mau_bg_cha="#fdfaf6", 
                                   width=260, height=56, radius=28, font=("Arial", 16, "bold"))
            btn_bat_dau.pack(pady=(585, 0))

    def _ve_nut_bat_dau_tren_nen(self, canvas):
        width, height = 260, 56
        radius = 28
        x_center, y_center = 300, 585
        
        x1, y1 = x_center - width/2, y_center - height/2
        x2, y2 = x_center + width/2, y_center + height/2
        
        points = [
            x1+radius, y1, x1+radius, y1, 
            x2-radius, y1, x2-radius, y1, 
            x2, y1, x2, y1+radius, x2, y1+radius, 
            x2, y2-radius, x2, y2-radius, 
            x2, y2, x2-radius, y2, x2-radius, y2, 
            x1+radius, y2, x1+radius, y2, 
            x1, y2, x1, y2-radius, x1, y2-radius, 
            x1, y1+radius, x1, y1+radius, 
            x1, y1
        ]
        
        # Bóng đen mờ bên dưới nút
        canvas.create_polygon([p + 3 if i % 2 == 1 else p for i, p in enumerate(points)], fill="#000000", smooth=True, stipple="gray50")
        
        btn_id = canvas.create_polygon(points, fill="#1cd153", smooth=True)
        text_id = canvas.create_text(x_center, y_center, text="Bắt Đầu Chơi", font=("Arial", 16, "bold"), fill="white")
        
        is_pressed = [False]
        def on_press(event):
            if not is_pressed[0]:
                is_pressed[0] = True
                canvas.move(btn_id, 0, 2)
                canvas.move(text_id, 0, 2)
                
        def on_release(event):
            if is_pressed[0]:
                is_pressed[0] = False
                canvas.move(btn_id, 0, -2)
                canvas.move(text_id, 0, -2)
                self.root.after(100, self.man_hinh_chon_che_do)
            
        def enter(e):
            canvas.config(cursor="hand2")
            canvas.itemconfig(btn_id, fill="#19b849")

        def leave(e):
            canvas.config(cursor="")
            canvas.itemconfig(btn_id, fill="#1cd153")

        for item in (btn_id, text_id):
            canvas.tag_bind(item, "<ButtonPress-1>", on_press)
            canvas.tag_bind(item, "<ButtonRelease-1>", on_release)
            canvas.tag_bind(item, "<Enter>", enter)
            canvas.tag_bind(item, "<Leave>", leave)

    def man_hinh_chon_che_do(self):
        self.xoa_khung_giao_dien()
        
        if self.bg_image:
            bg_label = tk.Label(self.khung_giao_dien, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
        khung_trung_tam = tk.Frame(self.khung_giao_dien, bg="#fdfaf6", bd=2, relief=tk.SOLID, padx=20, pady=20)
        khung_trung_tam.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=380, height=300)
        
        tk.Label(khung_trung_tam, text="Chọn Chế Độ Chơi", font=("Arial", 20, "bold"), fg="#2c3e50", bg="#fdfaf6").pack(pady=(20, 30))
        
        btn_1vs1 = tk.Button(khung_trung_tam, text="⚔️   Chế Độ 1 VS 1   ⚔️\n(Chơi đối kháng offline)", font=("Arial", 14, "bold"),
                             bg="white", fg="#1cd153", activebackground="#f1f2f6", activeforeground="#1cd153",
                             bd=1, relief=tk.SOLID, width=24, height=3, cursor="hand2", highlightthickness=0,
                             command=self.man_hinh_nhap_ten)
        btn_1vs1.pack(pady=10)

    def man_hinh_nhap_ten(self):
        self.xoa_khung_giao_dien()
        
        if self.bg_image:
            bg_label = tk.Label(self.khung_giao_dien, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
        khung_trung_tam = tk.Frame(self.khung_giao_dien, bg="#fdfaf6", bd=2, relief=tk.SOLID, padx=25, pady=25)
        khung_trung_tam.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=450)
        
        tk.Label(khung_trung_tam, text="Thông Tin Người Chơi", font=("Arial", 20, "bold"), fg="#2c3e50", bg="#fdfaf6").pack(pady=(10, 25))
        
        frame_p1 = tk.Frame(khung_trung_tam, bg="#fdfaf6")
        frame_p1.pack(pady=10, fill=tk.X)
        tk.Label(frame_p1, text="Tên Người Chơi 1 (Quân Đỏ):", font=("Arial", 11, "bold"), fg="#e74c3c", bg="#fdfaf6").pack(anchor=tk.W, pady=3)
        self.var_ten1 = tk.StringVar()
        self.var_ten1.trace_add("write", self.kiem_tra_form_nhap) 
        
        self.ent_p1 = tk.Entry(frame_p1, textvariable=self.var_ten1, font=("Arial", 12), justify="center", 
                               bg="#F5F5F5", fg="#333333", relief="flat", highlightthickness=1,
                               highlightbackground="#CCCCCC", highlightcolor="#C0392B")
        self.ent_p1.pack(fill=tk.X, ipady=8)
        
        frame_p2 = tk.Frame(khung_trung_tam, bg="#fdfaf6")
        frame_p2.pack(pady=10, fill=tk.X)
        tk.Label(frame_p2, text="Tên Người Chơi 2 (Quân Đen):", font=("Arial", 11, "bold"), fg="#2c3e50", bg="#fdfaf6").pack(anchor=tk.W, pady=3)
        self.var_ten2 = tk.StringVar()
        self.var_ten2.trace_add("write", self.kiem_tra_form_nhap) 
        
        self.ent_p2 = tk.Entry(frame_p2, textvariable=self.var_ten2, font=("Arial", 12), justify="center", 
                               bg="#F5F5F5", fg="#333333", relief="flat", highlightthickness=1,
                               highlightbackground="#CCCCCC", highlightcolor="#2C3E50")
        self.ent_p2.pack(fill=tk.X, ipady=8)
        
        # THAY BẰNG NÚT BO GÓC MÀU XANH HIỆN ĐẠI
        self.btn_choi = NutBoGoc(khung_trung_tam, "Bắt Đầu Trận Đấu", self.vao_tran_dau, 
                                 mau_nen="#1cd153", mau_chu="white", mau_bg_cha="#fdfaf6", 
                                 width=240, height=48, radius=24, state=tk.DISABLED)
        self.btn_choi.pack(pady=30)
        
        self.ent_p1.bind("<Return>", lambda event: self.ent_p2.focus())
        self.ent_p2.bind("<Return>", self.kiem_tra_va_vao_tran)

        self.ent_p1.focus()
        
    def kiem_tra_va_vao_tran(self, event=None):
        if self.btn_choi.state == tk.NORMAL:
            self.vao_tran_dau()

    def kiem_tra_form_nhap(self, *args):
        ten1 = self.var_ten1.get().strip()
        ten2 = self.var_ten2.get().strip()
        
        if ten1 != "" and ten2 != "":
            self.btn_choi.config_state(tk.NORMAL)
        else:
            self.btn_choi.config_state(tk.DISABLED)

    def vao_tran_dau(self):
        self.ten_nguoi_choi_1 = self.var_ten1.get().strip()
        self.ten_nguoi_choi_2 = self.var_ten2.get().strip()
        
        self.xoa_khung_giao_dien()
        self.root.configure(bg="#2c3e50")
        self.khung_giao_dien.configure(bg="#2c3e50")
        
        width = 8 * self.cell_size + 2 * self.margin
        height = 9 * self.cell_size + 2 * self.margin
        
        self.thong_bao = tk.Label(self.khung_giao_dien, text="", font=("Arial", 16, "bold"), bg="#2c3e50", fg="white")
        self.thong_bao.pack(pady=10)

        self.canvas = tk.Canvas(self.khung_giao_dien, width=width, height=height, bg="#e3c193", highlightthickness=0)
        self.canvas.pack(pady=5)
        self.canvas.bind("<Button-1>", self.xu_ly_click)
        
        self.tao_thanh_chuc_nang(self.khung_giao_dien)
        self.cap_nhat_ban_co()

    def tao_thanh_chuc_nang(self, parent):
        frame_btn = tk.Frame(parent, bg="#2c3e50")
        frame_btn.pack(pady=10)
        
        btn_style = {"font": ("Arial", 11, "bold"), "width": 11, "bd": 0, "height": 1, "cursor": "hand2"}
        
        self.btn_di_lai = tk.Button(frame_btn, text="Đi Lại ↩", bg="#3498db", fg="white", 
                                    activebackground="#2980b9", activeforeground="white", command=self.di_lai, **btn_style)
        self.btn_di_lai.pack(side=tk.LEFT, padx=12)
        
        self.btn_hoa = tk.Button(frame_btn, text="Hòa Cờ 🤝", bg="#e67e22", fg="white", 
                                activebackground="#d35400", activeforeground="white", command=self.cau_hoa, **btn_style)
        self.btn_hoa.pack(side=tk.LEFT, padx=12)
        
        self.btn_chiu_thua = tk.Button(frame_btn, text="Chịu Thua 🏳", bg="#e74c3c", fg="white", 
                                      activebackground="#c0392b", activeforeground="white", command=self.dau_hang, **btn_style)
        self.btn_chiu_thua.pack(side=tk.LEFT, padx=12)

    def ve_ban_co(self):
        self.canvas.delete("all") 
        for i in range(10):
            y = self.margin + i * self.cell_size
            self.canvas.create_line(self.margin, y, self.margin + 8 * self.cell_size, y, width=2)
            
        for j in range(9):
            x = self.margin + j * self.cell_size
            if j == 0 or j == 8: 
                self.canvas.create_line(x, self.margin, x, self.margin + 9 * self.cell_size, width=2)
            else: 
                self.canvas.create_line(x, self.margin, x, self.margin + 4 * self.cell_size, width=2)
                self.canvas.create_line(x, self.margin + 5 * self.cell_size, x, self.margin + 9 * self.cell_size, width=2)
                
        self.canvas.create_line(self.margin + 3*self.cell_size, self.margin, self.margin + 5*self.cell_size, self.margin + 2*self.cell_size, width=2)
        self.canvas.create_line(self.margin + 5*self.cell_size, self.margin, self.margin + 3*self.cell_size, self.margin + 2*self.cell_size, width=2)
        self.canvas.create_line(self.margin + 3*self.cell_size, self.margin + 7*self.cell_size, self.margin + 5*self.cell_size, self.margin + 9*self.cell_size, width=2)
        self.canvas.create_line(self.margin + 5*self.cell_size, self.margin + 7*self.cell_size, self.margin + 3*self.cell_size, self.margin + 9*self.cell_size, width=2)
        
        center_y = self.margin + 4.5 * self.cell_size
        self.canvas.create_text(self.margin + 2*self.cell_size, center_y, text="楚 河", font=("KaiTi", 24, "bold"), angle=0)
        self.canvas.create_text(self.margin + 6*self.cell_size, center_y, text="漢 界", font=("KaiTi", 24, "bold"), angle=0)

        for j in range(9):
            x = self.margin + j * self.cell_size
            self.canvas.create_text(x, self.margin - 35, text=str(j + 1), font=("Arial", 12, "bold"), fill="black")
            self.canvas.create_text(x, self.margin + 9 * self.cell_size + 35, text=str(9 - j), font=("Arial", 12, "bold"), fill="red")

    def ve_quan_co(self):
        ban_co = self.game.ban_co
        r_radius = 22 
        
        for r in range(10):
            for c in range(9):
                quan = ban_co[r][c]
                if quan != '--':
                    x = self.margin + c * self.cell_size
                    y = self.margin + r * self.cell_size
                    
                    if self.game_over:
                        if (r, c) in self.ke_tan_cong:
                            self.canvas.create_oval(x - r_radius - 6, y - r_radius - 6, x + r_radius + 6, y + r_radius + 6, fill="#2ecc71", outline="#27ae60", width=2)
                            self.canvas.create_oval(x + r_radius - 5, y - r_radius - 10, x + r_radius + 15, y - r_radius + 10, fill="#2ecc71", outline="white")
                            self.canvas.create_text(x + r_radius + 5, y - r_radius, text="✔", fill="white", font=("Arial", 10, "bold"))
                    elif self.hang_cu == r and self.cot_cu == c:
                        self.canvas.create_oval(x - r_radius - 4, y - r_radius - 4, x + r_radius + 4, y + r_radius + 4, fill="#f1c40f", outline="#f39c12", width=2)

                    color = "#c0392b" if quan.startswith('r') else "#2c3e50"
                    text_color = "red" if quan.startswith('r') else "black"
                    
                    self.canvas.create_oval(x - r_radius, y - r_radius, x + r_radius, y + r_radius, fill="#f5e6d3", outline=color, width=3)
                    self.canvas.create_oval(x - r_radius + 4, y - r_radius + 4, x + r_radius - 4, y + r_radius - 4, outline=color, width=1)
                    
                    char = CHINESE_CHARS.get(quan, quan)
                    self.canvas.create_text(x, y, text=char, font=("KaiTi", 20, "bold"), fill=text_color)
                    
                    if self.game_over and self.vua_bi_diet == (r, c):
                        self.canvas.create_oval(x - r_radius - 4, y - r_radius - 4, x + r_radius + 4, y + r_radius + 4, outline="#9b59b6", width=4)
                        self.canvas.create_line(x + r_radius + 4, y - r_radius - 4, x - r_radius - 4, y + r_radius + 4, fill="#9b59b6", width=4)

    def ve_goi_y_di(self):
        dot_radius = 8
        r_radius = 22 
        for r, c in self.goi_y_di:
            x = self.margin + c * self.cell_size
            y = self.margin + r * self.cell_size
            quan_muc_tieu = self.game.ban_co[r][c]
            if quan_muc_tieu == '--':
                self.canvas.create_oval(x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius, fill="#a855f7", outline="#8e44ad")
            else:
                self.canvas.create_oval(x - r_radius - 4, y - r_radius - 4, x + r_radius + 4, y + r_radius + 4, outline="#a855f7", width=4)

    def cap_nhat_ban_co(self):
        self.ve_ban_co()
        self.ve_quan_co()
        self.ve_goi_y_di() 
        
        if self.game_over: return 
            
        if self.game.luot_di == "Do":
            self.thong_bao.config(text=f"LƯỢT ĐI: {self.ten_nguoi_choi_1} (Đỏ)", fg="#ff4757")
        else:
            self.thong_bao.config(text=f"LƯỢT ĐI: {self.ten_nguoi_choi_2} (Đen)", fg="#7bed9f")
    
    def reset_game(self):
        self.game = LogicCoTuong()
        self.hang_cu = -1
        self.cot_cu = -1
        self.goi_y_di = []
        self.lich_su_di = []
        self.game_over = False
        self.ke_tan_cong = []
        self.vua_bi_diet = ()
        self.cap_nhat_ban_co()

    def di_lai(self):
        if not self.lich_su_di:
            messagebox.showinfo("Thông báo", "Chưa có nước cờ nào được đi để lùi lại!")
            return
        if self.game_over:
            self.game_over = False
            self.ke_tan_cong = []
            self.vua_bi_diet = ()
            
        trang_thai_cu = self.lich_su_di.pop()
        self.game.ban_co = trang_thai_cu['ban_co']
        self.game.luot_di = trang_thai_cu['luot_di']
        self.hang_cu = -1
        self.goi_y_di = []
        self.cap_nhat_ban_co()

    def cau_hoa(self):
        if self.game_over: return
        if messagebox.askyesno("Cầu Hòa", "Bạn có chắc chắn muốn kết thúc trận đấu với tỷ số Hòa không?"):
            self.game_over = True
            self.thong_bao.config(text="GAME OVER - HÒA CỜ", fg="#9b59b6")
            self.hien_thi_bang_ket_qua(self.ten_nguoi_choi_1, self.ten_nguoi_choi_2, "Hòa", "Hòa", "🤝 Hòa Cờ!", "Hai bên đã bắt tay giảng hòa, bất phân thắng bại.")

    def dau_hang(self):
        if self.game_over: return
        if self.game.luot_di == "Do":
            ten_p_thua, phe_thua = self.ten_nguoi_choi_1, "Đỏ"
            ten_p_thang, phe_thang = self.ten_nguoi_choi_2, "Đen"
        else:
            ten_p_thua, phe_thua = self.ten_nguoi_choi_2, "Đen"
            ten_p_thang, phe_thang = self.ten_nguoi_choi_1, "Đỏ"
        
        if messagebox.askyesno("Chịu Thua", f"Người chơi [{ten_p_thua}] muốn đầu hàng?"):
            self.game_over = True
            self.thong_bao.config(text="GAME OVER", fg="#9b59b6")
            self.hien_thi_bang_ket_qua(ten_p_thang, ten_p_thua, phe_thang, phe_thua, "🏳️ Chịu Thua!", "Thế sự như cờ, lúc lên lúc xuống, hãy bình tâm chấp nhận.")

    def hien_thi_bang_ket_qua(self, ten_thang, ten_thua, phe_thang, phe_thua, tieu_de, thong_diep):
        popup = tk.Toplevel(self.root)
        popup.title("Kết Quả Ván Đấu")
        popup.geometry("380x370")
        popup.configure(bg="#fdfaf6") 
        popup.transient(self.root)
        popup.grab_set()

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 190
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 185
        popup.geometry(f"+{x}+{y}")

        tk.Label(popup, text=tieu_de, font=("Arial", 22, "bold"), fg="#e74c3c", bg="#fdfaf6").pack(pady=(20, 5))
        tk.Label(popup, text=thong_diep, font=("Arial", 10, "italic"), fg="#7f8c8d", bg="#fdfaf6").pack(pady=(0, 20))

        frame_players = tk.Frame(popup, bg="#fdfaf6")
        frame_players.pack(fill=tk.X, padx=20)

        frame_thua = tk.Frame(frame_players, bg="#fdfaf6")
        frame_thua.pack(side=tk.LEFT, expand=True)
        tk.Label(frame_thua, text="Thua" if phe_thua != "Hòa" else "Hòa", font=("Arial", 12, "bold"), fg="#e74c3c", bg="#fdfaf6").pack()
        
        cv_thua = tk.Canvas(frame_thua, width=70, height=70, bg="#fdfaf6", highlightthickness=0)
        cv_thua.pack(pady=5)
        mau_nen_thua = "#341f97" if phe_thua == "Đen" else "#eb2f06"
        if phe_thua == "Hòa": mau_nen_thua = "#7f8c8d"
        
        chu_thua = ten_thua[0].upper() if ten_thua else "X"
        
        cv_thua.create_oval(5, 5, 65, 65, fill=mau_nen_thua, outline="")
        cv_thua.create_text(35, 35, text=chu_thua, fill="white", font=("Arial", 20, "bold"))
        tk.Label(frame_thua, text=ten_thua, font=("Arial", 11, "bold"), fg="#2c3e50", bg="#fdfaf6", wraplength=110).pack()

        tk.Label(frame_players, text="Và", font=("Arial", 12), fg="#95a5a6", bg="#fdfaf6").pack(side=tk.LEFT, expand=True)

        frame_thang = tk.Frame(frame_players, bg="#fdfaf6")
        frame_thang.pack(side=tk.RIGHT, expand=True)
        tk.Label(frame_thang, text="Thắng" if phe_thang != "Hòa" else "Hòa", font=("Arial", 12, "bold"), fg="#27ae60", bg="#fdfaf6").pack()
        
        cv_thang = tk.Canvas(frame_thang, width=70, height=70, bg="#fdfaf6", highlightthickness=0)
        cv_thang.pack(pady=5)
        mau_nen_thang = "#eb2f06" if phe_thang == "Đỏ" else "#341f97"
        if phe_thang == "Hòa": mau_nen_thang = "#7f8c8d"
        
        chu_thang = ten_thang[0].upper() if ten_thang else "T"
        
        cv_thang.create_oval(5, 5, 65, 65, fill=mau_nen_thang, outline="")
        cv_thang.create_text(35, 35, text=chu_thang, fill="white", font=("Arial", 20, "bold"))
        tk.Label(frame_thang, text=ten_thang, font=("Arial", 11, "bold"), fg="#2c3e50", bg="#fdfaf6", wraplength=110).pack()

        # NÚT TÁI ĐẤU CŨNG ĐƯỢC BO GÓC!
        btn_tai_dau = NutBoGoc(popup, "↺ Tái Đấu (Ván Mới)", lambda: [self.reset_game(), popup.destroy()], 
                               mau_nen="#1cd153", mau_chu="white", mau_bg_cha="#fdfaf6", 
                               width=220, height=48, radius=24, font=("Arial", 13, "bold"))
        btn_tai_dau.pack(pady=(25, 10))

    def xu_ly_click(self, event):
        if self.game_over: return 

        c = round((event.x - self.margin) / self.cell_size)
        r = round((event.y - self.margin) / self.cell_size)
        
        if not (0 <= c <= 8 and 0 <= r <= 9): return

        if self.hang_cu == -1:
            quan_co = self.game.ban_co[r][c]
            if quan_co == '--': return 
            if (self.game.luot_di == "Do" and not quan_co.startswith('r')) or \
               (self.game.luot_di == "Den" and not quan_co.startswith('b')):
                messagebox.showwarning("Lỗi", "Đây không phải quân của bạn!")
                return
            
            self.hang_cu, self.cot_cu = r, c
            self.goi_y_di = self.game.lay_cac_nuoc_di_hop_le(r, c)
            self.cap_nhat_ban_co() 
            
        else:
            hang_moi, cot_moi = r, c
            quan_cu = self.game.ban_co[self.hang_cu][self.cot_cu]
            quan_muc_tieu = self.game.ban_co[hang_moi][cot_moi]
            
            if hang_moi == self.hang_cu and cot_moi == self.cot_cu:
                self.hang_cu = -1
                self.goi_y_di = [] 
                self.cap_nhat_ban_co()
                return
                
            if (self.game.luot_di == "Do" and quan_muc_tieu.startswith('r')) or \
               (self.game.luot_di == "Den" and quan_muc_tieu.startswith('b')):
                self.hang_cu, self.cot_cu = hang_moi, cot_moi
                self.goi_y_di = self.game.lay_cac_nuoc_di_hop_le(hang_moi, cot_moi)
                self.cap_nhat_ban_co()
                return

            cac_nuoc_hop_le = self.goi_y_di
            self.goi_y_di = [] 
                
            if (hang_moi, cot_moi) not in cac_nuoc_hop_le:
                messagebox.showwarning("Lỗi Luật", "Nước đi không hợp lệ!")
                self.hang_cu = -1
                self.cap_nhat_ban_co()
                return

            trang_thai_truoc = {
                'ban_co': [row[:] for row in self.game.ban_co],
                'luot_di': self.game.luot_di
            }
            self.lich_su_di.append(trang_thai_truoc)

            self.game.ban_co[self.hang_cu][self.cot_cu] = '--' 
            self.game.ban_co[hang_moi][cot_moi] = quan_cu      

            self.game.luot_di = "Den" if self.game.luot_di == "Do" else "Do"
            self.hang_cu = -1
            
            phe_sap_danh = self.game.luot_di
            bi_chieu_bi, ds_ke_dich = self.game.kiem_tra_chieu_bi(phe_sap_danh)
            
            if bi_chieu_bi:
                self.game_over = True
                self.ke_tan_cong = ds_ke_dich
                self.vua_bi_diet = self.game.tim_tuong(phe_sap_danh)
                self.thong_bao.config(text="GAME OVER", fg="#9b59b6")
                self.cap_nhat_ban_co() 
                
                if phe_sap_danh == "Do":
                    self.hien_thi_bang_ket_qua(self.ten_nguoi_choi_2, self.ten_nguoi_choi_1, "Đen", "Đỏ", "⚔️ Chiếu Bí!", f"Tướng của {self.ten_nguoi_choi_1} đã gục ngã!")
                else:
                    self.hien_thi_bang_ket_qua(self.ten_nguoi_choi_1, self.ten_nguoi_choi_2, "Đỏ", "Đen", "⚔️ Chiếu Bí!", f"Tướng của {self.ten_nguoi_choi_2} đã gục ngã!")
                return
                
            ds_chieu_tuong = self.game.kiem_tra_bi_chieu(phe_sap_danh)
            if len(ds_chieu_tuong) > 0:
                self.cap_nhat_ban_co() 
                messagebox.showwarning("Cảnh báo", f"Người chơi [{self.ten_nguoi_choi_1 if phe_sap_danh=='Do' else self.ten_nguoi_choi_2}] đang bị chiếu tướng!")
            else:
                self.cap_nhat_ban_co()

if __name__ == "__main__":
    root = tk.Tk()
    app = CoTuongGUI(root)
    root.mainloop()