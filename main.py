import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GdkPixbuf
from PIL import Image
import mutagen

def get_song_info(song):
    audio = mutagen.File(song)
    tags = audio.tags

    info = {
        'title': str(tags['TIT2']),
        'artist': str(tags['TPE1']),
        'cover': None
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

    styles = """picture{ border-radius: 10px; } .info{ font-size: 20px; }"""
    css = Gtk.CssProvider()
    css.load_from_data(styles.encode())
    info.get_style_context().add_class('info')
    Gtk.StyleContext.add_provider_for_display(win.get_display(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    container.append(cover_wrap)
    container.append(info_wrap)

    win.set_child(container)
    win.present()

app = Gtk.Application(application_id='org.r1v3ra.gplayer')
app.connect('activate', main)
app.run(None)