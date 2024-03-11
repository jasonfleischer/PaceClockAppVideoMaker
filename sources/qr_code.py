#!/usr/bin/python3

import qrcode

class QRCode:

	@staticmethod
	def generate(url, destination_path):
		qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=0)
		qr.add_data(url)
		qr.make(fit=True)
		img = qr.make_image(fill_color="#232321", back_color="#FFFFFF")
		img.save(destination_path)