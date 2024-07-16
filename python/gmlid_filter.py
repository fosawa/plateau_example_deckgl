import xml.etree.ElementTree as ET

def get_namespaces(file):
    events = "start", "start-ns"
    namespaces = {}
    for event, elem in ET.iterparse(file, events):
        if event == "start-ns":
            namespaces[elem[0]] = elem[1]
    return namespaces

def filter_citygml_buildings(input_file, output_file, target_gml_id):
    # 名前空間の取得
    namespaces = get_namespaces(input_file)
    
    # XMLパーサの設定
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(input_file, parser=parser)
    root = tree.getroot()

    # cityObjectMember要素を取得
    city_object_members = root.findall('.//core:cityObjectMember', namespaces)

    # 指定したgml:idを持つBuilding要素を探す
    for city_object_member in city_object_members:
        building = city_object_member.find('.//bldg:Building', namespaces)
        if building is not None:
            gml_id = building.attrib.get('{http://www.opengis.net/gml}id')
            if gml_id != target_gml_id:
                root.remove(city_object_member)

    # 新しいツリーを出力ファイルに保存
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

# 使用例
input_file = '../citygml/53394525_bldg_6697_2_op.gml'
target_gml_ids = [
    'bldg_ffc04e24-60a0-48ce-8b20-93a51c160bb3',
    'bldg_68155acb-5edf-4ac3-b21c-a27306cfa8f5',
    'bldg_841d1294-22c9-4395-99c3-c805a9a901e9',
    'bldg_6f8b966e-b948-4efc-a7ef-02890bea3457',
    'bldg_efc1ebe0-ba1b-42de-87b8-deadb5b20a22',
    'bldg_2ad3209c-3b58-4e8c-933e-b54c5191aa33',
    'bldg_cc2488b7-1e1f-47fb-bc9a-9880c2e9f4a2',
    'bldg_594c17e3-cedb-4d35-abaf-8f79004e6c9f'
]

for target_gml_id in target_gml_ids:
    output_file = target_gml_id + '.gml'
    filter_citygml_buildings(input_file, output_file, target_gml_id)

