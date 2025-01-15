import yaml
import base64
import json
import pyfiglet
from colorama import init, Fore, Style

# Inisialisasi colorama untuk warna
init(autoreset=True)

def display_banner():
    """Menampilkan banner menggunakan pyfiglet"""
    banner = pyfiglet.figlet_format("Clash Config Generator")
    print(Fore.CYAN + banner)

def vless_to_clash(vless_link):
    """Mengonversi tautan VLESS menjadi struktur YAML untuk Clash"""
    try:
        parts = vless_link.replace("vless://", "").split("@")
        user_id = parts[0]
        server_part = parts[1].split(":")
        server = server_part[0]
        port = server_part[1].split("?")[0]

        # Struktur YAML untuk Clash
        return {
            "proxies": [
                {
                    "name": "VLESS Proxy",
                    "type": "vless",
                    "server": server,
                    "port": int(port),
                    "uuid": user_id,
                    "encryption": "none",
                    "tls": True,
                    "skip-cert-verify": True,
                    "servername": server,
                    "network": "ws",
                    "ws-opts": {
                        "path": "/?ed=2048",
                        "headers": {
                            "Host": server
                        }
                    }
                }
            ],
            "proxy-groups": [
                {
                    "name": "Auto",
                    "type": "select",
                    "proxies": ["VLESS Proxy"]
                }
            ],
            "rules": [
                "MATCH,Auto"
            ]
        }
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        return None

def vmess_to_clash(vmess_link):
    """Mengonversi tautan VMESS menjadi struktur YAML untuk Clash"""
    try:
        vmess_data = json.loads(base64.b64decode(vmess_link.replace("vmess://", "")).decode('utf-8'))
        
        # Struktur YAML untuk Clash
        return {
            "proxies": [
                {
                    "name": "VMESS Proxy",
                    "type": "vmess",
                    "server": vmess_data.get("add"),
                    "port": int(vmess_data.get("port")),
                    "uuid": vmess_data.get("id"),
                    "alterId": int(vmess_data.get("aid", 0)),
                    "cipher": vmess_data.get("scy", "auto"),
                    "tls": vmess_data.get("tls") == "tls",
                    "skip-cert-verify": True,
                    "network": vmess_data.get("net", "ws"),
                    "ws-opts": {
                        "path": vmess_data.get("path", "/"),
                        "headers": {
                            "Host": vmess_data.get("host", vmess_data.get("add"))
                        }
                    }
                }
            ],
            "proxy-groups": [
                {
                    "name": "Auto",
                    "type": "select",
                    "proxies": ["VMESS Proxy"]
                }
            ],
            "rules": [
                "MATCH,Auto"
            ]
        }
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        return None

def save_to_yaml(data, filename):
    """Menyimpan konfigurasi YAML ke file"""
    try:
        with open(filename, "w") as file:
            yaml.dump(data, file, default_flow_style=False)
        print(Fore.GREEN + f"File berhasil disimpan sebagai {filename}")
    except Exception as e:
        print(Fore.RED + f"Error saat menyimpan file: {e}")

def main():
    display_banner()

    while True:
        print(Fore.YELLOW + "Pilih jenis tautan:")
        print("1. VLESS")
        print("2. VMESS")
        print("3. Keluar")

        choice = input(Fore.GREEN + "Masukkan pilihan (1/2/3): ").strip()

        if choice == "1":
            vless_link = input(Fore.CYAN + "Masukkan tautan VLESS (contoh: vless://uuid@host:port): ").strip()
            config = vless_to_clash(vless_link)
            if config:
                save_to_yaml(config, "clash_config_vless.yaml")

        elif choice == "2":
            vmess_link = input(Fore.CYAN + "Masukkan tautan VMESS (contoh: vmess://base64_encoded_json): ").strip()
            config = vmess_to_clash(vmess_link)
            if config:
                save_to_yaml(config, "clash_config_vmess.yaml")

        elif choice == "3":
            print(Fore.MAGENTA + "Keluar dari program...")
            break

        else:
            print(Fore.RED + "Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
