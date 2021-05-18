import json
import os
import pathlib
import shutil
import subprocess
from os import listdir

from bs4 import BeautifulSoup, NavigableString

from config import Config

config = Config()


def decompile_apk(path, name):
    apk_path = pathlib.PurePath(path, name)
    command = ['apktool', 'd', str(apk_path), '-o', config.decompile_temp]
    cp = subprocess.run(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(cp.stdout)
    print(cp.stderr)


def clean_value(input):
    if '/' in input:
        return input.split('/')[1]
    else:
        return input


def analyse_xml_images(element):
    children = element.children
    if not children:
        return None
    image_map = {}
    for node in children:
        if isinstance(node, NavigableString):
            continue
        analyse_node(image_map, node)
        child_images = analyse_xml_images(node)
        if child_images:
            image_map.update(child_images)
    return image_map


def analyse_node(image_map, node):
    if 'android:id' in node.attrs.keys() and 'android:src' in node.attrs.keys():
        image_name = clean_value(node.attrs['android:src'])
        node_key = clean_value(node.attrs['android:id'])
        if image_name != '@null':
            image_map[node_key] = image_name


def retrieve_all_layout_image_names():
    path = config.decompile_temp + '/res/layout'
    result = {}
    for f in listdir(path):
        with open(path + '/' + f, 'r') as file:
            data = file.read()
        xml_layout = BeautifulSoup(data, "xml")
        image_names = analyse_xml_images(xml_layout)
        if len(image_names):
            key = f.replace('.xml', '')
            result[key] = image_names
    return result


def clean_temp_dir():
    shutil.rmtree(config.decompile_temp)


def save_image_names(app_name, image_names):
    short_app_name = app_name.split('-')[0]
    path = config.image_repo + '/' + short_app_name + '.json'
    with open(path, 'w+') as outfile:
        json.dump(image_names, outfile, indent=4)


def extract_from_app(path, app_name):
    clean_temp_dir()
    decompile_apk(path, app_name)
    image_names = retrieve_all_layout_image_names()
    save_image_names(app_name, image_names)


def extract_all_apps():
    for path, subdirs, files in os.walk(config.apks_dir):
        for name in files:
            extract_from_app(path, name)


if __name__ == '__main__':
    extract_all_apps()
    # with open('activity_main.xml', 'r') as f:
    #     data = f.read()
    # xml_layout = BeautifulSoup(data, "xml")
    # xml_layout = parse('activity_main.xml')
    # image_map = analyse_xml_images(xml_layout, 'activity_main')
    # print(image_map)
