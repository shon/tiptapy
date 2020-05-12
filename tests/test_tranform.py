import os
import pytest
import tiptapy
import json
from tiptapy import extras


tags_to_test = (
    "simple",
    "blockquote",
    "bulletlist",
    "mark_tags",
    "ordered_list",
    "image",
    "featuredimage",
    "horizontal_rule",
    "embed"
)


def build_test_data():
    """
    Scan data directories and return test data
    """
    store = {'json': {}, 'html': {}}
    for data_type in store:
        dir_path = os.path.abspath(f'tests/data/{data_type}/')
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            with open(file_path) as f:
                data = f.read()
                store[data_type][file.split(f'.{data_type}')[0]] = data
    return store['json'], store['html']


json_data, html_data = build_test_data()


def build_failing_caption_data(mediatag):
    """
    Manipulate mediatags input json data to return a dict with
    empty caption and no caption key.
    """
    transfomed_data = {}
    input_data = json.loads(json_data[mediatag])
    del input_data['attrs']['caption']
    transfomed_data['no_caption_key'] = input_data
    input_data['attrs']['caption'] = ''
    transfomed_data['empty_caption'] = input_data
    return transfomed_data


@pytest.mark.parametrize("tag", tags_to_test)
def test_html_tag(tag):
    """
    Test expected json input with the expected html.
    """
    tag_data = json_data[tag]
    expected_html = html_data[tag]
    assert tiptapy.to_html(tag_data) == expected_html


@pytest.mark.parametrize("mediatag",
                         ["image", "featuredimage", "embed"]
                         )
def test_mediatag_caption(mediatag):
    """
    Test missing caption key in json input with the expected html.
    """
    transfomed_data = build_failing_caption_data(mediatag)
    for data in transfomed_data:
        tag_data = transfomed_data[data]
        expected_html = html_data[mediatag]
        assert tiptapy.to_html(tag_data) != expected_html
