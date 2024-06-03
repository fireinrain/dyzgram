import qrcode
from qrcode.main import QRCode


def gen_qrcode_print(login_token: str, show_with_img: bool = False):
    qr = QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.clear()
    qr.add_data(login_token)
    qr.make(fit=True)
    if show_with_img:
        img = qr.make_image(fill='black', back_color='white')
        img.show()
    else:
        # show with string
        qr.print_ascii()


def display_url_as_qrcode(url):
    return gen_qrcode_print(url)
