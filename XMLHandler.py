from typing import ByteString
import zipfile
import os
from lxml import etree
from Consts import XML_FOLDER, PAPERS_FOLDER
import pandas as pd
import Utils
import docx
from shutil import copy, rmtree


class XMLHandler:
    def __init__(self, paper_date, rows_for_date):
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
        self.rows_for_date = rows_for_date
        self.map_rId_to_image_name()
        self.build_namespaces_dict()
        self.find_all_images_in_xml()

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
                            if(wframe_element is None):
                                break
                            cords['page'] = self.page_numbers[-1]
                            cords['x'] = int(
                                wframe_element.attrib[self.ns['w']+'x'])
                            cords['y'] = int(
                                wframe_element.attrib[self.ns['w']+'y'])
                            self.image_data[rId] = cords
                        except Exception as e:
                            print(e)
                            raise(e)
                self.images_elements.append(elem)
            elif(elem.tag == self.ns["w"]+'footnotePr'):
                self.page_numbers.append(self.page_numbers[-1]+1)
        print(self.image_data)

    def find_application_numbers_tags_of_images(self, application_numbers_to_search, text_app_nums, verification_level=1):
        application_numers_left = application_numbers_to_search.copy()
        self.application_numbers_cords = {}
        pages = [0]
        for elem in self.tree.iter():
            if(len(application_numers_left) == 0):
                break
            if(elem.tag == self.ns['w']+'p'):
                text = self.get_text_from_paragraph(elem)
                if(Utils.check_if_string_contain_appnum_tag(text)):
                    result = Utils.is_array_element_in_string(
                        text, application_numers_left)
                    if(result != -1):
                        app_num = result
                        x, y = self.get_cords_from_paragraph(elem)
                        self.application_numbers_cords[str(app_num)] = {
                            'x': x, 'y': y, 'page': pages[-1]}
                        if(app_num in application_numers_left):
                            application_numers_left.remove(app_num)
                    elif(verification_level == 2):
                        numbers = Utils.parse_numbers_from_string(
                            text, self.rows_for_date, application_numers_left)
                        if(len(numbers) > 0):
                            if(Utils.is_array_element_in_string(text, [numbers[0]]) and numbers[0] not in text_app_nums):
                                app_num = numbers[0]
                                if(app_num == -1):
                                    continue
                                x, y = self.get_cords_from_paragraph(elem)
                                self.application_numbers_cords[str(app_num)] = {
                                    'x': x, 'y': y, 'page': pages[-1]}
                                if(app_num in application_numers_left):
                                    application_numers_left.remove(app_num)

            elif(elem.tag == self.ns["w"]+'footnotePr'):
                pages.append(pages[-1]+1)
        print(self.application_numbers_cords)

    def match_between_image_and_app_num(self):
        matches = {}
        for key in self.application_numbers_cords.keys():
            tag_page = int(self.application_numbers_cords[key]['page'])
            tag_x = int(self.application_numbers_cords[key]['x'])
            tag_y = int(self.application_numbers_cords[key]['y'])
            best = self.get_image_candidate_by_tag(tag_page, tag_x, tag_y)
            matches[key] = best
        for app_num, rId in matches.items():
            if(rId is not None):
                image_name = self.rId_dict[rId]
                matches[app_num] = image_name
            else:
                matches[app_num] = -1
        print(matches)
        return matches

    def get_image_candidate_by_tag(self, tag_page, tag_x, tag_y):
        candidates = {}
        best = None
        # calculate which images havent been used yet
        images_not_used = {}
        for key, value in self.image_data.items():
            if('used' not in value.keys()):
                images_not_used[key] = value
        # find best image according to it's position and tag position
        for key, value in images_not_used.items():
            # picture is on the left bar on the same page
            if(value['page'] == tag_page and tag_y <= value['y'] and ((tag_x < 4000 and value['x'] < 4000) or (tag_x > 4000 and value['x'] > 4000))):
                candidates[key] = self.image_data[key]
        if(len(candidates) > 0):
            min_y = 100000000
            for k, v in candidates.items():
                if(v['y'] < min_y):
                    min_y = v['y']
                    best = k
            self.image_data[k]['used'] = 1
            return best
        else:
            for key, value in images_not_used.items():
                if(value['page'] == tag_page and tag_y >= value['y'] and ((tag_x < 4000 and value['x'] > 4000))):
                    candidates[key] = self.image_data[key]
        if(len(candidates) > 0):
            min_y = 100000000
            for k, v in candidates.items():
                if(v['y'] < min_y):
                    min_y = v['y']
                    best = k
            self.image_data[k]['used'] = 1
            return best
        else:
            # picture is on the right bar on the next page
            for key, value in images_not_used.items():
                if(value['page'] == tag_page+1 and tag_y >= value['y'] and ((tag_x > 4000 and value['x'] < 4000))):
                    candidates[key] = self.image_data[key]
        if(len(candidates) > 0):
            min_y = 100000000
            for k, v in candidates.items():
                if(v['y'] < min_y):
                    min_y = v['y']
                    best = k
            self.image_data[k]['used'] = 1
            return best
        else:
            return best

    def build_namespaces_dict(self):
        self.ns["w"] = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        self.ns["a"] = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

    # for example tag = <a:blip> and type_tage=<Drawing> wil return the ancestor of <a:blip> that is from type <Drawing>
    def get_ancestor_by_type(self, tag, type_tag):
        parent = tag.getparent()
        while(parent.tag != type_tag or parent.tag == self.ns["w"]+'document'):
            parent = parent.getparent()
        return parent

    # get w:p tag and extract it's cordinates using w:framePr x w:x and w:y
    def get_cords_from_paragraph(self, p_tag):
        w_ppr = p_tag.find(self.ns['w']+'pPr')
        w_frame_pPr = w_ppr.find(self.ns['w']+'framePr')
        x = w_frame_pPr.attrib[self.ns['w']+'x']
        y = w_frame_pPr.attrib[self.ns['w']+'y']
        return x, y

    def get_text_from_paragraph(self, p_tag):
        text = ""
        w_rs = p_tag.findall(self.ns['w']+'r')
        for w_r in w_rs:
            w_t = w_r.find(self.ns['w']+'t')
            text += w_r.find(self.ns['w']+'t').text + \
                ' ' if w_t is not None else ""
        return text

    # if __name__ == '__main__':
    #     try:
    #         from XMLHandler import XMLHandler
    #         xml = XMLHandler('48-02-12')
    #         xml.find_all_images_in_xml()
    #         xml.find_application_numbers_tags_of_images(
    #             [7589, 7823, 8684, 8704, 8772, 8877, 8973, 8974, 9010, 9042, 9043, 9099])
    #         matches = xml.match_between_image_and_app_num()
    #         rmtree('./'+XML_FOLDER+'/'+'48-02-12')
    #     except Exception as e:
    #         rmtree('./'+XML_FOLDER+'/'+'48-02-12')
    #         raise(e)
