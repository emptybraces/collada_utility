import sys
import inspect
import util
class Library:
    """parent class of all library classes.
    """
    def __init__(self):
        self._elements = [];
    @property
    def elements(self):
        return self._elements;
    def addElement(self, element):
        self.elements.append(element);
    def __iter__(self):
        return iter(self.elements);

class LibraryMaterials(Library):
    """manage for MaterialElement class.
    """
    def __init__(self):
        super().__init__();
class LibraryEffects(Library):
    """manage for EffectElement class.
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
class LibraryVisualScenes(Library):
    """manage for VisualSceneElement class.
    """
    def __init__(self):
        super().__init__();

class Element:
    """parent class of all element class
    """
    def __init__(self, element, namespaces):
        self._id = element.attrib.get("id");
        self._sid = element.attrib.get("sid");
        self._name = element.attrib.get("name");
        self._type = element.attrib.get("type");
    @property
    def id(self): return self._id;
    @property
    def sid(self): return self._sid;
    @property
    def name(self): return self._name;
    @property
    def type(self): return self._type;
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
    def match(self, id):
        return id == self.id;

class MaterialElement(Element):
    """<material> element information"""
    def __init__(self, element, namespaces):
        super().__init__(element, namespaces);
        self._instanceEffectUrl = element.find("NS:instance_effect", namespaces).attrib.get("url");
    @property
    def instanceEffectUrl(self):
        return self._instanceEffectUrl;
    
class EffectElement(Element):
    """<effect> element information"""
    def __init__(self, element, namespaces):
        super().__init__(element, namespaces);
        self._surfaceElementList = [];
        for elem in element.findall("NS:profile_COMMON/NS:newparam/NS:surface", namespaces):
            surface = {"type":elem.attrib["type"], "initfrom": elem.find("NS:init_from", namespaces).text};
            self.surfaceElementList.append(surface);
    @property
    def surfaceElementList(self): return self._surfaceElementList;

# class NewparamElement(Element):
#     """<newparam> element information"""
#     def __init__(self, element, namespaces):
#         super().__init__(element, namespaces);
#         surface_element = element.find("NS:surface", namespaces);
#         self._surfaceType = surface_element.attrib.get("type");
#         self._surfaceInitfrom = element.find("NS:surface/NS:init_from", namespaces).text;
#         self._sampler2DSource = element.find("NS:sampler2D/NS:source", namespaces).text;
#     @property
#     def surfaceType(self):     return self._surfaceType;
#     @property
#     def surfaceInitfrom(self): return self._surfaceInitfrom;
#     @property
#     def sampler2DSource(self): return self._sampler2DSource;

class ImageElement(Element):
    """<image> element information"""
    def __init__(self, element, namespaces):
        super().__init__(element, namespaces);
        self._initfrom = element.find("NS:init_from", namespaces).text;
    @property
    def initfrom(self): return self._initfrom;

class GeometryElement(Element):
    """<geometry> element information"""
    def __init__(self, element, namespaces):
        super().__init__(element, namespaces);
        mesh = element.find("NS:mesh", namespaces);
        self._mesh = MeshElement(mesh, namespaces);
    @property
    def mesh(self):
        return self._mesh;

class MeshElement(Element):
    """<mesh> element information"""
    def __init__(self, element, namespaces):
        super().__init__(element, namespaces);
        self._sourceElementList = list(map(
            lambda elem: SourceElement(elem, namespaces),
            element.findall("NS:source", namespaces)));
        self._verticesElementList = list(map(
            lambda elem: VerticesElement(elem, namespaces),
            element.findall("NS:vertices", namespaces)));
        self._polylistElementList = list(map(
            lambda elem: PolylistElement(elem, namespaces),
            element.findall("NS:polylist", namespaces)));
    @property
    def sourceElementList(self):
        return self._sourceElementList;
    @property
    def verticesElementList(self):
        return self._verticesElementList;
    @property
    def polylistElementList(self):
        return self._polylistElementList;

class SourceElement(Element):
    """<source> element information"""
    def __init__(self, element, namespaces):
        super(self.__class__, self).__init__(element, namespaces);
        float_array = element.find("NS:float_array", namespaces);
        self._value = util.convertElementType(float_array.text.split(), float);
        self._count = int(float_array.attrib.get("count"));
        # stride = 3; # TODO: get from accessor attribute
        # self.data = self.splitArray(text.split(" "), stride);
    @property
    def value(self):
        return self._value;
    @property
    def count(self):
        return self._count;

class VerticesElement(Element):
    """<vertices> element information"""
    def __init__(self, element, namespaces):
        super().__init__(element, namespaces);
        _input = element.find("NS:input", namespaces)
        self._semantic = _input.attrib.get("semantic");
        self._source = _input.attrib.get("source");
    @property
    def semantic(self):
        return self._semantic;
    @property
    def source(self):
        return self._source;

class PolylistElement(Element):
    """<polylist> element information"""
    def __init__(self, element, namespaces):
        super().__init__(element, namespaces);
        # declare member variable
        self._hasPosition    = False;
        self._hasNormal      = False;
        self._hasTexcoord    = False;
        self._hasColor       = False;
        # get the input information
        input_element_count = 0;
        for elem in element.findall("NS:input", namespaces):
            input_element_count += 1;
            semantic = elem.attrib.get("semantic");
            if semantic == "VERTEX":
                self._hasPosition           = True;
                self._inputPositionSource   = elem.attrib.get("source");
                self._inputPositionOffset   = int(elem.attrib.get("offset"));
                self._inputPositionSet      = elem.attrib.get("set");
            elif semantic == "NORMAL":
                self._hasNormal             = True;
                self._inputNormalSource     = elem.attrib.get("source");
                self._inputNormalOffset     = int(elem.attrib.get("offset"));
                self._inputNormalSet        = elem.attrib.get("set");
            elif semantic == "TEXCOORD":
                self._hasTexcoord           = True;
                self._inputTexcoordSource   = elem.attrib.get("source");
                self._inputTexcoordOffset   = int(elem.attrib.get("offset"));
                self._inputTexcoordSet      = elem.attrib.get("set");
            elif semantic == "COLOR":
                self._hasColor              = True;
                self._inputColorSource      = elem.attrib.get("source");
                self._inputColorOffset      = int(elem.attrib.get("offset"));
                self._inputColorSet         = elem.attrib.get("set");
        # get the matrial
        self._material = element.attrib.get("material");
        # get the vertex count
        self._vertexCount = element.attrib.get("count");
        # get the value count
        self._valueCount = sum(util.convertElementType(element.find("NS:vcount", namespaces).text.split(), int));
        # get the p
        self._p = util.convertElementType(element.find("NS:p", namespaces).text.split(), int);
        # input element count
        self._inputElementCount = input_element_count;
    @property 
    def hasPosition(self):          return self._hasPosition;
    @property 
    def hasNormal(self):            return self._hasNormal;
    @property 
    def hasTexcoord(self):          return self._hasTexcoord;
    @property 
    def hasColor(self):             return self._hasColor;
    @property 
    def inputPositionSource(self):  return self._inputPositionSource;
    @property 
    def inputPositionOffset(self):  return self._inputPositionOffset;
    @property
    def inputPositionSet(self):     return self._inputPositionSet;
    @property
    def inputNormalSource(self):    return self._inputNormalSource;
    @property
    def inputNormalOffset(self):    return self._inputNormalOffset;
    @property
    def inputNormalSet(self):       return self._inputNormalSet;
    @property
    def inputTexcoordSource(self):  return self._inputTexcoordSource;
    @property
    def inputTexcoordOffset(self):  return self._inputTexcoordOffset;
    @property
    def inputTexcoordSet(self):     return self._inputTexcoordSet;
    @property
    def inputColorSource(self):     return self._inputColorSource;
    @property
    def inputColorOffset(self):     return self._inputColorOffset;
    @property
    def inputColorSet(self):        return self._inputColorSet;
    @property
    def material(self):             return self._material;
    @property
    def vertexCount(self):          return self._vertexCount;
    @property
    def valueCount(self):           return self._valueCount;
    @property
    def p(self):                    return self._p;
    @property
    def inputElementCount(self):    return self._inputElementCount;

class VisualSceneElement(Element):
    """<visual_scene> element information"""
    def __init__(self, element, namespaces):
        super().__init__(element, namespaces);
        self._nodeElementList = list(map(
            lambda elem: NodeElement(elem, namespaces),
            element.findall("NS:node", namespaces)));
    @property
    def nodeElementList(self):
        return self._nodeElementList;

class NodeElement(Element):
    """<node> element information"""
    def __init__(self, element, namespaces):
        super().__init__(element, namespaces);
        self._matrix = element.find("NS:matrix", namespaces).text;
        for elem in ["instance_camera", "instance_light", "instance_geometry"]:
            self._instanceUrl = element.find("NS:"+elem, namespaces)
            if self._instanceUrl is not None:
                self._instanceUrl = self._instanceUrl.attrib["url"];
                return;
    @property
    def matrix(self):
        m = Matrix();
        matrix = util.convertElementType(self._matrix.split(), float);
        transpose = m.transpose(matrix);
        return transpose;
    @property
    def instanceUrl(self):
        return self._instanceUrl;
    def matchUrl(self, url):
        return self._instanceUrl[1:] == url;


class DummyWriter:
    """ DummyWriter Class
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

class Matrix:
    """ Matrix operator class"""
    def multiplyVec3(self, m, a):
        x = a[0]; y = a[1]; z = a[2];
        w = m[3] * x + m[7] * y + m[11] * z + m[15];
        if w == 0: w = 1.0;
        # print("w = ", w)
        out = [0 for i in range(3)];  
        out[0] = (m[0] * x + m[4] * y + m[8] * z + m[12]) / w;
        out[1] = (m[1] * x + m[5] * y + m[9] * z + m[13]) / w;
        out[2] = (m[2] * x + m[6] * y + m[10] * z + m[14]) / w;
        return out;
    def transpose(self, m):
        out = [0 for i in range(16)];
        out[0] = m[0];
        out[1] = m[4];
        out[2] = m[8];
        out[3] = m[12];
        out[4] = m[1];
        out[5] = m[5];
        out[6] = m[9];
        out[7] = m[13];
        out[8] = m[2];
        out[9] = m[6];
        out[10] = m[10];
        out[11] = m[14];
        out[12] = m[3];
        out[13] = m[7];
        out[14] = m[11];
        out[15] = m[15];
        return out;

