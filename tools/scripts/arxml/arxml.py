import os
import xml.etree.ElementTree as ET
from datetime import datetime



def finalize_arxml_doc(file):
   with open(file, "r") as f:
      contents = f.readlines()
   comment = "<!-- Generated by OSEK Builder tool of FreeOSEK project on " + str(datetime.now()) + " -->\n"
   contents.insert(1, comment)
   with open(file, "w") as f:
      contents = "".join(contents)
      f.write(contents)


def build_Ecuc_package(root):
   arpkg = ET.SubElement(root, "AR-PACKAGE")
   shortname = ET.SubElement(arpkg, "SHORT-NAME")
   shortname.text = "Ecuc"
   elements = ET.SubElement(arpkg, "ELEMENTS")



def export(path):
   if not os.path.exists(path):
      os.makedirs(path)
   outfile = path+"/output.arxml"
   
   root = ET.Element("AUTOSAR")
   tree = ET.ElementTree(root)
   arpkgs = ET.SubElement(root, "AR-PACKAGES")
   build_Ecuc_package(arpkgs)

   print("export.py::export in "+ path)
   ET.indent(tree, space="\t", level=0)
   tree.write(outfile, encoding="utf-8", xml_declaration=True)
   finalize_arxml_doc(outfile)



if __name__ == '__main__':
   print("export.py::__main__")