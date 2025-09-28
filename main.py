import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GdkPixbuf
from PIL import Image
import mutagen
from pygame import mixer
import time

is_playing = False

def playSong(button, song, icon_pause, icon_play):
    global is_playing
    mixer.init()
    mixer.music.load(song)
    mixer.music.play()

    if is_playing == False:
        button.set_child(icon_pause)
        is_playing = not is_playing
    else: 
        button.set_child(icon_play)
        is_playing = not is_playing
        stopSong(button, song)

def stopSong(button, song):
    mixer.music.load(song)
    mixer.music.stop()

def get_song_info(song):
    audio = mutagen.File(song)
    tags = audio.tags

    len_min = int(audio.info.length//60)
    len_sec = int(audio.info.length%60)
    length = int(audio.info.length)

    info = {
        'title': str(tags['TIT2']),
        'artist': str(tags['TPE1']),
        'cover': None,
        'len_min': len_min,
        'len_sec': len_sec,
        'len': f"{len_min}:{len_sec}",
        'sec_len': length
    }

    if song.endswith('.mp3'):
            # Для MP3 файлов
            for tag in audio.tags.keys():
                if tag.startswith('APIC') or tag == 'APIC:':
                    cover_data = audio.tags[tag].data
                    with open('cache/cover.jpg', 'wb') as f:
                        f.write(cover_data)
                    info['cover'] = 'cache/cover.jpg'
                    break

    return info

def main(app):
    win = Gtk.ApplicationWindow(application=app)
    win.set_title('GPlayer')
    win.set_default_size(400, 500)

    container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    container.set_halign(Gtk.Align.CENTER)
    
    info_wrap = Gtk.Box()
    song = "linkin-park-faint.mp3"
    song_info = get_song_info(song)
    artist = song_info['artist']
    name = song_info['title']
    info = Gtk.Label(label=f'{artist} - {name}')
    info.set_margin_top(24)
    info_wrap.append(info)
    info_wrap.set_halign(Gtk.Align.CENTER)

    cover_wrap = Gtk.Box()
    img = Image.open(song_info['cover'])
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(song_info['cover'], 200, 200, False)
    cover = Gtk.Picture.new_for_pixbuf(pixbuf)
    cover.set_margin_top(margin=45)
    cover_wrap.append(cover)
    cover_wrap.set_halign(Gtk.Align.CENTER)

    position_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    position = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
    position.set_range(0, 100)
    length = Gtk.Label(label=f'{song_info['len']}')
    position_box.append(length)
    position_box.append(position)

    controls = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=28)
    
    prev = Gtk.Picture.new_for_filename('data/prev.svg')
    play = Gtk.Picture.new_for_filename('data/play.svg')
    pause = Gtk.Picture.new_for_filename('data/pause.svg')
    next = Gtk.Picture.new_for_filename('data/next.svg')
    
    prev_btn = Gtk.Button()
    prev_btn.set_child(prev)
    play_btn = Gtk.Button()
    play_btn.set_child(play)
    play_btn.connect('clicked', lambda btn: playSong(btn, song, pause, play))
    next_btn = Gtk.Button()
    next_btn.set_child(next)

    controls.append(prev_btn)
    controls.append(play_btn)
    controls.append(next_btn)


    styles = """picture{ border-radius: 10px; } .info{ font-size: 20px; }"""
    css = Gtk.CssProvider()
    css.load_from_data(styles.encode())
    info.get_style_context().add_class('info')
    Gtk.StyleContext.add_provider_for_display(win.get_display(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    container.append(cover_wrap)
    container.append(info_wrap)
    container.append(position_box)
    container.append(controls)

    win.set_child(container)
    win.present()

app = Gtk.Application(application_id='org.r1v3ra.gplayer')
app.connect('activate', main)
app.run(None)