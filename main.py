#!/usr/bin/python

# change to directory of script
# $ cd /Users/jason/Files/app_video_maker
# run the following
# $ python3 main.py

import os

from sources.log import Log
from sources.qr_code import QRCode
from sources.translator import *
from sources.image_generator import ImageGenerator

from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects

generated_resources_folder = "resources/generated"

gray_background_color = (35, 35, 33) # hex #232321
fps = 25

def main():
	for language_code in language_codes:
		set_current_langage_code(language_code)
		build_video(language_code)
		do_translations()

def build_video(language_code):

	output_path = f"output/pace_clock_{language_code}.mp4"
	width = 1920
	height = 1080
	
	remove_file(output_path)
	generate_resources(width, height)

	clips = []

	splash_clip = generate_splash_clip(width, height, 4, language_code)
	clips.append(splash_clip)

	android_apple_clip = generate_android_apple_clip(width, height, 4).set_start(getStart(clips))
	clips.append(android_apple_clip)

	apple_products_clip = generate_apple_products_clip(width, height, 4, language_code).set_start(getStart(clips))
	clips.append(apple_products_clip)

	activities_clips = generate_activities_clips(width, height, 4, language_code).set_start(getStart(clips))
	clips.append(activities_clips)

	demo_clip = generate_demo_clip(width, height, 28, language_code).set_start(getStart(clips))
	clips.append(demo_clip)

	download_clip = generate_download_clip(width, height, 9, language_code).set_start(getStart(clips))
	clips.append(download_clip)

	final_clip = CompositeVideoClip(clips, size=(width, height))
	Log.i(f"final clip duration {final_clip.duration}")

	audioclip = AudioFileClip("resources/track.wav")
	audioclip = audioclip.set_fps(fps)

	final_clip.audio = CompositeAudioClip([audioclip])

	final_clip.write_videofile(output_path, fps=fps)
	#final_clip.preview() # breaks with sound, and is slow

def generate_splash_clip(width, height, duration, language_code):

	video = generate_activities_clip("resources/intro.mp4", "Pace Clock", width, height, duration, language_code)

	animated_duration = duration/4
	animated_icon = ImageClip(f"{generated_resources_folder}/icon.png")
	animated_icon = animated_icon.set_duration(animated_duration)
	animated_icon = animated_icon.set_position((width*0.01, "center"))

	start_size = height*0.6
	end_size = height*0.5
	animated_icon.fps = fps
	animated_icon = animated_icon.resize(lambda t: ( 
		start_size * ((animated_duration - t)/animated_duration) + end_size, 								
		start_size * ((animated_duration - t)/animated_duration) + end_size ))

	icon = ImageClip(f"{generated_resources_folder}/icon.png")
	icon = icon.set_duration(duration-animated_duration)
	icon = icon.set_position((width*0.01, "center"))
	icon = icon.resize(height=end_size)
	icon = icon.set_start(animated_icon.end)

	return CompositeVideoClip([video, animated_icon, icon], size=(width, height))

def generate_android_apple_clip(width, height, duration):

	background = ColorClip(size=(width, height), color=gray_background_color)
	background = background.set_duration(duration)

	iphone_clip = generate_iphone_display_clip("resources/apple_iphone_dark.mp4", duration)
	iphone_clip = iphone_clip.set_duration(duration)
	iphone_clip = iphone_clip.set_position(("center", height*0.12))
	iphone_clip = iphone_clip.resize(height=height*0.6)

	apple_icon = ImageClip(f"{generated_resources_folder}/colored_apple_icon.png")
	apple_icon = apple_icon.set_duration(duration)
	apple_icon = apple_icon.resize(height=height*0.1)
	apple_icon = apple_icon.set_position(("center", height*0.77))

	apple_section = CompositeVideoClip([iphone_clip, apple_icon], size=(round(width*0.5), height))
	
	android_clip = generate_android_phone_display_clip("resources/android_phone.mp4", duration)
	android_clip = android_clip.set_duration(duration)
	android_clip = android_clip.set_position(("center", height*0.12))
	android_clip = android_clip.resize(height=height*0.6)

	android_icon = ImageClip(f"{generated_resources_folder}/colored_android_icon.png")
	android_icon = android_icon.set_duration(duration)
	android_icon = android_icon.resize(height=height*0.1)
	android_icon = android_icon.set_position(("center", height*0.77))

	android_section = CompositeVideoClip([android_clip, android_icon], size=(round(width*0.5), height))
	android_section = android_section.set_position((width*0.5, 0))

	return scale(CompositeVideoClip([background, android_section, apple_section], size=(width, height)))

