import logging


logger = logging.getLogger(__name__)



def validate_image_format(image_data):
    """Validate image format from base64 string"""
    if not image_data.startswith('data:image/'):
        return False
    
    # Check for common image formats
    valid_formats = ['jpeg', 'jpg', 'png', 'gif', 'bmp', 'webp']
    for fmt in valid_formats:
        if f'image/{fmt}' in image_data:
            return True
    
    return False

