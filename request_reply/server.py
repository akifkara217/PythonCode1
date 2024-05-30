import zmq
import os
import base64

bind_address = "tcp://0.0.0.0:5555"
upload_dir = "uploads"

if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(bind_address)

print("Server started and waiting...")

while True:
    message = socket.recv_json()

    command = message.get("command")

    if command == "upload":
        file_name = message.get("file_name")
        file_content = base64.b64decode(message.get("file_content"))

        with open(os.path.join(upload_dir, file_name), "wb") as f:
            f.write(file_content)
        
        socket.send_json({"status": "success", "message": f"{file_name} uploaded."})

    elif command == "download":
        file_name = message.get("file_name")
        file_path = os.path.join(upload_dir, file_name)

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                file_content = base64.b64encode(f.read()).decode()

            socket.send_json({"status": "success", "file_content": file_content})
        else:
            socket.send_json({"status": "error", "message": f"{file_name} not found."})

    elif command == "delete":
        file_name = message.get("file_name")
        file_path = os.path.join(upload_dir, file_name)

        if os.path.exists(file_path):
            os.remove(file_path)
            socket.send_json({"status": "success", "message": f"{file_name} deleted."})
        else:
            socket.send_json({"status": "error", "message": f"{file_name} not found."})

    elif command == "list_files":
        files = os.listdir(upload_dir)
        socket.send_json({"status": "success", "files": files})

    elif command == "read_file":
        file_name = message.get("file_name")
        file_path = os.path.join(upload_dir, file_name)

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                file_content = f.read()

            socket.send_json({"status": "success", "file_content": file_content})
        else:
            socket.send_json({"status": "error", "message": f"{file_name} not found."})

    elif command == "write_file":
        file_name = message.get("file_name")
        content = message.get("content")

        with open(os.path.join(upload_dir, file_name), "w") as f:
            f.write(content)

        socket.send_json({"status": "success", "message": f"{file_name} created and content written."})

    elif command == "create_file":
        file_name = message.get("file_name")
        content = message.get("content")

        with open(os.path.join(upload_dir, file_name), "w") as f:
            f.write(content)

        socket.send_json({"status": "success", "message": f"{file_name} created and content written."})

    else:
        socket.send_json({"status": "error", "message": "Unknown command."})
