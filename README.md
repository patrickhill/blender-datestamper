# Blender 3D - Auto Save Render with Date Stamp
This plugin extends the [Auto Save Render](http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Render/Auto_Save) plugin by tstscr

## Features
1. Adds a date stamp to the auto saved render image filename instead of an incrementing number.
2. Will set the File Output node save path to a folder with a date stamp

## Benefits
Gives unique file name to render outputs so previous renders don't get overwritten.

## How I Use It
The stock Blender File Output node will over write your image files every time you render a scene. This plugin will create unique names so you can keep track of your work history and progress. I find it very useful when I have multiple render layers for a scene and I want an image of each layer auto saved out each time I start a render. This takes care of that plus the date stamps gives me useful context for my work. By simply looking at my renders:
* I can quickly see when I last worked on a project or how long I've been working on a project
* I can see how work progress e.g. It takes me a long time to model objects but texturing progress moves very fast.