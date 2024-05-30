import zmq
import os
import sys
import base64

# Server address
server_address = "tcp://4.tcp.eu.ngrok.io:14632"

# ZeroMQ creates context and socket 
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(server_address)

def upload_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
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
        print(f"{file_name} downloaded and saved as {save_path}.")
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

# Process arguments from the command line
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please enter a command: upload, download, delete, list_files, read_file, write_file, create_file")
        sys.exit(1)
    
    command = sys.argv[1]

    if command == "upload":
        if len(sys.argv) != 3:
            print("Usage: python client.py upload <file_path>")
            sys.exit(1)
        upload_file(sys.argv[2])
    elif command == "download":
        if len(sys.argv) != 4:
            print("Usage: python client.py download <file_name> <save_path>")
            sys.exit(1)
        download_file(sys.argv[2], sys.argv[3])
    elif command == "delete":
        if len(sys.argv) != 3:
            print("Usage: python client.py delete <file_name>")
            sys.exit(1)
        delete_file(sys.argv[2])
    elif command == "list_files":
        list_files()
    elif command == "read_file":
        if len(sys.argv) != 3:
            print("Usage: python client.py read_file <file_name>")
            sys.exit(1)
        read_file(sys.argv[2])
    elif command == "write_file":
        if len(sys.argv) != 4:
            print("Usage: python client.py write_file <file_name> <content>")
            sys.exit(1)
        write_file(sys.argv[2], sys.argv[3])
    elif command == "create_file":
        if len(sys.argv) != 4:
            print("Usage: python client.py create_file <file_name> <content>")
            sys.exit(1)
        create_file(sys.argv[2], sys.argv[3])
    else:
        print("Unknown command. Available commands: upload, download, delete, list_files, read_file, write_file, create_file")
