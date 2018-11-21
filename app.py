from flask import Flask, request, flash, render_template
from flask_wtf import FlaskForm
from wtforms import TextField, validators
from music_spider import Zingmp3AudioDownloader, Zingmp3VideoDownloader
from music_spider import NhaccuatuiDownloader
import os
import re

app = Flask(__name__, static_url_path='/static')
app.config.from_object(__name__)
app.config['SECRET_KEY'] = os.urandom(30)


class WebForm(FlaskForm):
    link = TextField('link', validators=[validators.required()])


@app.route('/', methods=['GET', 'POST'])
def hello():
    form = WebForm()
    if request.method == 'POST':
        raw = request.form['link']
        link = raw.split(" | ")[0]
        mp3_valid = re.match("(https?:\/\/)?(m.)?mp3\.zing\.vn\/bai-hat\/[\w\d\-]+/([\w\d]{8})\.html", link)
        mp3v_valid = re.match("(https?:\/\/)?mp3\.zing\.vn\/video-clip\/[\w\d\-]+/([\w\d]{8})\.html", link)
        nct_valid = re.match("https?:\/\/www\.nhaccuatui\.com\/bai-hat\/[-.a-z0-9A-Z]+\.html", link)
        if form.validate_on_submit():
            if mp3_valid:
                try:
                    player, title, artist, thumbnail, link128, link320, lossless = Zingmp3AudioDownloader(link).crawl_download_url()
                    flash(u"Get link successfully", 'success')
                    flash(link128, '128Kbps')
                    if link320:
                        flash(link320, '320Kbps')
                    if lossless:
                        flash(lossless, 'Lossless')
                    flash(player, 'player')
                    flash(title, 'title')
                    flash(artist, 'artist')
                    flash(thumbnail, 'thumbnail')
                except:
                    msg = Zingmp3AudioDownloader(link)
                    if msg:
                        flash("This song is copyrighted", 'copyright')
                    else:
                        flash("Serious error has occurred.", 'fail')
            elif mp3v_valid:
                try:
                    player, title, thumbnail, artist, download_url_360, download_url_480, download_url_720, download_url_1080 = Zingmp3VideoDownloader(link).crawl_download_url()
                    flash(u"Get link successfully", 'success')
                    flash(download_url_360, '128Kbps')
                    if download_url_480:
                        flash(download_url_480, '320Kbps')
                    if download_url_720:
                        flash(download_url_720, 'Lossless')
                    if download_url_1080:
                        flash(download_url_1080, '1080p')
                    flash(player, 'player')
                    flash(title, 'title')
                    flash(artist, 'artist')
                    flash(thumbnail, 'thumbnail')
                except:
                    msg = Zingmp3VideoDownloader(link)
                    if msg:
                        flash("This song is copyrighted", 'copyright')
                    else:
                        flash("Serious error has occurred.", 'fail')

            elif nct_valid:

                try:
                    title, artist, thumbnail, link128, link320, lossless = NhaccuatuiDownloader(link).crawl_download_url()
                    flash(u"Get link successfully", 'success')
                    player = link128
                    flash(link128, '128Kbps')

                    if "hq.mp3" in link320:
                        flash(link320, '320Kbps')

                    if ".flac" in lossless:
                        flash(lossless, 'Lossless')

                    flash(player, 'player')
                    flash(title, 'title')
                    flash(artist, 'artist')
                    flash(thumbnail, 'thumbnail')
                except:
                    flash("Serious error has occurred.", 'fail')

            else:
                flash(u"The link you entered is incorrect, please check again.", 'error')

        else:
            flash(u'You need to enter a link.', 'error')

    return render_template('main.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
