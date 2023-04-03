import base64
from flask import Flask, request, make_response, render_template
import qrcode
import io
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)


def generate_qr_animation(input_text):
    # Generate the QR code image
    qr = qrcode.QRCode(version=1, box_size=5, border=5)
    qr.add_data(input_text)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Create a sequence of images with the QR code gradually revealed from top to bottom
    frame_duration = 0.05
    num_frames = qr_img.size[1]
    frames = []
    for i in range(num_frames):
        frame = Image.new('RGB', qr_img.size, color='white')
        draw = ImageDraw.Draw(frame)
        draw.rectangle([0, 0, qr_img.size[0], i], fill='black')
        frame.paste(qr_img, (0, 0), mask=qr_img)
        frames.append(frame)

    # Combine the frames into an animated GIF
    gif_bytes = io.BytesIO()
    frames[0].save(gif_bytes, format='GIF', append_images=frames[1:], save_all=True, duration=frame_duration*500)
    gif_bytes.seek(0)

    # Convert the animated GIF to base64 encoding
    gif_b64 = base64.b64encode(gif_bytes.getvalue()).decode('utf-8')

    return gif_b64

@app.route('/', methods=['GET', 'POST'])
def generate_qr():
    qr_code = None
    if request.method == 'POST':
        # Get the input text from the form data
        input_text = request.form['text']

        qr_code = generate_qr_animation(input_text)

    # Render the HTML template with the form
    return render_template('input.html', qr_code=qr_code)

if __name__ == '__main__':
    app.run(debug=True)
