#Simplified BSD License
#
#Copyright (c) 2012, Florian Meyer
#tstscr@web.de
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met: 
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer. 
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution. 
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#################################################################

# Plugin extended and modified by Patrick Hill
# Date: 2016-03-12 14.46.01
# website: HelloHill.com
# email: patrickrhill@gmail.com


bl_info = {
    "name": "Auto Save Render with Datestamp",
    "author": "tstscr",
    "version": (1, 0),
    "blender": (2, 63, 0),
    "location": "Rendertab -> Render Panel",
    "description": "Automatically save the image after rendering",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Render/Auto_Save",
    "tracker_url": "http://projects.blender.org/tracker/index.php?func=detail&aid=32491",
    "category": "Render"}
###########################################################################
import bpy
from bpy.props import BoolProperty, EnumProperty
from bpy.app.handlers import persistent
from os.path import dirname, exists, join
from bpy.path import basename
from os import mkdir, listdir
from re import findall
import time
import re

datestamp = time.strftime("%Y-%m-%d") + " " + time.strftime("%H.%M.%S")

@persistent
def set_base_path(self):
    global datestamp
    datestamp = time.strftime("%Y-%m-%d") + " " + time.strftime("%H.%M.%S")

    print("Base Path Getting Set")
    
    # bpy.context.scene.node_tree.nodes["File Output"].base_path = "//exports/" + datestamp

    # sets File Output Node Input Subpath to unique name with date stamp
    scene = bpy.context.scene
    for node in scene.node_tree.nodes:
        if node.type == "OUTPUT_FILE":
            # print(node.type)
            # print(node.file_slots)
            node.base_path = "//exports"
            x = 1
            for slot in node.file_slots:
                slot_path = slot.path
                slot_stripped_of_date = re.sub(r'\d{4}-\d{2}-\d{2} \d{2}.\d{2}.\d{2}-', '', slot_path)
                number_with_leading_zero = format(x, '02d')
                slot.path = datestamp + "-" + slot_stripped_of_date
                x += 1


@persistent
def auto_save_render(scene):

    if not scene.save_after_render or not bpy.data.filepath:
        return
    rndr = scene.render
    original_format = rndr.image_settings.file_format

    format = rndr.image_settings.file_format
    if format == 'OPEN_EXR_MULTILAYER': extension = '.exr'
    if format == 'JPEG': extension = '.jpg'
    if format == 'PNG': extension = '.png'
    
    blendname = basename(bpy.data.filepath).rpartition('.')[0]
    filepath = dirname(bpy.data.filepath) + '/exports'

    print (datestamp)

    if not exists(filepath):
        mkdir(filepath)
        
    if scene.auto_save_subfolders:
        filepath = join(filepath, blendname)
        if not exists(filepath):
            mkdir(filepath)

    #imagefiles starting with the blendname
    files = [f for f in listdir(filepath) \
            if f.startswith(blendname) \
            and f.lower().endswith(('.png', '.jpg', '.jpeg', '.exr'))]
    
    highest = 0
    if files:
        for f in files:
            #find last numbers in the filename after the blendname
            suffix = findall('\d+', f.split(blendname)[-1])
            if suffix:
                if int(suffix[-1]) > highest:
                    highest = int(suffix[-1])
    
    #save_name = join(filepath, blendname) + '-' + datestamp + extension
    save_name = filepath + "/" + datestamp + "-composite" + extension

    image = bpy.data.images['Render Result']
    if not image:
        print('Auto Save: Render Result not found. Image not saved')
        return
    
    print('Auto_Save:', save_name)
    image.save_render(save_name, scene=None)

    rndr.image_settings.file_format = original_format

###########################################################################
def auto_save_UI(self, context):
    layout = self.layout
    
    split=layout.split(percentage=0.66, align=True)
    row = split.row()
    row.prop(context.scene, 'save_after_render', text='Auto Save', toggle=False)
    row.prop(context.scene, 'auto_save_subfolders', toggle=False)
    
def register():
    bpy.types.Scene.save_after_render = BoolProperty(
                    name='Save after render',
                    default=True,
                    description='Automatically save rendered images into: //auto_save/')
    bpy.types.Scene.auto_save_subfolders = BoolProperty(
                    name='subfolder',
                    default=False,
                    description='Save into individual subfolders per blend name')
    bpy.app.handlers.render_pre.append(set_base_path)
    bpy.app.handlers.render_post.append(auto_save_render)
    bpy.types.RENDER_PT_render.append(auto_save_UI)
    
def unregister():
    del(bpy.types.Scene.save_after_render)
    del(bpy.types.Scene.auto_save_subfolders)
    bpy.app.handlers.render_post.remove(auto_save_render)
    bpy.types.RENDER_PT_render.remove(auto_save_UI)

if __name__ == "__main__":
    register()