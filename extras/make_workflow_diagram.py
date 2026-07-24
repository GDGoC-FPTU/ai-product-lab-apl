"""
Sinh file 04-workflow-diagram.png — Sơ đồ Current-State Workflow (Phase 3.1).

Bài toán: Xanh SM (GSM) — Xử lý sự cố pin thấp / cạn pin của tài xế giữa ca.

Sơ đồ dùng swimlane 3 làn (Tài xế / Điều phối viên / Hệ thống) để làm nổi bật
các điểm chuyển giao thông tin (handoff), thời gian từng bước và 2 nút thắt cổ chai.

Lưu ý về mô hình hoá: B3+B4 (tìm trạm & soạn tin chỉ đường) và B5 (điều xe sạc di động)
LOẠI TRỪ NHAU theo chính ranh giới pin < 5% của nhóm, nên sơ đồ có nhánh quyết định và
KHÔNG cộng thẳng cả 5 bước thành một con số duy nhất.

Chạy:  python extras/make_workflow_diagram.py
Xuất:  04-workflow-diagram.png (thư mục gốc repo)
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

plt.rcParams["font.family"] = "DejaVu Sans"

OUT_PATH = Path(__file__).resolve().parent.parent / "04-workflow-diagram.png"

# ---------------------------------------------------------------- bảng màu
INK = "#1B262C"
MUTED = "#5A6B75"
STEP_FILL, STEP_EDGE = "#DCE9F7", "#2A5D9F"
BNECK_FILL, BNECK_EDGE = "#FBDAD3", "#C0392B"
SYS_FILL, SYS_EDGE = "#ECEFF1", "#78909C"
OUT_FILL, OUT_EDGE = "#DCF2E3", "#1E8449"
HAND_FILL, HAND_EDGE = "#FDF3C7", "#B7791F"
DEC_FILL, DEC_EDGE = "#EAE2F8", "#6C3FB8"
LANE_FILLS = ["#F7FAFD", "#FDFAF6", "#F6F8F8"]

fig, ax = plt.subplots(figsize=(17.5, 9.8), dpi=150)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")
fig.patch.set_facecolor("white")


# ---------------------------------------------------------------- helpers
def lane(y0, y1, label, sub, idx):
    ax.add_patch(Rectangle((1, y0), 98, y1 - y0, facecolor=LANE_FILLS[idx],
                           edgecolor="#C9D3DA", linewidth=1.0, zorder=0))
    ax.add_patch(Rectangle((1, y0), 13, y1 - y0, facecolor="#E3EAEF",
                           edgecolor="#C9D3DA", linewidth=1.0, zorder=1))
    ax.text(7.5, (y0 + y1) / 2 + 2.0, label, ha="center", va="center",
            fontsize=9.8, fontweight="bold", color=INK, zorder=2, linespacing=1.4)
    ax.text(7.5, (y0 + y1) / 2 - 2.8, sub, ha="center", va="center",
            fontsize=7.2, color=MUTED, zorder=2, linespacing=1.35)


def box(cx, cy, w, h, title, body, fill, edge, lw=1.6, dashed=False, badge=None):
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0.35,rounding_size=1.1",
        facecolor=fill, edgecolor=edge, linewidth=lw,
        linestyle="--" if dashed else "-", zorder=3))
    ax.text(cx, cy + h / 2 - 2.4, title, ha="center", va="center",
            fontsize=9.2, fontweight="bold", color=INK, zorder=4, linespacing=1.3)
    ax.text(cx, cy - 2.5, body, ha="center", va="center",
            fontsize=7.5, color=MUTED, zorder=4, linespacing=1.5)
    if badge:
        ax.add_patch(FancyBboxPatch(
            (cx - w / 2 + 0.5, cy + h / 2 - 1.3), 11.4, 2.6,
            boxstyle="round,pad=0.15,rounding_size=0.6",
            facecolor=BNECK_EDGE, edgecolor="none", zorder=5))
        ax.text(cx - w / 2 + 6.2, cy + h / 2 + 0.05, badge, ha="center", va="center",
                fontsize=7.0, fontweight="bold", color="white", zorder=6)


def diamond(cx, cy, w, h, label):
    ax.add_patch(Polygon([[cx, cy + h / 2], [cx + w / 2, cy], [cx, cy - h / 2], [cx - w / 2, cy]],
                         closed=True, facecolor=DEC_FILL, edgecolor=DEC_EDGE,
                         linewidth=1.8, zorder=4))
    ax.text(cx, cy, label, ha="center", va="center", fontsize=7.4,
            fontweight="bold", color=DEC_EDGE, zorder=5, linespacing=1.3)


def arrow(p0, p1, color=STEP_EDGE, dashed=False, rad=0.0, lw=1.8):
    ax.add_patch(FancyArrowPatch(
        p0, p1, arrowstyle="-|>", mutation_scale=14, linewidth=lw,
        color=color, linestyle="--" if dashed else "-",
        connectionstyle=f"arc3,rad={rad}", zorder=2,
        shrinkA=2, shrinkB=2))


def handoff(x, y, tag, text):
    ax.add_patch(FancyBboxPatch(
        (x - 9.2, y - 2.1), 18.4, 4.2,
        boxstyle="round,pad=0.22,rounding_size=0.8",
        facecolor=HAND_FILL, edgecolor=HAND_EDGE, linewidth=1.2, zorder=7))
    ax.text(x, y + 0.75, f"⇄  HANDOFF {tag}", ha="center", va="center",
            fontsize=7.3, fontweight="bold", color="#8A5A00", zorder=8)
    ax.text(x, y - 1.15, text, ha="center", va="center",
            fontsize=6.9, color="#7A5200", zorder=8)


# ---------------------------------------------------------------- tiêu đề
ax.text(50, 97.6, "SƠ ĐỒ QUY TRÌNH HIỆN TẠI  —  CURRENT-STATE WORKFLOW",
        ha="center", va="center", fontsize=17.5, fontweight="bold", color=INK)
ax.text(50, 94.2,
        "Xanh SM (GSM) · Xử lý sự cố pin thấp / cạn pin của tài xế giữa ca   |   "
        "Vin Smart Future — Lab 02, Phase 3.1",
        ha="center", va="center", fontsize=10.2, color=MUTED)

# ---------------------------------------------------------------- swimlanes
lane(71.0, 91.0, "TÀI XẾ", "Ngoài đường,\nxe đang thấp pin", 0)
lane(44.0, 69.5, "ĐIỀU PHỐI VIÊN", "Trung tâm Điều vận\n(người làm chính)", 1)
lane(22.0, 42.5, "HỆ THỐNG /\nCÔNG CỤ", "Các màn hình rời rạc,\nkhông nối với nhau", 2)

Y_DRV, Y_DIS, Y_SYS = 80.0, 57.5, 32.2
BH_DRV, BH_DIS, BH_SYS = 13.5, 17.5, 13.0
W = 12.4
HW = W / 2 + 0.35

# ---------------------------------------------------------------- các bước
box(22, Y_DRV, W, BH_DRV, "B1 · Báo sự cố",
    "Tài xế gọi tổng đài báo pin\nthấp, đọc biển số & vị trí\n\n~2 phút",
    STEP_FILL, STEP_EDGE)

box(35, Y_DIS, W, BH_DIS, "B2 · Tra định vị xe",
    "ĐPV nhập biển số, tra toạ độ\nGPS trên dashboard nội bộ\n\n~2 phút",
    STEP_FILL, STEP_EDGE)

diamond(45.5, Y_DIS, 5.6, 9.2, "pin\n< 5% ?")

box(57.5, Y_DIS, W, BH_DIS, "B3 · Tìm trụ sạc trống",
    "Đổi tab, dò trạm còn trụ trống\nĐÚNG chuẩn cổng sạc của\ndòng xe, đối chiếu bằng mắt\n\n~5 phút",
    BNECK_FILL, BNECK_EDGE, lw=2.4, badge="BOTTLENECK")

box(74, Y_DIS, W, BH_DIS, "B4 · Soạn tay tin chỉ dẫn",
    "Viết tin tiếng Việt: đường đi,\nsố trụ, lưu ý pin — gõ tay\ntừ đầu cho từng ca\n\n~4 phút",
    BNECK_FILL, BNECK_EDGE, lw=2.4, badge="BOTTLENECK")

box(90.5, Y_DIS, W, BH_DIS, "B5 · Điều xe sạc di động",
    "Gọi thoại đội xe sạc di động.\nLOẠI TRỪ với B3+B4 — xe pin\n<5% không được chỉ đi xa\n\n~2 phút",
    STEP_FILL, STEP_EDGE)

box(90.5, Y_DRV, W, BH_DRV, "Kết quả với tài xế",
    "Nhận chỉ dẫn ở phút ~13\n(thời gian THAO TÁC, chưa\ntính chờ hàng đợi)",
    OUT_FILL, OUT_EDGE, dashed=True)

box(35, Y_SYS, W, BH_SYS, "Dashboard định vị",
    "Hệ thống theo dõi\nđội xe (nội bộ)", SYS_FILL, SYS_EDGE, dashed=True)
box(57.5, Y_SYS, W, BH_SYS, "Dashboard trạm sạc",
    "Trang tra trụ sạc\nVinFast — tab riêng,\ncập nhật có độ trễ", SYS_FILL, SYS_EDGE, dashed=True)
box(90.5, Y_SYS, W, BH_SYS, "Tổng đài đội cứu hộ",
    "Kênh thoại riêng,\nkhông ghi vào ticket", SYS_FILL, SYS_EDGE, dashed=True)

# ---------------------------------------------------------------- mũi tên
TOP_DIS, BOT_DIS = Y_DIS + BH_DIS / 2, Y_DIS - BH_DIS / 2
arrow((22, Y_DRV - BH_DRV / 2), (30.0, TOP_DIS - 0.8), rad=-0.16)     # B1 -> B2
arrow((35 + HW, Y_DIS), (42.4, Y_DIS))                                # B2 -> quyết định
arrow((48.6, Y_DIS), (57.5 - HW, Y_DIS))                              # quyết định -> B3
ax.text(49.9, Y_DIS + 3.4, "pin ≥ 5%", ha="center", va="center",
        fontsize=6.8, fontweight="bold", color=DEC_EDGE, zorder=6)
arrow((57.5 + HW, Y_DIS), (74 - HW, Y_DIS))                           # B3 -> B4
arrow((74 + HW, Y_DIS), (90.5 - HW, Y_DIS), dashed=True, color=MUTED)  # B4 -> B5 (hiếm)
arrow((77.5, TOP_DIS), (88.5, Y_DRV - BH_DRV / 2), rad=0.16, color=OUT_EDGE)  # B4 -> tài xế

# nhánh pin < 5%: bỏ qua hoàn toàn B3 + B4
BR_Y = 47.2
ax.plot([45.5, 45.5, 86.5], [Y_DIS - 4.5, BR_Y, BR_Y],
        color=DEC_EDGE, linewidth=1.8, linestyle="--", zorder=2)
arrow((86.5, BR_Y), (86.5, BOT_DIS), color=DEC_EDGE, dashed=True)
ax.text(73.0, 45.9, "pin < 5%  →  bỏ qua B3 + B4",
        ha="center", va="center", fontsize=7.0, fontweight="bold",
        color=DEC_EDGE, zorder=9)

# vòng làm lại (rework)
ax.plot([90.5, 90.5, 22, 22], [Y_DRV + BH_DRV / 2, 88.8, 88.8, Y_DRV + BH_DRV / 2],
        color="#B7791F", linewidth=1.5, linestyle=":", zorder=2)
arrow((22.6, 88.8), (22, Y_DRV + BH_DRV / 2), color="#B7791F", dashed=True, lw=1.5)
ax.text(56, 89.9, "↩  REWORK — tài xế tới nơi thì trụ đã bị chiếm / sai chuẩn cổng sạc → "
                  "báo lại từ đầu với mức pin thấp hơn (tỉ lệ r CHƯA ĐO)",
        ha="center", va="center", fontsize=6.9, fontweight="bold", color="#8A5A00", zorder=6)

for x in (35, 57.5, 90.5):
    arrow((x - 1.1, BOT_DIS), (x - 1.1, Y_SYS + BH_SYS / 2), dashed=True, color=SYS_EDGE, lw=1.4)
    arrow((x + 1.1, Y_SYS + BH_SYS / 2), (x + 1.1, BOT_DIS), dashed=True, color=SYS_EDGE, lw=1.4)

# ---------------------------------------------------------------- handoff
handoff(27.0, 70.2, "H1", "Thoại: biển số & vị trí đọc bằng lời")
handoff(35, 43.2, "H2", "Gõ tay biển số vào dashboard")
handoff(56.5, 43.2, "H3", "Đổi tab, đối chiếu bằng mắt")
handoff(90.5, 43.2, "H4", "Gọi thoại, không ghi lại ticket")
handoff(66.0, 70.2, "H5", "Gửi tin qua App — không có xác nhận đã đọc")

# ---------------------------------------------------------------- timeline
TL_X0, TL_X1 = 17.0, 92.0
SPAN = TL_X1 - TL_X0
REF = 13.0   # trục chung: phút

ax.text(1.5, 20.2, "DÒNG THỜI GIAN THEO TỪNG NHÁNH (thời gian thao tác, ước lượng)",
        ha="left", va="center", fontsize=9.2, fontweight="bold", color=INK)


def timeline(y, h, steps, label, total_note):
    ax.text(1.5, y + h / 2, label, ha="left", va="center",
            fontsize=7.6, fontweight="bold", color=INK)
    x = TL_X0
    for name, minutes, is_bneck in steps:
        w = SPAN * minutes / REF
        ax.add_patch(Rectangle((x, y), w, h,
                               facecolor=BNECK_EDGE if is_bneck else STEP_EDGE,
                               edgecolor="white", linewidth=1.4, zorder=3))
        ax.text(x + w / 2, y + h / 2, f"{name}·{minutes}′", ha="center", va="center",
                fontsize=7.4, fontweight="bold", color="white", zorder=4)
        x += w
    ax.text(x + 0.8, y + h / 2, total_note, ha="left", va="center",
            fontsize=8.2, fontweight="bold", color=INK)


timeline(15.4, 3.2,
         [("B1", 2, False), ("B2", 2, False), ("B3", 5, True), ("B4", 4, True)],
         "Nhánh THƯỜNG\n(pin ≥ 5%)", "= 13 phút")
timeline(11.0, 3.2,
         [("B1", 2, False), ("B2", 2, False), ("tin ngắn", 2, False), ("B5", 2, False)],
         "Nhánh NGUY CẤP\n(pin < 5%)", "≈ 8 phút")

ax.text(TL_X0 + SPAN * 8.5 / 13, 8.6,
        "B3 + B4 = 9/13 phút  →  69% thời gian nhánh thường nằm ở 2 nút thắt      "
        "|      E[T] = 13·(1−q) + 8·q  với q = tỉ lệ ca pin < 5% (CHƯA ĐO)",
        ha="center", va="center", fontsize=7.8, fontweight="bold", color=BNECK_EDGE)

# ---------------------------------------------------------------- chú giải
ax.add_patch(FancyBboxPatch((1, 0.4), 55, 7.0, boxstyle="round,pad=0.3,rounding_size=0.8",
                            facecolor="#FBFCFD", edgecolor="#C9D3DA", linewidth=1.0, zorder=3))
ax.text(2.8, 6.4, "CHÚ GIẢI", fontsize=8.2, fontweight="bold", color=INK, va="center", zorder=4)
legend = [
    (STEP_FILL, STEP_EDGE, "-", "Bước thủ công bình thường"),
    (BNECK_FILL, BNECK_EDGE, "-", "Nút thắt cổ chai (bottleneck)"),
    (SYS_FILL, SYS_EDGE, "--", "Hệ thống / công cụ rời rạc"),
    (HAND_FILL, HAND_EDGE, "-", "⇄  Điểm chuyển giao (handoff)"),
]
for i, (fill, edge, ls, label) in enumerate(legend):
    lx = 2.8 + (i % 2) * 26.5
    ly = 3.4 - (i // 2) * 2.7
    ax.add_patch(FancyBboxPatch((lx, ly), 2.6, 1.8, boxstyle="round,pad=0.12,rounding_size=0.4",
                                facecolor=fill, edgecolor=edge, linewidth=1.4, linestyle=ls, zorder=4))
    ax.text(lx + 3.7, ly + 0.9, label, fontsize=7.3, color=MUTED, va="center", zorder=4)

ax.add_patch(FancyBboxPatch((58, 0.4), 41, 7.0, boxstyle="round,pad=0.3,rounding_size=0.8",
                            facecolor="#FFF9E8", edgecolor="#E0C878", linewidth=1.0, zorder=3))
ax.text(59.8, 6.4, "GIẢ ĐỊNH CẦN XÁC THỰC", fontsize=8.2, fontweight="bold",
        color="#8A5A00", va="center", zorder=4)
ax.text(59.8, 5.1,
        "Mọi con số thời gian là ƯỚC LƯỢNG phục vụ scoping trong Lab, chưa phải\n"
        "số đo từ hệ thống BI của Vingroup. Cách xác thực: trích log tổng đài + log\n"
        "ticket điều vận, đo phân phối thời gian thật từng bước trước khi chốt baseline.",
        fontsize=7.2, color="#7A5200", va="top", ha="left", zorder=4, linespacing=1.65)

fig.savefig(OUT_PATH, dpi=150, bbox_inches="tight", facecolor="white", pad_inches=0.25)
print(f"[OK] Da xuat so do: {OUT_PATH}")
