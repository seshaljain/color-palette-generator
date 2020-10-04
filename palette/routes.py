import os
import secrets
from flask import render_template, url_for, redirect, request, Response
from palette.forms import ImageForm
from palette import app
from kmeans import get_colors


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_name)

    form_picture.save(picture_path)
    return picture_name


@app.route('/', methods=['GET', 'POST'])
def home():
    form = ImageForm()
    if form.validate_on_submit():
        f_name = save_picture(form.picture.data)
        color_list = get_colors(
            form.picture.data, int(request.form['colorCount']))
        palette_path = '-'.join(color_list)
        return redirect(url_for('palette', colors=palette_path, image=f_name))
    return render_template('home.html', form=form)


@app.route('/palette/<colors>')
def palette(colors):
    hex_colors = ['#' + color for color in colors.split('-')]
    image = request.args.get('image')
    return render_template('palette.html', colors=hex_colors, image=image, download_url=request.path)


@app.route('/download/css/palette/<colors>')
def download_css(colors):
    color_list = colors.split('-')
    output = ":root {\n"
    for i, val in enumerate(color_list):
        output += "  --color-{0}: #{1};\n".format(i + 1, val)
    output += '}'
    return Response(output, mimetype="text/css", headers={"Content-Disposition": 'attachment; filename="colors.css"'})


@app.route('/download/scss/palette/<colors>')
def download_scss(colors):
    color_list = colors.split('-')
    output = ""
    for i, val in enumerate(color_list):
        output += "$color-{0}: #{1};\n".format(i + 1, val)
    return Response(output, mimetype="text/x-scss", headers={"Content-Disposition": 'attachment; filename="colors.scss"'})


@app.route('/download/json/palette/<colors>')
def download_json(colors):
    color_list = colors.split('-')
    output = "{\n"
    for i, val in enumerate(color_list):
        output += '  "color-{0}": "#{1}",\n'.format(i + 1, val)
    output += "}"
    return Response(output, mimetype="text/json", headers={"Content-Disposition": 'attachment; filename="colors.json"'})
