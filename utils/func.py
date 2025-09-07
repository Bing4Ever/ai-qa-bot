import base64
import hashlib
from pathlib  import Path

def save_image_local(uploaded_file, save_dir = "uploads/invoice") -> str:
    base_dir = Path(__file__).resolve().parent.parent
    abs_save_dir = base_dir / save_dir
    abs_save_dir.mkdir(parents=True, exist_ok=True)

    file_bytes = uploaded_file.getvalue()
    base64_image = base64.b64encode(file_bytes)
    file_hash = hashlib.md5(base64_image).hexdigest()
    file_ext = uploaded_file.name.split(".")[-1]
    file_name = f"{file_hash}.{file_ext}"
    file_path = abs_save_dir / file_name
    
    if not file_path.exists():
        with open(file_path, "wb") as f:
            f.write(file_bytes)

    return str(file_path)  