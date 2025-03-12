import cloudinary
from cloudinary.uploader import upload

#cloundinary configuration
cloudinary.config(
    cloud_name = "djgk66jji",
    api_key="975526958172616",
    api_secret="q1RrpqGCYt_TZka5HdZJ9kO_PsU"
)

#util functionn...

async def upload_image(image):
    result = upload(image)
    print("cloundianry response,",result)
    return result["secure_url"] #string
    