def generate_apple_products_clip(width, height, duration, language_code):

	background = ColorClip(size=(width, height), color=gray_background_color)
	background = background.set_duration(duration)

	macOS_text = TextClip("MacOS", fontsize=round(height*0.08), color='white', font=get_font_family(language_code))
	visionOS_text = TextClip("VisionOS", fontsize=round(height*0.08), color='white', font=get_font_family(language_code))
	watchOS_text = TextClip("WatchOS", fontsize=round(height*0.08), color='white', font=get_font_family(language_code))

	apple_icon_width = width*0.05
	apple_icon = ImageClip(f"resources/apple_icon.png")
	apple_icon = apple_icon.set_duration(duration)
	apple_icon = apple_icon.resize(width=apple_icon_width)
	apple_icon = apple_icon.set_position((width*0.5-apple_icon_width-visionOS_text.w*0.5, height*0.05))

	macOS_video = generate_mac_os_display_clip(duration, 18, 18)
	macOS_video = macOS_video.set_duration(duration)
	macOS_video = macOS_video.resize(height=height*0.8)
	macOS_video = macOS_video.set_position(("center", height*0.18))

	macOS_text = macOS_text.set_duration(duration)
	macOS_text = macOS_text.set_position((width*0.5-macOS_text.w*0.5+apple_icon_width*0.5, height*0.104-macOS_text.h*0.5))

	mac_section = CompositeVideoClip([background, macOS_video, apple_icon, macOS_text], size=(width, height))

	watch_display = generate_watch_display_clip("resources/apple_watch.mp4", duration)
	watch_display = watch_display.set_duration(duration)
	watch_display = watch_display.resize(height=height*0.6)
	watch_display = watch_display.set_position(("center", height*0.25))

	watchOS_text = watchOS_text.set_duration(duration)
	watchOS_text = watchOS_text.set_position((width*0.5-watchOS_text.w*0.5+apple_icon_width*0.5, height*0.104-watchOS_text.h*0.5))

	watch_section = CompositeVideoClip([background, watch_display, apple_icon, watchOS_text], size=(width, height))

	visionOS_video = VideoFileClip("resources/apple_vision.mp4")
	visionOS_video = visionOS_video.set_duration(duration)
	visionOS_video = visionOS_video.resize(width=width)
	visionOS_video = visionOS_video.set_position(("center", "center"))

	visionOS_text = visionOS_text.set_duration(duration)
	visionOS_text = visionOS_text.set_position((width*0.5-visionOS_text.w*0.5+apple_icon_width*0.5, height*0.104-visionOS_text.h*0.5))

	vision_section = CompositeVideoClip([visionOS_video, apple_icon, visionOS_text], size=(width, height))

	return CompositeVideoClip([mac_section,
								watch_section.set_start(duration*1),
								vision_section.set_start(duration*2)
								], size=(width, height))

def generate_activities_clips(width, height, duration, language_code):

	screens = [("resources/swimming.mp4", TR("Swimming")),
				("resources/running.mp4", TR("Running")),
				("resources/stretching.mp4", TR("Stretching")),
				("resources/training.mp4", TR("Training")),
				("resources/studying.mp4", TR("Studying"))]
	clips = []

	for index, screen in enumerate(screens):
		path, label = screen
		clip = generate_activities_clip(path, label, width, height, duration, language_code)
		clip = clip.set_start(duration*index)
		clips.append(clip)

	total_duration = duration*len(screens)
	watch_display = generate_watch_display_clip("resources/apple_watch.mp4", total_duration)
	watch_display = watch_display.set_duration(total_duration)
	watch_display = watch_display.resize(height=height*0.4)
	watch_display = watch_display.set_position((width*0.05, "center"))
	clips.append(watch_display)

	return CompositeVideoClip(clips, size=(width, height))

