import yaml
import xml.etree.ElementTree as xml_tree
from xml.dom import minidom  # Import for pretty printing

with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)

rss_element = xml_tree.Element('rss', {
    'version': '2.0',
    'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
    'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'
})

channel_element = xml_tree.SubElement(rss_element, 'channel')

link_prefix = yaml_data['link'].rstrip('/')  # Remove trailing slash

xml_tree.SubElement(channel_element, 'title').text = yaml_data['title']
xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data['subtitle']
xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
xml_tree.SubElement(channel_element, 'description').text = yaml_data['description']
xml_tree.SubElement(channel_element, 'itunes:image', {'href': f"{link_prefix}/{yaml_data['image'].lstrip('/')}"})
xml_tree.SubElement(channel_element, 'language').text = yaml_data['language']
xml_tree.SubElement(channel_element, 'link').text = link_prefix

xml_tree.SubElement(channel_element, 'itunes:category', {'text': yaml_data['category']})

for item in yaml_data['item']:
    item_element = xml_tree.SubElement(channel_element, 'item')
    xml_tree.SubElement(item_element, 'title').text = item['title']
    xml_tree.SubElement(item_element, 'itunes:author').text = yaml_data['author']
    xml_tree.SubElement(item_element, 'description').text = item['description']
    xml_tree.SubElement(item_element, 'itunes:duration').text = item['duration']
    xml_tree.SubElement(item_element, 'pubDate').text = item['published']

    length_value = item['length'].replace(',', '')  # Remove commas from length

    xml_tree.SubElement(item_element, 'enclosure', {
        'url': f"{link_prefix}/{item['file'].lstrip('/')}",
        'type': 'audio/mpeg',
        'length': length_value
    })

# Pretty-print the XML
xml_str = xml_tree.tostring(rss_element, encoding='utf-8')
parsed_xml = minidom.parseString(xml_str)  # Format the XML
pretty_xml = parsed_xml.toprettyxml(indent="  ")  # Add indentation

# Write the formatted XML to file
with open('podcast.xml', 'w', encoding='utf-8') as f:
    f.write(pretty_xml)
