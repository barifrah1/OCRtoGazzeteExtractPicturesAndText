import zipfile
import os
from lxml import etree
from Consts import XML_FOLDER, PAPERS_FOLDER
import pandas as pd
import Utils
import docx
from shutil import rmtree


class XMLHandler:
    def __init__(self, paper_date):
        self.paper_date = paper_date
        with zipfile.ZipFile('./'+PAPERS_FOLDER+'/'+paper_date+'.docx', "r") as zip_ref:
            path = './'+XML_FOLDER+'/'+paper_date
            Utils.create_folder_if_not_exist(path)

            zip_ref.extractall(path)
            xml_content = zip_ref.read('word/document.xml')
        tree = etree.fromstring(xml_content)
        self.tree = etree.ElementTree(tree)
        self.ns = {}  # namespace dict
        etree.indent(self.tree, space="\t", level=0)
        self.tree.write(path+'/indent.xml')
        self.images_path = path+'/word/media'
        self.images_names = os.listdir(self.images_path)
        self.map_rId_to_image_name()

        self.build_namespaces_dict()

    # map rId of all images from document.xml.rels file
    def map_rId_to_image_name(self):
        doc = docx.Document(docx='./'+PAPERS_FOLDER +
                            '/'+self.paper_date+'.docx')
        part = doc.part
        rels = part.rels
        self.rId_dict = {}
        for rel in rels.values():
            try:
                rId = rel.rId
                try:
                    target = rel.target_part
                except ValueError:
                    # rel.target_ref is from type media/imageX.jpeg
                    image_name = rel.target_ref.split('/')[1]
                    self.rId_dict[rId] = image_name
                    continue
                if('image' in target.content_type):
                    # target.partname is from type /word/media/imageX.jpeg
                    image_name = target.partname.split('/')[3]
                    self.rId_dict[rId] = image_name
                else:
                    continue
            except Exception as e:
                print(f"failed to extract rel from rels due to:{e}")
                continue

    def find_all_images_in_xml(self):
        self.images_elements = []
        self.image_data = {}
        self.page_numbers = [0]
        for elem in self.tree.iter():
            if(elem.tag == self.ns["w"]+'drawing'):
                rId = -1
                cords = {'page': -1, 'x': -1, 'y': -1}  # cordinates
                drawing = elem
                for e in drawing.iter():
                    if(e.tag == self.ns["a"]+'blip'):
                        ns = Utils.add_curly_braces_to_string(e.nsmap["r"])
                        rId = (e.attrib[ns+'embed'])
                        p_element = self.get_ancestor_by_type(
                            e, self.ns["w"]+'p')
                        try:
                            ppr_element = p_element.find(self.ns['w']+'pPr')
                            wframe_element = ppr_element.find(
                                self.ns['w']+'framePr')
                            cords['page'] = self.page_numbers[-1]
                            cords['x'] = wframe_element.attrib[self.ns['w']+'x']
                            cords['y'] = wframe_element.attrib[self.ns['w']+'y']
                            self.image_data[rId] = cords
                        except Exception as e:
                            print(e)
                            raise(e)
                self.images_elements.append(elem)
            elif(elem.tag == self.ns["w"]+'footnotePr'):
                self.page_numbers.append(self.page_numbers[-1]+1)
        print(self.image_data)

    def build_namespaces_dict(self):
        self.ns["w"] = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        self.ns["a"] = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

    # for example tag = <a:blip> and type_tage=<Drawing> wil return the ancestor of <a:blip> that is from type <Drawing>
    def get_ancestor_by_type(self, tag, type_tag):
        parent = tag.getparent()
        while(parent.tag != type_tag or parent.tag == self.ns["w"]+'document'):
            parent = parent.getparent()
        return parent

    if __name__ == '__main__':
        try:
            from XMLHandler import XMLHandler
            xml = XMLHandler('40-09-19')
            xml.find_all_images_in_xml()
            rmtree('./'+XML_FOLDER+'/'+'40-09-19')
        except Exception as e:
            rmtree('./'+XML_FOLDER+'/'+'40-09-19')
            raise(e)
