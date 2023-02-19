#import random
#import re
#import traceback
import gradio as gr
from modules import script_callbacks, scripts #, shared
#from modules.shared import opts
import requests

PLUGIN_NAME = "Sankaku Prompt"
HTTP_HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0' }

def on_ui_settings():
	section = ('sankaku-prompt', PLUGIN_NAME)

def handle(image):
	name = image.orig_name
	hash = name.split(".")[0]

	response = requests.get(f'https://capi-v2.sankakucomplex.com/posts?lang=en&page=1&limit=1&tags=md5%3A{hash}', headers=HTTP_HEADERS)
	data = response.json()

	tags = []
	if(len(data) > 0):
		for tag in data[0]['tags']:
			tag = tag['tagName'].replace("_", " ")
			tags.append(tag)

		tags = (', ').join(tags)

	return(tags)

class SankakuPropmptScript(scripts.Script):
	def __init__(self) -> None:
		super().__init__()

	def title(self):
		return(PLUGIN_NAME)

	def show(self, is_img2img):
		return scripts.AlwaysVisible

	def ui(self, is_img2img):
		with gr.Group():
			with gr.Accordion(PLUGIN_NAME, open=False):
				fetch_tags = gr.Button(value='Get Tags', variant='primary')
				#image = gr.Image(source="upload", type="file", label="Image with MD5 Hash")
				image = gr.File(type="file", label="Image with MD5 hash")
				tags = gr.Textbox(value = "", label="Tags", lines=5)

		fetch_tags.click(fn=handle, inputs=[image], outputs=[tags])
		return [image, tags, fetch_tags]

script_callbacks.on_ui_settings(on_ui_settings)