import sys
import inspect

class Library:
    """parent class of all library classes.
    """
    def __init__(self, lst = []):
        self._elements = lst;
    @property
    def elements(self):
        return self._elements;
    def addElement(self, element):
        self._elements.append(element);

class LibraryMaterials(Library):
    """manage for MaterialElement class.
    """
    def __init__(self):
        super().__init__();

class LibraryImages(Library):
    """manage for ImageElement class.
    """
    def __init__(self):
        super().__init__();

class LibraryGeometries(Library):
    """manage for GeometryElement class.
    """
    def __init__(self):
        super().__init__();

class Element:
    """parent class of all element class
    """
    def __init__(self, element, namespaces):
        self._id = element.attrib.get("id");
        self._name = element.attrib.get("name");
    @property
    def id(self):
        return self._id;
    @property
    def name(self):
        return self._name
    def splitArray(self, array, stride):
        r = [];
        s = 0; e = stride;
        for x in range(int(len(array)/stride)):
            r.append(array[s:e]);
            s += stride;
            e += stride;
        return r;
    def debugPrint(self, clazz):
        print(vars(clazz));

class MaterialElement(Element):
    """<material> element information"""
    def __init__(self, element, namespaces):
        super().__init__(element, namespaces);
        self._instanceEffectUrl = element.find("NS:instance_effect", namespaces).attrib.get("url");
    @property
    def instanceEffectUrl(self):
        return self._instanceEffectUrl;
    
class ImageElement(Element):
    """<image> element information"""
    def __init__(self, element, namespaces):
        super().__init__(element, namespaces);
        self._url = element.find("NS:init_from", namespaces).text;
    @property
    def url(self):
        return self._url;

class GeometryElement(Element):
    """<geometry> element information"""
    def __init__(self, element, namespaces):
        super().__init__(element, namespaces);
        mesh = element.find("NS:mesh", namespaces);
        self._mesh = MeshElement(mesh);
    @property
    def mesh(self):
        return self._mesh

class MeshElement(Element):
    """<mesh> element information"""
    def __init__(self, element, namespaces):
        super().__init__(element, namespaces);
        self._sources = list(map(
            lambda elem: SourceElement(elem, namespaces),
            element.findall("NS:source", namespaces)));
        self._vertices = list(map(
            lambda elem: VerticesElement(elem, namespaces),
            element.findall("NS:vertices", namespaces)));
        self._polylist = list(map(
            lambda elem: PolylistElement(elem, namespaces),
            element.findall("NS:polylist", namespaces)));
    @property
    def sources(self):
        return self._sources;
    @property
    def vertices(self):
        return self._vertices;
    @property
    def polylist(self):
        return self._polylist;

class SourceElement(Element):
    """<source> element information"""
    def __init__(self, element, namespaces):
        super(self.__class__, self).__init__(element, namespaces);
        float_array = element.find("NS:float_array", namespaces);
        self.data = float_array.text.split();
        self._count = float_array.attrib.get("count";
        # stride = 3; # TODO: get from accessor attribute
        # self.data = self.splitArray(text.split(" "), stride);
    @property
    def count(self):
        return self._count
    def match(self, source):
        return True if source.find(self.id) != -1 else False;

class VerticesElement:
    """<vertices> element information"""
    def __init__(self, element, namespaces):
        _input = element.find("NS:input", namespaces)
        self._semantic = _input.attrib.get("semantic");
        self._source = _input.attrib.get("source");
    @property
    def semantic(self):
        return self._semantic;
    @property
    def source(self):
        return self._source;
    def match(self, source):
        return self.source if source.find(self.id) != -1 else None;

class PolylistElement:
    """<polylist> element information"""
    def __init__(self, element, namespaces):
        # get the input information
        for elem in element.findall("NS:input", namespaces):
            if elem.attrib.get("semantic") == "POSITION":
                self._input_position_source = elem.attrib.get("source");
                self._input_position_offset = elem.attrib.get("offset");
                self._input_position_set = elem.attrib.get("set");
            elif elem.attrib.get("semantic") == "NORMAL":
                self._input_normal_source = elem.attrib.get("source");
                self._input_normal_offset = elem.attrib.get("offset");
                self._input_normal_set = elem.attrib.get("set");
            elif elem.attrib.get("semantic") == "TEXCOORD":
                self._input_texcoord_source = elem.attrib.get("source");
                self._input_texcoord_offset = elem.attrib.get("offset");
                self._input_texcoord_set = elem.attrib.get("set");
            elif elem.attrib.get("semantic") == "COLOR":
                self._input_color_source = elem.attrib.get("source");
                self._input_color_offset = elem.attrib.get("offset");
                self._input_color_set = elem.attrib.get("set");
        # get the vcount
        self._vcount = element.find("NS:vcount", namespaces).text.split();
        self._vcount = list(map(lambda x: int(x), self.vcount));
        # get the p
        self._p = element.find("NS:p", namespaces).text.split();
        self._p = list(map(lambda x: int(x), self.p));
    @property def input_position_source(self):  return self._input_position_source;
    @property def input_position_offset(self):  return self._input_position_offset;
    @property def input_position_set(self):     return self._input_position_set;
    @property def input_normal_source(seaf):    return self._input_normal_source;
    @property def input_normal_offset(self):    return self._input_normal_offset;
    @property def input_normal_set(self):       return self._input_normal_set;
    @property def input_texcoord_source(self):  return self._input_texcoord_source;
    @property def input_texcoord_offset(self):  return self._input_texcoord_offset;
    @property def input_texcoord_set(self):     return self._input_texcoord_set;
    @property def input_color_source(self):     return self._input_color_source;
    @property def input_color_offset(self):     return self._input_color_offset;
    @property def input_color_set(self):        return self._input_color_set;
    @property def vcount(self):                 return self._vcount;
    @property def p(self):                      return self._p;
    def totalVCount(self):
        # return reduce(lambda x, y: int(x) + int(y), self.vcount);
        return sum(self.vcount);

class DebugPrint:
    """ Dummy Class
        Instead of binary output
        print() function can not be used with binary mode.
    """
    def write(self, fmt, *args):
        string = "";
        for arg in args:
            string += " " + str(arg);
        print(string.lstrip(), end=" ");

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass;
