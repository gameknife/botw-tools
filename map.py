import struct
import pprint
import os
import json
import prod
import xml.etree.ElementTree as ET

from scipy.spatial.transform import Rotation

export_path = "D:/GKNIFE/LightingBeast/exported/actors/"

def zyx_to_yzx_rotation(zyx_rotation):
    r = Rotation.from_euler('xyz', zyx_rotation, degrees=False)
    q = r.as_quat()
    yzx_rotation = Rotation.from_quat(q).as_euler('xzy', degrees=False)
    return yzx_rotation

files = [
('map_locations.json',''),
#('map_locations_dungeon.json','_dungeon'),
#('map_locations_trial.json','_trial'),
]

namefile = open('botw_names.json')
object_names = json.load(namefile)
namefile.close()

if not os.path.exists(export_path):
    os.makedirs(export_path)

for outfilename,folder_suffix in files:

    for filename in os.listdir('mubin'+folder_suffix):

        # output objects
        objects = {}

        root = ET.parse('mubin'+folder_suffix+'/'+filename).getroot()

        export_filename = export_path + os.path.basename(filename) + ".json"

        # skip if file already exists
        if os.path.exists(export_filename):
            continue

        dropactor_objs = (root.findall('./*/value') +
                          root.findall('./Rails/*/RailPoints/value'))

        for actor in dropactor_objs:
            name = actor.findall('./UnitConfigName')[0].text
            coords = [float(node.text[:-1]) for node in actor.findall('./Translate/value')]
            if len(coords) == 0:
                continue
            scale = [float(node.text[:-1]) for node in actor.findall('./Scale/value')]
            if len(scale) == 0:
                if 'Scale' in actor.attrib:
                    scale = [float(actor.attrib['Scale'][:-1]),float(actor.attrib['Scale'][:-1]),float(actor.attrib['Scale'][:-1])]
                else:
                    scale = [1,1,1]

            raw_rotation = [float(node.text[:-1]) for node in actor.findall('./Rotate/value')]
            if len(raw_rotation) == 0:
                if 'Rotate' in actor.attrib:
                    raw_rotation = [0,float(actor.attrib['Rotate'][:-1]),0]
                else:
                    raw_rotation = [0,0,0]

            # convert rotation from euler order ZYX to YZX
            rotation = zyx_to_yzx_rotation(raw_rotation)

            drop_tables = actor.findall('./_Parameters/DropTable')
            drop_actors = (actor.findall('./_Parameters/DropActor') +
                           actor.findall('./_Parameters/RideHorseName') +
                           actor.findall('./_Parameters/EquipItem1') +
                           actor.findall('./_Parameters/EquipItem2') +
                           actor.findall('./_Parameters/EquipItem3') +
                           actor.findall('./_Parameters/EquipItem4') +
                           actor.findall('./_Parameters/EquipItem5') +
                           actor.findall('./_Parameters/ArrowName'))
            hard = actor.findall('./_Parameters[@IsHardModeActor]')
            is_hardmode = False
            if hard and hard[0].attrib['IsHardModeActor'] == 'true':
                is_hardmode = True
            
            if name in object_names:
                nice_name = object_names[name]
            else:
                nice_name = name
                
            # if len(drop_tables):
            #     drop_table = drop_tables[0].text
            #     if drop_table != 'Normal':
            #         name = name+':'+drop_table
            #         nice_name = nice_name+':'+drop_table
            # for drop_actor in drop_actors:
            #     drop_actor = drop_actor.text
            #     if drop_actor in ('Normal', 'Default', 'NormalArrow'):
            #         continue
            #     name += ':' + drop_actor
            #     nice_name += ':' + object_names[drop_actor]
            # if is_hardmode:
            #     name = 'HARD:'+name
            #     nice_name = 'HARD:'+nice_name
            
            # add uuid to name
            if 'HashId' in actor.attrib:
                name = name + '_' + actor.attrib['HashId']

            objects[name] = {'actor':nice_name, 'location':"", 'rotation':"", 'scale':""}
            #object][name]['locations'] = objects["mubin"][name]['locations'] + 1
            objects[name]['location'] = "{},{},{}".format(round(coords[0] * 100,2), round(coords[-1] * 100,2), round(coords[1] * 100,2))
            objects[name]['rotation'] = "{},{},{}".format(round(rotation[1] * 180 / 3.1415926535897932,2), round(rotation[2] * -180 / 3.1415926535897932,2), round(rotation[0] * 180 / 3.1415926535897932,2))
            objects[name]['scale'] = "{},{},{}".format(round(scale[0],2), round(scale[-1],2), round(scale[1],2))
            #if len(scale):
            #    objects[name]['locations'][-1].append({'width':scale[0],'height':scale[-1],'rotation':rotation[1]})

        outfile = open(export_filename,'w')
        #outfile.write('var locations = ')
        json.dump(objects, outfile, sort_keys=True,separators=(',', ':'),indent=4)
        #outfile.write(';\n')
        outfile.close()

    for filename in os.listdir('blwp'+folder_suffix):

        # output objects
        objects = {}

        export_filename = export_path + os.path.basename(filename) + ".json"

        # skip if file already exists
        if os.path.exists(export_filename):
            continue

        f=open('blwp'+folder_suffix+'/'+filename,'rb')
        data = f.read()
        f.close()
        
        chunk_objects = prod.parseProd(data)
        for name in chunk_objects:
            if name in object_names:
                nice_name = object_names[name]
            else:
                nice_name = name
            if name not in objects:
                objects[name] = {'actor':nice_name, 'count': len(chunk_objects[name]), 'locations':[], 'rotations':[], 'scales':[]}

            
            all_transforms = [(x,y,z,rotX, rotY, rotZ, scale) for x,y,z,rotX,rotY,rotZ,scale in chunk_objects[name]]

            # iterate the all_transforms
            for transform in all_transforms:
                objects[name]['locations'].append( "{},{},{}".format(round(transform[0]*100,2), round(transform[2]*100,2), round(transform[1]*100),2) )
                raw_rotation = [transform[3],transform[4],transform[5]]
                rotation = zyx_to_yzx_rotation(raw_rotation)
                objects[name]['rotations'].append( "{},{},{}".format(round(rotation[1] * 180 / 3.1415926535897932,2), round(rotation[2] * -180 / 3.1415926535897932,2), round(rotation[0] * 180 / 3.1415926535897932,2)) )
                objects[name]['scales'].append( "{}".format(round(transform[6],2)) )
            #objects["blwp"][name]['locations'] = objects["blwp"][name]['locations'] + 1

        outfile = open(export_filename,'w')
        #outfile.write('var locations = ')
        json.dump(objects, outfile, sort_keys=True,separators=(',', ':'),indent=4)
        #outfile.write(';\n')
        outfile.close()