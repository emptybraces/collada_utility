import sys
import re
import struct
import math
import os.path
# from xml.etree import ElementTree
from xml.etree import ElementTree
from classes import *
import util
# const variable definition
DEBUG_MODE = True;
USE_INDICES = False;

# functions
def write(file, fmt, *args):
    if DEBUG_MODE:
        file.write(fmt, *args);
    else:
        file.write(struct.pack(fmt, *args));
def writeBinaryWithIndices(f, datalist):
    """
    write to a file the custom model data include indices.

    index used when drawing.


    in case of not exist data, fill the -1 value.
    custom model data description is following.
    # example
    # filename1:
    #     datakind databyte(*=variable length)
    # filename2:
    #     ...

    argv[2]/GEOMETRYNAME_datamap.bin:
        output type             4
        position value count    4
        position data offset    4
        normal value count      4
        normal data offset      4
        texcoord value count    4
        texcoord data offset    4
        color value count       4
        color data offset       4
    argv[2]/GEOMETRYNAME_vertex.bin:
        position vertices       4*
        normal vertices         4*
        uvmap data              4*
        color data              4*
    """
    pass;
    # pos_semantic = None;
    # pos_valuenum = None;
    # pos_indices = None;
    # pos_vertex = None;
    # pos_vertex_num = None;
    # normal_semantic = None;
    # normal_valuenum = None;
    # normal_indices = None;
    # normal_vertex = None;
    # # collect write info
    # for m in data_map:
    #     # vertex info
    #     if m["semantic"] == "VERTEX":
    #         pos_semantic = ord(m["semantic"][0]);
    #         pos_valuenum = m["valueNum"];
    #         pos_indices = m["index"];
    #         pos_vertex = m["vertex"];
    #         pos_vertex_num = int(len(m["vertex"]) / 3);
    #     # normal info
    #     elif m["semantic"] == "NORMAL":
    #         normal_semantic = ord(m["semantic"][0]);
    #         # normal_valuenum = m["valueNum"];
    #         normal_indices = m["index"];
    #         normal_vertex = m["vertex"];

    # new_vertex_normal = [[0, 0, 0] for i in range(pos_vertex_num)];
    # tmp_vertex_normal = [[] for i in range(pos_vertex_num)];
    # for i in range(len(pos_indices)):
    #     pi = int(pos_indices[i]);
    #     ni = int(normal_indices[i]);
    #     nx = float(normal_vertex[ni * 3 + 0]);
    #     ny = float(normal_vertex[ni * 3 + 1]);
    #     nz = float(normal_vertex[ni * 3 + 2]);
    #     already = False;
    #     for v in tmp_vertex_normal[pi]:
    #         if v[0] == nx and v[1] == ny and v[2] == nz:
    #             already = True;
    #             break;
    #     if not already:
    #         new_vertex_normal[pi][0] += nx;
    #         new_vertex_normal[pi][1] += ny;
    #         new_vertex_normal[pi][2] += nz;
    #         tmp_vertex_normal[pi].append([nx, ny, nz]);
    # normal_valuenum = len(new_vertex_normal) * 3;
    # # write
    # print("header part:");
    # write(f, "<1i", 0);
    # write(f, "<2i", pos_semantic, pos_valuenum);
    # write(f, "<2i", normal_semantic, normal_valuenum);
    # # index size
    # write(f, "<1i", ord("Common"[0]));
    # write(f, "<1i", len(pos_indices));
    # print("\ndata part:");
    # # indices
    # for elem in pos_indices: 
    #     write(f, "<1h", int(elem));
    # print();
    # # vertex data
    # for elem in pos_vertex: 
    #     write(f, "<1f", float(elem));
    # print();
    # # normal data
    # for v3 in new_vertex_normal:
    #     v3 = normalize(v3);
    #     write(f, "<3f", v3[0], v3[1], v3[2]);
    # print();
