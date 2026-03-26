import io,logging,os,subprocess
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from PIL import Image
logger=logging.getLogger(__name__)
THUMBNAIL_SIZE=(400,400)
def validate_uploaded_file(file:UploadedFile,media_type:str)->None:
    ct=file.content_type or "";sz=(file.size or 0)/(1024*1024)
    if media_type in("image","gif"): allowed,mx=settings.ALLOWED_IMAGE_TYPES,settings.MAX_IMAGE_SIZE_MB
    elif media_type=="video": allowed,mx=settings.ALLOWED_VIDEO_TYPES,settings.MAX_VIDEO_SIZE_MB
    elif media_type=="doc": allowed,mx=settings.ALLOWED_DOCUMENT_TYPES,settings.MAX_DOCUMENT_SIZE_MB
    else: raise ValidationError(f"Unknown type: {media_type}")
    if ct not in allowed: raise ValidationError(f"Bad type: {ct}")
    if sz>mx: raise ValidationError(f"Too large: {sz:.1f}MB (max {mx})")
def create_image_thumbnail(fp,tp):
    try:
        os.makedirs(os.path.dirname(tp),exist_ok=True)
        with Image.open(fp) as img:
            img.thumbnail(THUMBNAIL_SIZE)
            if img.mode in("RGBA","P"): img=img.convert("RGB")
            img.save(tp,"JPEG",quality=85)
        return True
    except Exception: logger.exception("Thumb error %s",fp);return False
def create_video_thumbnail(fp,tp):
    try:
        os.makedirs(os.path.dirname(tp),exist_ok=True)
        subprocess.run(["ffmpeg","-i",fp,"-ss","00:00:01","-vframes","1","-vf",f"scale={THUMBNAIL_SIZE[0]}:-1","-y",tp],capture_output=True,timeout=30,check=True)
        return True
    except Exception: logger.exception("Video thumb error %s",fp);return False
def get_image_dimensions(file:UploadedFile):
    try:
        file.seek(0);img=Image.open(io.BytesIO(file.read()));w,h=img.size;file.seek(0);return w,h
    except Exception: return None,None
