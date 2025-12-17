import cloudinary.uploader
from dotenv import load_dotenv
import os

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

DEFAULT_IMAGE = os.getenv("DEFAULT_PRODUCT_IMAGE")
DEFAULT_USER_IMAGE = os.getenv("DEFAULT_USER_IMAGE")


def upload_image(file, default_type: str = "product"):
    if file:
        result = cloudinary.uploader.upload(file.file)
        return result["secure_url"]
    else:
        return DEFAULT_USER_IMAGE if default_type == "user" else DEFAULT_IMAGE
