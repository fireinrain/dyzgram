import qrcode
from qrcode.main import QRCode


def gen_qrcode_print(login_token: str):
    qr = QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.clear()
    qr.add_data(login_token)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.show()


def display_url_as_qrcode(url):
    print(url)  # do whatever to show url as a qr to the user
    gen_qrcode_print(url)
