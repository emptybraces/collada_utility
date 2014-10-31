# class Element
# parent class of all element class
class Element:
    """docstring for ClassName"""
    def __init__(self, element, namespaces):
        self.id = element.attrib["id"];
        
    def splitArray(self, array, stride):
        r = [];
        s = 0; e = stride;
        for x in range(int(len(array)/stride)):
            r.append(array[s:e]);
            s += stride;
            e += stride;
        return r;

# class ImageElement
# class ImageElement(Element):
#     """docstring for ClassName"""
#     def __init__(self, element, namespaces):
#         super(self.__class__, self).__init__(element, namespaces);
#         float_array = element.find("NS:float_array", namespaces);
#         text = float_array.text;
#         self.count = float_array.attrib["count"];
#         stride = 3; # TODO: get from accessor attribute
#         # self.data = self.splitArray(text.split(" "), stride);
#         self.data = text.split();

# class SourceElement
# <source> element information
class SourceElement(Element):
    """docstring for ClassName"""
    def __init__(self, element, namespaces):
        super(self.__class__, self).__init__(element, namespaces);
        float_array = element.find("NS:float_array", namespaces);
        text = float_array.text;
        self.count = float_array.attrib["count"];
        stride = 3; # TODO: get from accessor attribute
        # self.data = self.splitArray(text.split(" "), stride);
        self.data = text.split();
    def match(self, source):
        return True if source.find(self.id) != -1 else False;

# class VerticesElement
# <vertices> element information
class VerticesElement:
    """docstring for ClassName"""
    def __init__(self, element, namespaces):
        self.id = element.attrib["id"];
        self.semantic = element.find("NS:input", namespaces).attrib["semantic"];
        self.input = element.find("NS:input", namespaces).attrib;
    def match(self, source):
        return self.input["source"] if source.find(self.id) != -1 else None;

# class Polylist Element
# <polylist> element information
class PolylistElement:
    """docstring for ClassName"""
    def __init__(self, element, namespaces):
        self.input = [];
        for elem in element.findall("NS:input", namespaces):
            self.input.append(elem.attrib)
        self.vcount = element.find("NS:vcount", namespaces).text.split();
        self.vcount = list(map(lambda x: int(x), self.vcount));
        self.p = element.find("NS:p", namespaces).text.split();
        self.p = list(map(lambda x: int(x), self.p));
    def totalVCount(self):
        # return reduce(lambda x, y: int(x) + int(y), self.vcount);
        return sum(self.vcount);

# Dummy Class
# Instead of binary output
# print() function can not be used with binary mode.
class DebugPrint:
    def write(self, fmt, *args):
        string = "";
        for arg in args:
            string += " " + str(arg);
        print(string.lstrip(), end=" ");

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass;
