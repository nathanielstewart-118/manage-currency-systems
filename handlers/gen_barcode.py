import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64

# Generate barcode in memory
def generate_barcode_base64(data):
    barcode_class = barcode.get_barcode_class('code128')
    buffer = BytesIO()
    barcode_class(data, writer=ImageWriter()).write(buffer)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')
