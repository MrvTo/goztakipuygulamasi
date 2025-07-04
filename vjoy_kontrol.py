import pyvjoy
import socket

j = pyvjoy.VJoyDevice(1)

def to_vjoy_axis(value):
    value = max(min(value, 1.0), -1.0)
    return int((value + 1) * 0.5 * 32768)
#gonderenialan
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
#gondericiden mesaj gelene kadar yazdır
print("UDP dinleniyor...")

while True:
    data, _ = sock.recvfrom(1024)
    try:
        x_str, y_str = data.decode().split(",")
        x = float(x_str)
        y = float(y_str)

        # Terslikleri düzelt
        j.data.wAxisX = to_vjoy_axis(-x)  # Ters çünkü mini sorun var
        j.data.wAxisY = to_vjoy_axis(-y) 
        j.update()

        print(f"Güncellendi: X={x:.2f}, Y={y:.2f}")
    except Exception as e:
        print("Veri hatalı:", e)
