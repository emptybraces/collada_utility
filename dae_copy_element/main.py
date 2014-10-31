import sys
import re
import os.path
# from xml.etree import ElementTree
from xml.etree import ElementTree

# const variable definition
DEBUG_MODE = True;
# function definition
def getTag(elem):
    return re.search("(?<=\})(.*)", elem.tag).group(0);
def main():
    if len(sys.argv) <= 1:
        print("invalid arguments");
        sys.exit();

    namespaces = {"NS":"http://www.collada.org/2005/11/COLLADASchema"};
    # input the file and parse contents
    try:
        tree = ElementTree.parse(sys.argv[1]);
        root = tree.getroot();
    except:
        print("unexpected error", sys.exc_info()[0]);
        raise;

    # write the file
    try:
        with open(sys.argv[1], 'r' ) as rf:
            rt = rf.readline();
            ns = rf.readline();
            for child in root:
                tag = getTag(child);
                filepath = sys.argv[1] + "." + tag;
                with open(filepath, 'w' ) as wf:
                    wf.write(rt);
                    wf.write(ns);
                    # start tag(<...>)
                    start_tag = rf.readline();
                    wf.write(start_tag);
                    # in case of end tag(<.../>)
                    if "<{}/>".format(tag) in start_tag:
                        continue;
                    for line in rf:
                        wf.write(line);
                        # end tag
                        if "</{}>".format(tag) in line:
                            break;

    except:
        print("unexpected error", sys.exc_info()[0]);
        raise;
# entry point
if __name__ == '__main__':
    main()