def generate_activities_clip(video_path, label, width, height, duration, language_code):

	video = VideoFileClip(video_path)
	video = video.set_duration(duration)
	video = video.resize(width=width, height=height)

	text_background = ImageClip(f"{generated_resources_folder}/background_label.png")
	text_background = text_background.set_duration(duration)
	text_background = text_background.resize(width=width)
	text_background = text_background.set_position((0, height*0.57))

	text = TextClip(label, fontsize=round(height*0.1), color='white', font=get_font_family(language_code))
	text = text.set_duration(duration)
	text = text.set_position(("center", height*0.665-text.h*0.5))

	return CompositeVideoClip([video, text_background, text], size=(width, height))

def generate_demo_clip(width, height, duration, language_code):

	background = ColorClip(size=(width, height), color=gray_background_color)
	background = background.set_duration(duration)

	video = generate_mac_os_display_clip(duration, 0, duration)
	video = video.set_duration(duration)
	video = video.resize(height=height*0.8)
	video = video.set_position(("center", "center"))

	text_offset = 2
	text_label = TR("Demo")
	hightlight_text = TextClip(text_label, fontsize=round(height*0.1), color='white', font=get_font_family(language_code))
	hightlight_text = hightlight_text.set_duration(2)
	hightlight_text = hightlight_text.set_opacity(0.6)
	hightlight_text = hightlight_text.set_position((text_offset, text_offset))

	text = TextClip(text_label, fontsize=round(height*0.1), color='gray', font=get_font_family(language_code))
	text = text.set_duration(2)

	text_shadow = CompositeVideoClip([hightlight_text, text], size=(text.w+text_offset, text.h+text_offset))
	text_shadow = text_shadow.set_duration(2)
	text_shadow = text_shadow.crossfadeout(1)
	text_shadow = text_shadow.set_position(("center", "center"))

	return CompositeVideoClip([background, video, text_shadow], size=(width, height))

def generate_download_clip(width, height, duration, language_code):

	background = ColorClip(size=(width, height), color=gray_background_color)
	background = background.set_duration(duration)
	
	apple_qr = ImageClip(f"{generated_resources_folder}/apple_qr_code.png")
	apple_qr = apple_qr.set_duration(duration)
	apple_qr = apple_qr.resize(height=height*0.5)
	apple_qr = apple_qr.set_position(("center", height*0.15))

	apple_icon = ImageClip(f"{generated_resources_folder}/colored_apple_icon.png")
	apple_icon = apple_icon.set_duration(duration)
	apple_icon = apple_icon.resize(height=height*0.1)
	apple_icon = apple_icon.set_position(("center", height*0.68))

	apple_section = CompositeVideoClip([apple_qr, apple_icon], size=(round(width*0.5), height))

	android_qr = ImageClip(f"{generated_resources_folder}/android_qr_code.png")
	android_qr = android_qr.set_duration(duration)
	android_qr = android_qr.resize(height=height*0.5)
	android_qr = android_qr.set_position(("center", height*0.15))

	android_icon = ImageClip(f"{generated_resources_folder}/colored_android_icon.png")
	android_icon = android_icon.set_duration(duration)
	android_icon = android_icon.resize(height=height*0.1)
	android_icon = android_icon.set_position(("center", height*0.68))

	android_section = CompositeVideoClip([android_qr, android_icon], size=(round(width*0.5), height))
	android_section = android_section.set_position((width*0.5, 0))

	text = TextClip(TR("Download links are in video description"), fontsize=round(height*0.04), color='white', font=get_font_family(language_code))
	text = text.set_duration(duration)
	text = text.set_position(("center", height*0.87))

	return scale(CompositeVideoClip([background, android_section, apple_section, text], size=(width, height)))

def generate_android_phone_display_clip(video_path, duration):
	android_background = ImageClip(f"{generated_resources_folder}/colored_android_phone_background.png")
	android_background = android_background.set_duration(duration)
	android_background = android_background.set_position(("center", "center"))
	
	video = VideoFileClip(video_path)
	video = video.set_duration(duration)
	video = video.resize(height=android_background.h*0.84)
	video = video.set_position(("center", android_background.h*0.08))

	return CompositeVideoClip([android_background, video])

