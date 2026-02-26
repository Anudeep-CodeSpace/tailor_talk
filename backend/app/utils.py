import base64
import os
from typing import Optional

def encode_image_to_base64(filepath: str) -> Optional[str]:
    '''
    Reads an image file, encodes it to base64 and deletes the file to save space.
    '''
    if not os.path.exists(filepath):
        return None
    
    try:
        with open(filepath, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        # Cleanup
        os.remove(filepath)

        return encoded_string
    
    except Exception as e:
        print(f'[ERROR] Unable to Encode Image: {e}')
        return None