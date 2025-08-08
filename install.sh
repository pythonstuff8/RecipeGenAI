#!/bin/bash
set -e

echo "[1/7] Updating system..."
sudo apt update && sudo apt upgrade -y

echo "[2/7] Installing required packages..."
sudo apt install -y hostapd dnsmasq python3-flask network-manager

echo "[3/7] Disabling default hostapd/dnsmasq services..."
sudo systemctl stop hostapd || true
sudo systemctl stop dnsmasq || true
sudo systemctl disable hostapd || true
sudo systemctl disable dnsmasq || true

echo "[4/7] Configuring static IP for AP mode..."
sudo bash -c 'cat >> /etc/dhcpcd.conf <<EOF
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
EOF'

echo "[5/7] Setting up dnsmasq..."
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo bash -c 'cat > /etc/dnsmasq.conf <<EOF
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
EOF'

echo "[6/7] Setting up hostapd..."
sudo bash -c 'cat > /etc/hostapd/hostapd.conf <<EOF
interface=wlan0
driver=nl80211
ssid=Doorbell-Setup
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=12345678
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
EOF'
sudo sed -i 's|#DAEMON_CONF=""|DAEMON_CONF="/etc/hostapd/hostapd.conf"|' /etc/default/hostapd

echo "[7/7] Installing Wi-Fi manager scripts..."
sudo mkdir -p /opt/wifi_provision
sudo bash -c 'cat > /opt/wifi_provision/server.py <<EOF
from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/configure", methods=["POST"])
def configure_wifi():
    data = request.json
    ssid = data.get("ssid")
    password = data.get("password")
    if not ssid or not password:
        return {"status": "error", "message": "Missing SSID or password"}, 400
    subprocess.run(["nmcli", "dev", "wifi", "connect", ssid, "password", password])
    return {"status": "ok", "message": "Wi-Fi credentials received"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
EOF'

sudo bash -c 'cat > /opt/wifi_provision/wifi_manager.sh <<EOF
#!/bin/bash
SSID=\$(nmcli -t -f ACTIVE,SSID dev wifi | grep "^yes" | cut -d: -f2)
if [ -z "\$SSID" ]; then
    echo "No Wi-Fi, starting AP mode..."
    sudo systemctl stop NetworkManager
    sudo systemctl start dnsmasq
    sudo systemctl start hostapd
    python3 /opt/wifi_provision/server.py
else
    echo "Connected to \$SSID"
    sudo systemctl stop dnsmasq
    sudo systemctl stop hostapd
    sudo systemctl start NetworkManager
fi
EOF'
sudo chmod +x /opt/wifi_provision/wifi_manager.sh

# Run at boot
(crontab -l 2>/dev/null; echo "@reboot /opt/wifi_provision/wifi_manager.sh") | crontab -

echo "✅ Installation complete. Rebooting..."
sudo reboot
