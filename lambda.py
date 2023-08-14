'''Python Script to the compatibilty for Level A WCAG Rule_1.2.1'''
import json
import logging
from bs4 import BeautifulSoup
import requests


def modify_tag(input_json):
    ''' Added Accessor Output '''
    new_json = {
        "type": "modify_tag",
        "data": {
            "selector": "",
            "tag": ""
        }
    }

    new_json['data']['selector'] = input_json['selector']
    new_json['data']['tag'] = input_json["editedContext"]

    return new_json


def checkingtextintitletag(node):
    '''Checking text value between opening and
    and closing title tag'''
    new_node = BeautifulSoup(node, "html.parser")
    title_tag_node_value = new_node.find('title').get_text()
    textvaluelength = len(title_tag_node_value)
    if textvaluelength <= 1:
        return 1
    return -1


def num_there(s):
    ''' Checking if element contains digit '''
    return any(i.isdigit() for i in s)


def get_title(link):
    """Getting pagetitle from pagelink"""
    # link = link.split("/")[-1]
    # if link.isalpha() == False:
    #     link = "home"
    # return link
    url = link

    # making requests instance
    reqs = requests.get(url)  # load the overall web page
    # using the BeautifulSoup module
    soup = BeautifulSoup(reqs.text, 'html.parser')

    # getting the title text
    try:
        title = soup.find('title').get_text()

    except:
        title = ""
    if len(title) > 1:
        return None
    else:
        data1 = url.split('/')
        print(data1)
        print('hi')
        data = [ele for ele in data1 if ele.strip()]
        print(data)
        print('hi1')
        if ((data[-1].find('#') == 0 and data[-2].find('www') != -1) or (data[-1].find('www') != -1)):
            print('hi4')
            return 'home'
        elif (data[-1].find('#') == 0 and data[-2].find('www') == -1):
            print('hi5')
            return data[-2]
        elif (data[-1].find('?') == 0 and data[-2].find('www') == -1):
            print('hi6')
            return data[-2]
        elif (data[-1].find('=') == 0 and data[-2].find('www') == -1):
            print('hi7')
            return data[-2]
        elif (num_there(data[-1]) and num_there(data[-2]) and num_there(data[-3]) and data[-4].find('www') == -1):
            print('hi8')
            return data[-4]
        elif (num_there(data[-1]) and num_there(data[-2])):
            print('hi9')
            return data[-3]
        elif (num_there(data[-1]) and data[-2].find('www') == -1):
            print('hi10')
            if 'https' in data[-2]:
                print('hi11')
                return 'home'
            return data[-2]
        elif (num_there(data[-1]) and data[-2].find('www') == -1):
            print('hi12')
            return data[-2]
        else:
            print('hi13')
            return data[-1]


def rule_2_4_2_fix(pagesource, data):
    output_json = data
    try:
        bs = BeautifulSoup(pagesource, "html.parser")
        tag = bs.select_one(data["selector"])
        print("tag", type(tag), "end")
        node = str(tag)
        print("node", node)
        output_json["editedContext"] = ""
        output_json["action"] = "notify"
        if output_json["code"] == "WCAG2AAA.Principle2.Guideline2_4.2_4_2.H25.1.EmptyTitle":
            # Checking when text in title is not present
            if checkingtextintitletag(node) == 1:
                if len(output_json["linkDetails"]) > 0:
                    page_link = output_json["linkDetails"]["page_link"]
                    link = get_title(page_link)  # getting page title
                    print("printing line 116, %s" % link)
                    if link != None and ('.aspx' in link or '.com' in link or '.pdf' in link or '.gif' in link or '.png' in link or 'jpeg' in link or 'jpeg' in link or '.ashx' in link or 'svg'):
                        link = link.split('.')[0]
                    if link != None:
                        print("sneha")
                        tag.append("{}".format(link))
                        output_json["editedContext"] = str(tag)
                        output_json['action'] = "fix"
                        output_json['editedContextInJson'] = modify_tag(
                            output_json)
                    else:
                        output_json['action'] = "noFixRequired"
                        output_json["editedContext"] = ""
                    return output_json
                else:
                    output_json['action'] = "unableToFix"
                    return output_json
            else:
                output_json['action'] = "noFixRequired"
                return output_json
        elif output_json['code'] == "WCAG2AAA.Principle2.Guideline2_4.2_4_2.H25.1.NoTitleEl":
            if len(output_json["linkDetails"]) > 0:
                page_link = output_json["linkDetails"]["page_link"]
                link = get_title(page_link)  # getting page title
                if link != None and ('.aspx' in link or '.com' in link or '.pdf' in link or '.gif' in link or '.png' in link or 'jpeg' in link or 'jpeg' in link or '.ashx' in link or 'svg'):
                    link = link.split('.')[0]
                if link != None:
                    output_json["editedContext"] = f"<head><title>{link}</title>"
                    output_json['action'] = "fix"
                    output_json['editedContextInJson'] = modify_tag(
                        output_json)
                else:
                    output_json['action'] = "noFixRequired"
                    output_json["editedContext"] = ""
                return output_json
            else:
                output_json['action'] = "unableToFix"
                return output_json

        elif output_json['code'] == "WCAG2AAA.Principle2.Guideline2_4.2_4_2.H25.1.NoHeadEl":
            if len(output_json["linkDetails"]) > 0:
                page_link = output_json["linkDetails"]["page_link"]
                link = get_title(page_link)  # getting page title
                if link != None and ('.aspx' in link or '.com' in link or '.pdf' in link or '.gif' in link or '.png' in link or 'jpeg' in link or 'jpeg' in link or '.ashx' in link or 'svg'):
                    link = link.split('.')[0]
                if link != None:
                    output_json["selector"] = "html > head"
                    output_json["editedContext"] = f"<head><title>{link}</title></head>"
                    output_json['action'] = "fix"
                    output_json['editedContextInJson'] = modify_tag(
                        output_json)
                else:
                    output_json['action'] = "noFixRequired"
                    output_json["editedContext"] = ""
                return output_json
            else:
                output_json['action'] = "unableToFix"
                return output_json

        else:
            output_json["editedContext"] = ""
            output_json["action"] = "notify"
            return output_json
    except Exception as e:
        output_json["editedContext"] = ""
        output_json["action"] = "unableToFix"
        return output_json


def starter(data):
    """rule 2.4.2 fix initiator which calls fix function"""
    result_json = {}
    pagesource = data["pageSource"]
    for i in data:
        if i in ["pageSource", "jobId", "linkDetails"]:
            continue
        result_json[str(i)] = rule_2_4_2_fix(pagesource, data[i])

    return result_json


def lambda_handler(event, context):
    """lambda function"""
    return starter(event)


with open('test_sample_1.json', 'r') as file:
    datas = json.load(file)
    final_data = lambda_handler(event=datas, context=None)
    final_json = json.dumps(final_data, indent=4)
    print(final_json)
