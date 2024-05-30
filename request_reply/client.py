import zmq
import os
import sys
import base64

# Sunucu adresi
server_address = "tcp://4.tcp.eu.ngrok.io:14632"

# ZeroMQ context ve socket oluştur
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(server_address)

def upload_file(file_path):
    if not os.path.exists(file_path):
        print(f"Dosya bulunamadı: {file_path}")
        return
    
    with open(file_path, "rb") as f:
        file_content = base64.b64encode(f.read()).decode()

    file_name = os.path.basename(file_path)

    socket.send_json({"command": "upload", "file_name": file_name, "file_content": file_content})
    response = socket.recv_json()
    print(response)

def download_file(file_name, save_path):
    socket.send_json({"command": "download", "file_name": file_name})
    response = socket.recv_json()

    if response.get("status") == "success":
        file_content = base64.b64decode(response.get("file_content"))
        with open(save_path, "wb") as f:
            f.write(file_content)
        print(f"{file_name} indirildi ve {save_path} olarak kaydedildi.")
    else:
        print(response.get("message"))

def delete_file(file_name):
    socket.send_json({"command": "delete", "file_name": file_name})
    response = socket.recv_json()
    print(response)

def list_files():
    socket.send_json({"command": "list_files"})
    response = socket.recv_json()
    if response.get("status") == "success":
        files = response.get("files")
        for file in files:
            print(file)
    else:
        print(response.get("message"))

def read_file(file_name):
    socket.send_json({"command": "read_file", "file_name": file_name})
    response = socket.recv_json()
    if response.get("status") == "success":
        file_content = response.get("file_content")
        print(file_content)
    else:
        print(response.get("message"))

def write_file(file_name, content):
    socket.send_json({"command": "write_file", "file_name": file_name, "content": content})
    response = socket.recv_json()
    print(response)

def create_file(file_name, content):
    socket.send_json({"command": "create_file", "file_name": file_name, "content": content})
    response = socket.recv_json()
    print(response)

# Komut satırından argümanları işleme
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Lütfen bir komut girin: upload, download, delete, list_files, read_file, write_file, create_file")
        sys.exit(1)
    
    command = sys.argv[1]

    if command == "upload":
        if len(sys.argv) != 3:
            print("Kullanım: python client.py upload <dosya_yolu>")
            sys.exit(1)
        upload_file(sys.argv[2])
    elif command == "download":
        if len(sys.argv) != 4:
            print("Kullanım: python client.py download <dosya_adı> <kaydetme_yolu>")
            sys.exit(1)
        download_file(sys.argv[2], sys.argv[3])
    elif command == "delete":
        if len(sys.argv) != 3:
            print("Kullanım: python client.py delete <dosya_adı>")
            sys.exit(1)
        delete_file(sys.argv[2])
    elif command == "list_files":
        list_files()
    elif command == "read_file":
        if len(sys.argv) != 3:
            print("Kullanım: python client.py read_file <dosya_adı>")
            sys.exit(1)
        read_file(sys.argv[2])
    elif command == "write_file":
        if len(sys.argv) != 4:
            print("Kullanım: python client.py write_file <dosya_adı> <içerik>")
            sys.exit(1)
        write_file(sys.argv[2], sys.argv[3])
    elif command == "create_file":
        if len(sys.argv) != 4:
            print("Kullanım: python client.py create_file <dosya_adı> <içerik>")
            sys.exit(1)
        create_file(sys.argv[2], sys.argv[3])
    else:
        print("Bilinmeyen komut. Kullanılabilir komutlar: upload, download, delete, list_files, read_file, write_file, create_file")