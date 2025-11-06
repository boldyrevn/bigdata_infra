import os
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

# Путь к исходному config файлу
CONFIG_FILE = "config"

# Папка для вывода XML
OUTPUT_DIR = "./hadoop-config"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Словарь для хранения свойств по файлам
files_map = {
    "core-site.xml": {},
    "hdfs-site.xml": {},
    "mapred-site.xml": {},
    "yarn-site.xml": {},
    "capacity-scheduler.xml": {},
}

# Читаем config
with open(CONFIG_FILE, "r") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            key, value = line.split("=", 1)
        except ValueError:
            continue
        # key вида CORE-SITE.XML_fs.default.name
        if "_" not in key:
            continue
        file_part, prop_name = key.split("_", 1)
        file_part = file_part.lower()
        prop_name = prop_name.strip()
        value = value.strip()
        if file_part == "core-site.xml":
            files_map["core-site.xml"][prop_name] = value
        elif file_part == "hdfs-site.xml":
            files_map["hdfs-site.xml"][prop_name] = value
        elif file_part == "mapred-site.xml":
            files_map["mapred-site.xml"][prop_name] = value
        elif file_part == "yarn-site.xml":
            files_map["yarn-site.xml"][prop_name] = value
        elif file_part == "capacity-scheduler.xml":
            files_map["capacity-scheduler.xml"][prop_name] = value


# Функция для создания XML
def write_xml(file_path, properties):
    configuration = Element("configuration")
    for name, value in properties.items():
        prop = SubElement(configuration, "property")
        name_el = SubElement(prop, "name")
        name_el.text = name
        value_el = SubElement(prop, "value")
        value_el.text = value
    # Красивый вывод
    xml_str = parseString(tostring(configuration)).toprettyxml(indent="  ")
    with open(file_path, "w") as f:
        f.write(xml_str)
    print(f"Created {file_path}")


# Генерируем файлы
for file_name, props in files_map.items():
    if props:
        write_xml(os.path.join(OUTPUT_DIR, file_name), props)
