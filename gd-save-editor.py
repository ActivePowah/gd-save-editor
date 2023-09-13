import os
import base64
import struct
import zlib
import json
from colorama import Fore as color
import time

def initialize_config():
    default_config = {
        'save-path': os.path.join(os.getenv('LocalAppData'), 'GeometryDash').replace('\\', '/'),
        'save-file-names': ['CCGameManager.dat', 'CCLocalLevels.dat']
    }

    with open('config.json', 'w') as file:
        json.dump(default_config, file, indent=4)

def load_config():
    if not os.path.exists('config.json'):
        initialize_config()

    with open('config.json', 'r') as file:
        config_data = json.load(file)

    return config_data

def xor_bytes(data: bytes, value: int) -> bytes:
    return bytes(map(lambda x: x ^ value, data))

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def main():
    while True:
        clear()
        option = input(f'{color.LIGHTBLUE_EX}GD Save Editor by Xytriza\n\n{color.YELLOW}[1]{color.LIGHTGREEN_EX} Decompile GD Save Files     {color.YELLOW}[2]{color.LIGHTGREEN_EX} Compile GD Save Files & Replace Existing Files     {color.YELLOW}[3]{color.LIGHTGREEN_EX} Path Editor{color.RESET}\n\n')

        if option == '1':
            config_data = load_config()
            SAVE_FILE_PATH = config_data.get('save-path')
            SAVE_FILE_NAMES = config_data.get('save-file-names')
            CURRENT_PATH = os.getcwd()
            clear()

            for save_file in SAVE_FILE_NAMES:
                XML_NAME = save_file.replace('.dat', '.xml')
                INPUT_PATH = os.path.join(SAVE_FILE_PATH, save_file).replace('\\', '/')
                OUTPUT_PATH = os.path.join(CURRENT_PATH, save_file).replace('\\', '/')
                if not os.path.exists(os.path.join(SAVE_FILE_PATH, save_file)):
                    print(f'{color.RED}[X]{color.LIGHTRED_EX} Unable to find {XML_NAME} in {SAVE_FILE_PATH}{color.RESET}')
                    continue

                try:
                    with open(INPUT_PATH, 'rb') as f:
                        compiled_data = f.read()

                    decompiled_data = xor_bytes(compiled_data, 11)
                    decoded_data = base64.b64decode(decompiled_data, altchars=b'-_')
                    decompressed_data = zlib.decompress(decoded_data[10:], -zlib.MAX_WBITS)

                    with open(XML_NAME, 'wb') as f:
                        f.write(decompressed_data)

                    print(f'{color.GREEN}[!]{color.LIGHTGREEN_EX} Decompiled {XML_NAME} & saved to {OUTPUT_PATH} {color.RESET}')
                except Exception as error:
                    print(f'{color.RED}[X]{color.LIGHTRED_EX} {error}{color.RESET}')

            del SAVE_FILE_PATH
            del SAVE_FILE_NAMES
            del CURRENT_PATH
            del XML_NAME
            del INPUT_PATH
            del OUTPUT_PATH
            time.sleep(3)
        elif option == '2':
            config_data = load_config()
            SAVE_FILE_PATH = config_data.get('save-path')
            SAVE_FILE_NAMES = config_data.get('save-file-names')
            CURRENT_PATH = os.getcwd()
            clear()

            for save_file in SAVE_FILE_NAMES:
                XML_NAME = save_file.replace('.dat', '.xml')
                INPUT_PATH = os.path.join(CURRENT_PATH, save_file).replace('\\', '/')
                OUTPUT_PATH = os.path.join(SAVE_FILE_PATH, save_file).replace('\\', '/')
                if not os.path.exists(os.path.join(CURRENT_PATH, XML_NAME)):
                    print(f'{color.RED}[X]{color.LIGHTRED_EX} Unable to find {XML_NAME} in {CURRENT_PATH}{color.RESET}')
                    continue

                try:
                    with open(OUTPUT_PATH, 'rb') as f:
                        decompiled_data = f.read()

                    compressed_data = zlib.compress(decompiled_data)
                    data_crc32 = zlib.crc32(decompiled_data)
                    data_size = len(decompiled_data)

                    compressed_data = (b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x0b' + compressed_data[2:-4] + struct.pack('I I', data_crc32, data_size))
                    encoded_data = base64.b64encode(compressed_data, altchars=b'-_')
                    compiled_data = xor_bytes(encoded_data, 11)

                    with open(os.path.join(SAVE_FILE_PATH, save_file), 'wb') as f:
                        f.write(compiled_data)

                    print(f'{color.GREEN}[!]{color.LIGHTGREEN_EX} Compiled {save_file} & saved to {OUTPUT_PATH} {color.RESET}')
                except Exception as error:
                    print(f'{color.RED}[X]{color.LIGHTRED_EX} {error}{color.RESET}')

            del SAVE_FILE_PATH
            del SAVE_FILE_NAMES
            del CURRENT_PATH
            del XML_NAME
            del INPUT_PATH
            del OUTPUT_PATH
            time.sleep(3)
        elif option == '3':
            while True:
                clear()
                edit_option = input(f'{color.LIGHTBLUE_EX}Path Editor\n\n{color.YELLOW}[1]{color.LIGHTGREEN_EX} Edit Save Folder Path     {color.YELLOW}[2]{color.LIGHTGREEN_EX} Edit Save File Names     {color.YELLOW}[3]{color.LIGHTGREEN_EX} Exit Editor{color.RESET}\n\n')

                if edit_option == '1':
                    clear()
                    folder = input(f'{color.LIGHTBLUE_EX}Enter the save folder path\n\n{color.RESET}').replace('\\', '/')
                    if folder.replace(' ', '') == '':
                        continue
                    if not os.path.exists(folder):
                        clear()
                        print(f'{color.RED}[X]{color.LIGHTRED_EX} Folder Doesn\'t exist{color.RESET}')
                        time.sleep(3)
                        continue

                    try:
                        config_data = load_config()
                        config_data['save-path'] = folder
                        with open('config.json', 'w') as file:
                            json.dump(config_data, file, indent=4)

                        clear()
                        print(f'{color.GREEN}[!]{color.LIGHTGREEN_EX} Edited Save Path successfully {color.RESET}')
                        time.sleep(3)
                    except Exception as error:
                        print(f'{color.RED}[X]{color.LIGHTRED_EX} {error}{color.RESET}')
                elif edit_option == '2':
                    clear()
                    names = input(f'{color.LIGHTBLUE_EX}Enter the new save filenames, seperated by commas\n\n{color.RESET}')
                    if names.replace(' ', '') == '':
                        continue

                    try:
                        clear()
                        config_data = load_config()
                        new_values = [value.strip() for value in names.split(',')]
                        config_data['save-file-names'] = new_values
                        with open('config.json', 'w') as file:
                            json.dump(config_data, file, indent=4)

                        clear()
                        print(f'{color.GREEN}[!]{color.LIGHTGREEN_EX} Edited Save Names successfully {color.RESET}')
                        time.sleep(3)
                    except Exception as error:
                        print(f'{color.RED}[X]{color.LIGHTRED_EX} {error}{color.RESET}')
                elif edit_option == '3':
                    break
                else:
                    clear()
                    print(f'{color.RED}[!]{color.LIGHTRED_EX} Invalid Option{color.RESET}')
                    time.sleep(3)
        else:
            clear()
            print(f'{color.RED}[!]{color.LIGHTRED_EX} Invalid Option{color.RESET}')
            time.sleep(3)

if __name__ == '__main__':
    main()