import xml.etree.ElementTree as ET

def borrar_datos_xml(archivo_xml):
    # Parsear el archivo XML
    tree = ET.parse(archivo_xml)
    root = tree.getroot()

    # Borrar todos los elementos hijos del elemento raíz
    for child in root:
        root.remove(child)

    # Guardar los cambios en el archivo XML
    tree.write(archivo_xml)

# Llamar a la función para borrar los datos del archivo XML
borrar_datos_xml('modeloFisherFace.xml')