def writeBinary(datalist):
    """
    write to a file the custom model data.

    index is not used when drawing.
    therefore, store a value in the order as the index.
    in case of not exist data, fill the -1 value.
    custom model data description is following.
    # example
    # filename1:
    #     datakind databyte(*=variable length)
    # filename2:
    #     ...

    argv[2]/GEOMETRYNAME_datamap.bin:
        output type             4
        position value count    4
        position data offset    4
        normal value count      4
        normal data offset      4
        texcoord value count    4
        texcoord data offset    4
        color value count       4
        color data offset       4
    argv[2]/GEOMETRYNAME_vertex.bin:
        position vertices       4*
        normal vertices         4*
        uvmap data              4*
        color data              4*
    """
    NVALUE = -1;
    for data in datalist:
        # write to datamap.bin
        filepath = "{}/{}_datamap.bin".format(sys.argv[2], data["geometry_name"]);
        with (DummyWriter() if DEBUG_MODE else open(filepath, "wb")) as f: 
            print("write: {}_datamap.bin".format(data["geometry_name"]));
            write(f, "<1i", 1);                         # output type
            ofs = 0;
            value_count = data["position_value_count"];
            write(f, "<1i", value_count);               # position value count
            write(f, "<1i", ofs);                       # position data offset
            ofs += value_count * 4;
            value_count = data.get("normal_value_count", NVALUE);
            write(f, "<1i", value_count);               # normal value count
            write(f, "<1i", ofs);                       # normal data offset
            ofs += max(value_count, 0) * 4;
            value_count = data.get("uv_value_count", NVALUE);
            write(f, "<1i", value_count);               # texcoord value count
            write(f, "<1i", ofs);                       # texcoord data offset
            ofs += max(value_count, 0) * 4;
            value_count = data.get("color_value_count", NVALUE);
            write(f, "<1i", value_count);               # color value count
            write(f, "<1i", ofs);                       # color data offset
            print();
        # write to vertex.bin
        filepath = "{}/{}_vertex.bin".format(sys.argv[2], data["geometry_name"]);
        with (DummyWriter() if DEBUG_MODE else open(filepath, "wb")) as f: 
            print("write: {}_vertex.bin".format(data["geometry_name"]));
            # position vertices
            value = data["position_value"];
            for idx in data["position_index"]:
                x, y, z = value[idx*3 : idx*3+3];
                write(f, "<3f", x, y, z);
            # normal vertices
            value = data.get("normal_value");
            if value:
                for idx in data["normal_index"]:
                    x, y, z = value[idx*3 : idx*3+3];
                    write(f, "<3f", x, y, z);
            # texcoord data
            value = data.get("texcoord_value");
            if value:
                for idx in data["texcoord_index"]:
                    u, v = value[idx*2 : idx*2+2];
                    write(f, "<2f", u, v);
            # color data
            value = data.get("color_value");
            if value:
                for idx in data["color_index"]:
                    r, g, b = value[idx*3 : idx*3+3];
                    write(f, "<3f", r, g, b);
            print()
