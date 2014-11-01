import sys
import re
import struct
import math
# from xml.etree import ElementTree
from xml.etree import ElementTree
from classes import *
# const variable definition
DEBUG_MODE = True;
USE_INDICES = False;

# functions
def write(file, fmt, *args):
    if DEBUG_MODE:
        file.write(fmt, *args);
    else:
        file.write(struct.pack(fmt, *args));
def normalize(values):
    x = values[0];
    y = values[1];
    z = values[2];
    length = x*x + y*y + z*z;
    out = [x, y, z];
    if length > 0:
        length = 1 / math.sqrt(length);
        out[0] = x * length;
        out[1] = y * length;
        out[2] = z * length;
    return out;
#
# write to a file the custom model data include indices.
#
# datamap
# name, byte
# mode,					4
# position semantic, 	4
# position data count, 	4
# normal semantic, 		4
# normal data count, 	4
# common semantic, 		4 
# indices count, 		4
# indices data,			2 * indices count
# position data,		4 * position data count
# normal data,			4 * normal data count
# 
def writeBinaryWithIndices(f, datalist):
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
def writeBinary(f, datalist):
    """
    write to a file the custom model data.
    
    datamap
    column: name, byte(*=variable length)
    custom type,                4
    geometry name,              *
    material name,              *
    position semantic,          4
    position data count,  4
    normal semantic,      4
    normal data count,    4
    common semantic,      4 
    position data,        4 * position data count
    normal data,          4 * normal data count
    """
    pos_semantic = None;
    pos_indices = None;
    pos_vertex = None;
    normal_semantic = None;
    normal_indices = None;
    normal_vertex = None;
    # collect write info
    for m in data_map:
        # vertex info
        if m["semantic"] == "VERTEX":
            pos_semantic = ord(m["semantic"][0]);
            pos_indices = m["index"];
            pos_vertex = m["vertex"];
        # normal info
        elif m["semantic"] == "NORMAL":
            normal_semantic = ord(m["semantic"][0]);
            normal_indices = m["index"];
            normal_vertex = m["vertex"];

    new_vertex_pos = [];
    for pi in pos_indices:
        x = float(pos_vertex[pi * 3 + 0]);
        y = float(pos_vertex[pi * 3 + 1]);
        z = float(pos_vertex[pi * 3 + 2]);
        new_vertex_pos.append(x);
        new_vertex_pos.append(y);
        new_vertex_pos.append(z);

    new_vertex_normal = [];
    for ni in normal_indices:
        x = float(normal_vertex[ni * 3 + 0]);
        y = float(normal_vertex[ni * 3 + 1]);
        z = float(normal_vertex[ni * 3 + 2]);
        new_vertex_normal.append(x);
        new_vertex_normal.append(y);
        new_vertex_normal.append(z);
    # write
    print("header part:");
    write(f, "<1i", 1);
    write(f, "<2i", pos_semantic, v_num * 3);
    write(f, "<2i", normal_semantic, v_num * 3);
    write(f, "<1i", ord("Common"[0]));

    print("\ndata part:");
    # vertex data
    for elem in new_vertex_pos: 
        write(f, "<1f", elem);
    print();
    # normal data
    for elem in new_vertex_normal:
        write(f, "<1f", elem);
    print();
# 
# main process 
# 
def main():
    """main process.
    """
    if len(sys.argv) <= (2 if not DEBUG_MODE else 1):
        print("invalid arguments");
        sys.exit();

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
            elif "library_effects" == tag: pass
            # do not need information
            elif "library_controllers" == tag: pass
            # do not need information
            elif "library_visual_scenes" == tag: pass
            # do not need information
            elif "scene" == tag: pass
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
        # data["material"]              = None;
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
                data["material"] = polylist.material;
                # vertex count
                data["vertex_count"] = polylist.vertexCount;
                # append the datalist
                data_list.append(data);
        # write binary
        # with (open(sys.argv[2], 'wb' ) if not DEBUG_MODE else DebugPrint()) as f:
        # 	if USE_INDICES:
        # 		writeBinaryWithIndices(f, data_list);
        # 	else:
        # 		writeBinary(f, data_list);
    except:
        print("unexpected error", sys.exc_info()[0]);
        raise;

# 
# entry point
# 
if __name__ == '__main__':
    main();