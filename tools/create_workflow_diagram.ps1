Add-Type -AssemblyName System.Drawing

$width = 1800; $height = 760
$bitmap = New-Object System.Drawing.Bitmap $width, $height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.Clear([System.Drawing.Color]::White)
$title = New-Object System.Drawing.Font 'Segoe UI', 25, ([System.Drawing.FontStyle]::Bold)
$font = New-Object System.Drawing.Font 'Segoe UI', 15
$small = New-Object System.Drawing.Font 'Segoe UI', 13
$brush = [System.Drawing.Brushes]::Black
$graphics.DrawString('Xanh SM — Current-State Workflow: xử lý sự cố pin yếu', $title, $brush, 48, 35)
$graphics.DrawString('🔄 Handoff  •  🔴 Bottleneck  •  Tổng thời gian trung bình: 21 phút/case', $font, $brush, 50, 90)

$steps = @(
    @{ x=50;   title='1. Nhận báo sự cố'; body='Tài xế gọi/chat tổng đài`nDispatcher ghi biển số`n⏱ 2 phút'; red=$false },
    @{ x=400;  title='2. Xác minh GPS & SOC'; body='Mở dashboard xe`nKiểm tra vị trí và mức pin`n⏱ 3 phút'; red=$false },
    @{ x=750;  title='3. Tra trạm sạc'; body='Tra cứu trạm còn chỗ`nSo khoảng cách và mức pin`n⏱ 6 phút  🔴'; red=$true },
    @{ x=1100; title='4. Soạn hướng dẫn'; body='Viết chỉ dẫn cho tài xế`nhoặc liên hệ cứu hộ`n⏱ 7 phút  🔴'; red=$true },
    @{ x=1450; title='5. Gửi & ghi log'; body='Gửi qua app/điện thoại`nCập nhật ticket sự cố`n⏱ 3 phút'; red=$false }
)

foreach ($step in $steps) {
    $fill = if ($step.red) { [System.Drawing.Color]::FromArgb(255,245,235) } else { [System.Drawing.Color]::FromArgb(237,246,255) }
    $outline = if ($step.red) { [System.Drawing.Color]::Firebrick } else { [System.Drawing.Color]::SteelBlue }
    $rect = New-Object System.Drawing.Rectangle $step.x, 210, 280, 250
    $graphics.FillRectangle((New-Object System.Drawing.SolidBrush $fill), $rect)
    $graphics.DrawRectangle((New-Object System.Drawing.Pen $outline, 4), $rect)
    $graphics.DrawString($step.title, $font, $brush, $step.x + 16, 235)
    $graphics.DrawString($step.body, $small, $brush, $step.x + 16, 290)
}

$pen = New-Object System.Drawing.Pen ([System.Drawing.Color]::DimGray), 4
for ($i=0; $i -lt 4; $i++) {
    $x1 = $steps[$i].x + 280; $x2 = $steps[$i+1].x
    $graphics.DrawLine($pen, $x1, 335, $x2 - 18, 335)
    $graphics.FillPolygon([System.Drawing.Brushes]::DimGray, [System.Drawing.Point[]]@((New-Object System.Drawing.Point ($x2 - 18),325),(New-Object System.Drawing.Point $x2,335),(New-Object System.Drawing.Point ($x2 - 18),345)))
    $graphics.DrawString('🔄 Handoff', $small, $brush, $x1 + 35, 480)
}

$note = 'Điểm nghẽn: dispatcher phải chuyển giữa GPS, dữ liệu trạm và kênh liên lạc; lựa chọn sai ở mức pin thấp có rủi ro vận hành.'
$graphics.DrawString($note, $font, $brush, 50, 580)
$graphics.DrawString('Nguồn: workflow baseline giả định cho bài lab — cần xác thực bằng log vận hành trước khi pilot.', $small, $brush, 50, 640)
$bitmap.Save((Join-Path $PSScriptRoot '..\04-workflow-diagram.png'), [System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose(); $bitmap.Dispose()