def generate_mac_os_display_clip(duration, start, end):
	video = VideoFileClip("resources/apple_mac.mov")
	video = video.subclip(start, end)
	video = video.set_duration(duration)
	
	clip_height = 4
	video_clip_background = ColorClip(size=(video.w, clip_height), color=gray_background_color)
	video_clip_background = video_clip_background.set_duration(duration)
	video_clip_background = video_clip_background.set_position((0, video.h - clip_height))

	return CompositeVideoClip([video, video_clip_background])	

def generate_iphone_display_clip(video_path, duration):
	iphone_background = ImageClip(f"{generated_resources_folder}/colored_apple_iphone_background.png")
	iphone_background = iphone_background.set_duration(duration)
	iphone_background = iphone_background.set_position(("center", "center"))
	
	video = VideoFileClip(video_path)
	video = video.set_duration(duration)
	video = video.resize(height=iphone_background.h*0.94)
	video = video.set_position(("center", iphone_background.h*0.03))
	video = video.speedx(factor=0.1) # hack to play proper speed

	return CompositeVideoClip([iphone_background, video])

def generate_watch_display_clip(video_path, duration):
	watchOS_background = ImageClip("resources/apple_watch_background.png")
	watchOS_background = watchOS_background.set_duration(duration)
	watchOS_background = watchOS_background.set_position(("center", "center"))
	
	video = VideoFileClip(video_path)
	video = video.set_duration(duration)
	video = video.resize(width=watchOS_background.w*0.78, height=watchOS_background.w*0.78)
	video = video.set_position(("center", "center"))
	video = video.loop(duration)

	return CompositeVideoClip([watchOS_background, video])

def getStart(clips):
	if len(clips)<1:
		return 0
	else:
		return clips[len(clips)-1].end

def scale(clip, factor=0.96):
	width = clip.w
	height = clip.h 

	background = ColorClip(size=(width, height), color=gray_background_color)
	background = background.set_duration(clip.duration)

	result = clip.resize((width*factor, height*factor))
	result = clip.set_position(("center", "center"))
	return  CompositeVideoClip([background, result], size=(width, height))

def get_font_family(language_code):
	if language_code == "ja":
		return "resources/NotoSansJP-VariableFont_wght.ttf"
	elif language_code == "ko":
		return "resources/NotoSansKR-VariableFont_wght.ttf"
	else:
		return "Futura"

def generate_resources(width, height):
	
	folder = "resources/generated"
	if not os.path.exists(folder):
		os.mkdir(folder)

	path = f"{folder}/apple_qr_code.png"
	if not os.path.exists(path):
		QRCode.generate("https://apps.apple.com/us/app/pace-clock/id6473059084", path)

	path = f"{folder}/android_qr_code.png"
	if not os.path.exists(path):
		QRCode.generate("https://play.google.com/store/apps/details?id=com.tarusstudios.paceclock", path)

	path = f"{folder}/icon.png"
	if not os.path.exists(path):
		ImageGenerator.convert_svg_to_png("resources/icon.svg", path)

	path = f"{folder}/colored_android_icon.png"
	if not os.path.exists(path):
		ImageGenerator.generate_image_with_background_color("resources/android_icon.png", path, gray_background_color)

	path = f"{folder}/colored_apple_icon.png"
	if not os.path.exists(path):
		ImageGenerator.generate_image_with_background_color("resources/apple_icon.png", path, gray_background_color)
		
	path = f"{folder}/colored_android_phone_background.png"
	if not os.path.exists(path):
		ImageGenerator.generate_image_with_background_color("resources/android_phone_background.png", path, gray_background_color)

	path = f"{folder}/colored_apple_iphone_background.png"
	if not os.path.exists(path):
		ImageGenerator.generate_image_with_background_color("resources/apple_iphone_background.png", path, gray_background_color)

	path = f"{folder}/background_label.png"
	if os.path.exists(path):
		os.remove(path)
	ImageGenerator.generate_background_gradient(path, width, round(height*0.2), gray_background_color, (0,0,0))

def remove_file(path):
	if os.path.exists(path):
		os.remove(path)
	else:
		Log.w("File does not exist: " + path)

os.system('clear')
Log.i("START app_video_maker")
main()
Log.i("FINISHED")

