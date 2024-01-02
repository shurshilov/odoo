================================
Web Image Editing (WIE)
================================

* This module extend image widget and work outbox!
* Also are available setting in xml file!
* See video for greater understanding!

Capabilities
=====

* Zoom and pan
* Rotate
* Crop
* Step back in history client-side (before save)
* Download original
* Open original image
* Upload URL image
* Edit current image
* Image preview by click
* Settings - min and max (height, width) image prview, ratio, backgroundColor
* And other...
 
Usage
=====

After installing the module, you can use it in the following ways

* 1. Instant use with default settings!

* 2. The widget passes options directly through to image, which supports the 
  following code-block::
    <field name="image_medium" widget="image" options=
        "{      
        'minWidth': 100,
        'minHeight': 100,
        'maxWidth': 800,
        'maxHeight': 600,
        'ratio': 1,
        'plugins':  {
                    'crop': {
                            'minHeight': 50,
                            'minWidth': 50,
                            'maxHeight': 250,
                            'maxWidth': 250,
                            'ratio': 1,
                            }
                    }
        }" />

  see video on youtube raw:: html
        <iframe width="560" height="315" src="https://www.youtube.com/watch?v=OOU8AkYuW1E" frameborder="0" allowfullscreen></iframe>

  .. image:: https://raw.githubusercontent.com/shurshilov/web/10.0/widget_image_tools/static/description/Menu.png
     :alt: WIE menu
     :class: img-thumbnail
     :height: 360

  .. image:: https://raw.githubusercontent.com/shurshilov/web/10.0/widget_image_tools/static/description/Edit.png
     :alt: WIE edit
     :class: img-thumbnail col-xs-offset-1
     :height: 360

  .. image:: https://raw.githubusercontent.com/shurshilov/web/10.0/widget_image_tools/static/description/Zoom.png
     :alt: WIE zoom
     :class: img-thumbnail col-xs-offset-1
     :height: 360

  .. image:: https://raw.githubusercontent.com/shurshilov/web/10.0/widget_image_tools/static/description/Preview.png
     :alt: WIE preview
     :class: img-thumbnail col-xs-offset-1
     :height: 360

  .. image:: https://raw.githubusercontent.com/shurshilov/web/10.0/widget_image_tools/static/description/Download_origin.png
     :alt: WIE download origin with origin name
     :class: img-thumbnail col-xs-offset-1
     :height: 360

Contributors
------------

* Shurshilov Artem <shurshilov.a@yandex.ru>