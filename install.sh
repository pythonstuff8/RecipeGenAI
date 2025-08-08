#!/bin/bash
set -e

echo "=== Updating system ==="
sudo apt update && sudo apt full-upgrade -y

echo "=== Installing packages ==="
sudo apt install -y hostapd dnsmasq python3-flask

# Unmask and disable services for manual control
sudo systemctl unmask hostapd
sudo systemctl disable hostapd
sudo systemctl disable dnsmasq

echo "=== Configuring dnsmasq ==="
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig || true
cat <<EOF | sudo tee /etc/dnsmasq.conf
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
EOF

echo "=== Configuring hostapd ==="
cat <<EOF | sudo tee /etc/hostapd/hostapd.conf
interface=wlan0
driver=nl80211
ssid=DoorbellSetup
hw_mode=g
channel=7
wmm_enabled=0
auth_algs=1
ignore_broadcast_ssid=0
EOF
sudo sed -i '/^#DAEMON_CONF/c\DAEMON_CONF="/etc/hostapd/hostapd.conf"' /etc/default/hostapd

echo "=== Creating Wi-Fi check script ==="
sudo tee /usr/local/bin/wifi-check.sh > /dev/null <<'EOF'
#!/bin/bash
if ! ping -c 1 -W 3 8.8.8.8 > /dev/null; then
    echo "No Wi-Fi, starting hotspot..."
    systemctl start hostapd
    systemctl start dnsmasq
else
    echo "Wi-Fi OK"
    systemctl stop hostapd
    systemctl stop dnsmasq
fi
EOF
sudo chmod +x /usr/local/bin/wifi-check.sh

echo "=== Adding Wi-Fi check to startup ==="
( sudo crontab -l 2>/dev/null; echo "@reboot /usr/local/bin/wifi-check.sh" ) | sudo crontab -

echo "=== Creating Flask Wi-Fi server ==="
sudo tee /home/pi/wifi_server.py > /dev/null <<'EOF'
from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/setwifi", methods=["POST"])
def setwifi():
    ssid = request.json.get("ssid")
    password = request.json.get("password")
    if not ssid or not password:
        return {"status": "error", "message": "Missing credentials"}, 400

    wpa_conf = f'''
network={{
    ssid="{ssid}"
    psk="{password}"
}}
'''
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a") as f:
        f.write(wpa_conf)

    subprocess.run(["wpa_cli", "-i", "wlan0", "reconfigure"])
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
EOF
sudo chown pi:pi /home/pi/wifi_server.py

echo "=== Creating systemd service for Flask ==="
sudo tee /etc/systemd/system/wifiserver.service > /dev/null <<EOF
[Unit]
Description=Wi-Fi Setup Server
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/wifi_server.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable wifiserver
sudo systemctl start wifiserver

echo "=== All done! ==="
echo "On next boot, Pi will start 'DoorbellSetup' AP if no Wi-Fi is connected."
echo "Clearing saved Wi-Fi credentials..."
sudo tee /etc/wpa_supplicant/wpa_supplicant.conf > /dev/null <<EOF
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US
EOF
sudo wpa_cli -i wlan0 reconfigure
