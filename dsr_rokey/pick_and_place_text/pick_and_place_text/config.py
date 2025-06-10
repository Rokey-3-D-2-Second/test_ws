import os
from ament_index_python.packages import get_package_share_directory

PACKAGE_NAME = "pick_and_place_text"
PACKAGE_PATH = get_package_share_directory(PACKAGE_NAME)

YOLO_MODEL_FILENAME = "best0610.pt"
YOLO_CLASS_NAME_JSON = "class_name_tool.json"

YOLO_MODEL_PATH = os.path.join(PACKAGE_PATH, "resource", YOLO_MODEL_FILENAME)
YOLO_JSON_PATH = os.path.join(PACKAGE_PATH, "resource", YOLO_CLASS_NAME_JSON)