# 
# main process 
# 
def main():
    """main process.
    """
    # check input arguments
    if DEBUG_MODE:
        if len(sys.argv) <= 1:
            print("invalid arguments: not enough arguments.");
            sys.exit();
        if not os.path.isfile(sys.argv[1]):
            print("invalid arguments: first argument　be required to specify the file path.");
            sys.exit();
        # adjust the argument length
        if len(sys.argv) == 2:
            sys.argv.append("hoge");
    else:
        if len(sys.argv) <= 2:
            print("invalid arguments: not enough arguments.");
            sys.exit();
        if not os.path.isfile(sys.argv[1]):
            print("invalid arguments: first argument　be required to specify the file path.");
            sys.exit();
        if not os.path.isdir(sys.argv[2]):
            print("invalid arguments: second argument　be required to type the directory path.");
            sys.exit();

    # collada namespace
    namespaces = {"NS":"http://www.collada.org/2005/11/COLLADASchema"};

    # input the file and parse
    try:
        tree = ElementTree.parse(sys.argv[1]);
        root = tree.getroot();
    except:
        print("unexpected error", sys.exc_info()[0]);
        raise;

    # 
    try:
        # declare the library class
        library_materials = LibraryMaterials();
        library_images = LibraryImages();
        library_geometries = LibraryGeometries();
        library_materials = LibraryMaterials();
        library_effects = LibraryEffects();

        # make the library
        for child in root:
            m = re.search("(?<=\})(.*)", child.tag);
            tag = m.group(0);
            if "asset" == tag: pass
            # do not need information
            elif "library_cameras" == tag: pass
            # do not need information
            elif "library_lights" == tag: pass
            # do not need information
            elif "library_controllers" == tag: pass
            # do not need information
            elif "library_visual_scenes" == tag: pass
            # do not need information
            elif "scene" == tag: pass
            elif "library_effects" == tag: 
                # get effects elements
                effect_elements = child.findall("NS:effect", namespaces);
                # register each element
                for elem in effect_elements:
                    effect = EffectElement(elem, namespaces);
                    library_effects.addElement(effect);

            elif "library_materials" == tag:
                # get material elements
                material_elements = child.findall("NS:material", namespaces);
                # register each element
                for elem in material_elements:
                    material = MaterialElement(elem, namespaces);
                    library_materials.addElement(material);

            elif "library_images" == tag: 
                # get image elements
                image_elements = child.findall("NS:image", namespaces);
                # register each element
                for elem in image_elements:
                    image = ImageElement(elem, namespaces);
                    library_images.addElement(image);

            elif "library_geometries" == tag:
                # get geometry element
                geometry_elements = child.findall("NS:geometry", namespaces);
                # register each elements
                for elem in geometry_elements:
                    geometry = GeometryElement(elem, namespaces);
                    library_geometries.addElement(geometry);

        # declare the data info to write
        data_list = [];
        # data = {};
        # data["geometry_name"]         = None;
        # data["position_value"]        = None;
        # data["position_value_count"]  = None;
        # data["position_index"]        = None;
        # data["normal_value"]          = None;
        # data["normal_value_count"]    = None;
        # data["normal_index"]          = None;
        # data["texcoord_value"]        = None;
        # data["texcoord_value_count"]  = None;
        # data["texcoord_index"]        = None;
        # data["color_value"]           = None;
        # data["color_value_count"]     = None;
        # data["color_index"]           = None;
        # data["material_count"]        = None;
        # data["material_image_name"]   = None;
        # data["vertex_count"]          = None;

        # store the data to write
        for geo in library_geometries:
            sourcesElemList     = geo.mesh.sourceElementList;
            verticesElemList    = geo.mesh.verticesElementList;
            polylistElemList    = geo.mesh.polylistElementList;

            # store the data for each element polylist
            for polylist in polylistElemList:
                
                data = {};
                iecount = polylist.inputElementCount;
                # geometry name
                data["geometry_name"] = geo.name;
                # position data
                if polylist.hasPosition:
                    # extract source text in vertices element
                    sourceRef = polylist.inputPositionSource;
                    vertices = list(filter(lambda e: e.match(sourceRef), verticesElemList));
                    if vertices:
                        sourceRef = vertices[0].source;
                    # target sources
                    target_sources = list(filter(lambda e: e.match(sourceRef), sourcesElemList));
                    assert target_sources, "can not find sources position.";
                    ts = target_sources[0];
                    offset = polylist.inputPositionOffset;
                    data["position_value"]          = ts.value;
                    data["position_value_count"]    = ts.count;
                    data["position_index"]          = polylist.p[offset::iecount];
                # normal data
                if polylist.hasNormal:
                    sourceRef = polylist.inputNormalSource;
                    target_sources = list(filter(lambda e: e.match(sourceRef), sourcesElemList));
                    assert target_sources, "can not find sources normal.";
                    ts = target_sources[0];
                    offset = polylist.inputNormalOffset;
                    data["normal_value"]        = ts.value;
                    data["normal_value_count"]  = ts.count;
                    data["normal_index"]        = polylist.p[offset::iecount];
                # texcoord data
                if polylist.hasTexcoord:
                    sourceRef = polylist.inputTexcoordSource;
                    target_sources = list(filter(lambda e: e.match(sourceRef), sourcesElemList));
                    assert target_sources, "can not find sources texcoord.";
                    ts = target_sources[0];
                    offset = polylist.inputTexcoordOffset;
                    data["texcoord_value"]          = ts.value;
                    data["texcoord_value_count"]    = ts.count;
                    data["texcoord_index"]          = polylist.p[offset::iecount];
                # color data
                if polylist.hasColor:
                    sourceRef = polylist.inputColorSource;
                    target_sources = list(filter(lambda e: e.match(sourceRef), sourcesElemList));
                    assert target_sources, "can not find sources color.";
                    ts = target_sources[0];
                    offset = polylist.inputColorOffset;
                    data["color_value"]         = ts.value;
                    data["color_value_count"]   = ts.count;
                    data["color_index"]         = polylist.p[offset::iecount];
                # material data
                if polylist.material:
                    target_material = util.filterForOnly(
                        lambda e: e.match(polylist.material), 
                        library_materials, "can not find material object.");
                    target_effect = util.filterForOnly(
                        lambda e: e.match(target_material.instanceEffectUrl[1:]), 
                        library_effects, "can not find effect object.");
                    data["material_count"]      = len(target_effect.surfaceElementList);
                    data["material_image_name"] = target_effect.surfaceElementList;

                # vertex count
                data["vertex_count"] = polylist.vertexCount;
                # append the datalist
                data_list.append(data);
        # write binary
        if USE_INDICES:
            writeBinaryWithIndices(data_list);
        else:
            writeBinary(data_list);
    except:
        print("unexpected error", sys.exc_info()[0]);
        raise;

# 
# entry point
# 
if __name__ == '__main__':
    main();