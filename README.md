# Color Palette Generator

A Flask app to detect and enlist colors in an image.
![Color Palette Generator](https://user-images.githubusercontent.com/11702800/115494607-9a6a3800-a283-11eb-857a-9f58b312e0f4.png)

## Setup

```
$ pipenv install

$ pipenv run gunicorn wsgi:app
```

A custom implementation of the KMeans algorithm extracts RGB colors from `jpg`, `png` or `jpeg` images and displays them in HEX format.

The colors can be downloaded as a CSS `:root` palette, SCSS variables or in JSON format.

Developed as a project exercise at Vision, NIT Bhopal.
