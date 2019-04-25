#!/usr/bin/env python
# coding: UTF-8

import os 
import time
import sys
import subprocess
import tempfile 
import webbrowser
import colorama
import numpy as np
from colorama import Fore, Back, Style
from PIL import Image 
from pdf2image import convert_from_path

def export(file_pdf):
    #filename = os.path.join(sys.path[0] ,'tests', 'nt.pdf')

    filename = file_pdf
    name_jpg = os.path.splitext(os.path.basename(file_pdf))[0]

    #save_dir = os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), 'jpg')
    save_dir = str(filename).rsplit('\\', 1)[0]
    list_jpg = []

    time.sleep(2)
    print(Fore.GREEN + "Iniciando exportacao PDF > JPEG..." + Style.RESET_ALL) 

    with tempfile.TemporaryDirectory():
        images_from_path = convert_from_path(filename, 300)     

        # percorre pdf para exportar as paginas
        i = 0
        for page in images_from_path:
            i += 1    
            
            print(Fore.RED + "Exportando pagina page-" + str(i) + ".jpg ..." + Style.RESET_ALL) 
            
            # salvando paginas exportadas
            save_filename  =  os.path.join(save_dir, 'page-' + str(i) + '.jpg')   
            page.save(os.path.join(save_dir, save_filename), 'JPEG')
            
            # armazena o caminho dos jpgs no list para poder usar na juncao logo abaixo
            list_jpg.append(save_filename)

            # redimensionando as imagens - nao usado a principio
            #if(resize):
            #    img_rsz = Image.open(save_filename)
            #    new_img_r = img_rsz.resize((1024, 720))
            #    new_img_r.save(save_filename, "JPEG")

    time.sleep(2)
    
    # pegando imagens
    images = list(map(Image.open, list_jpg))
    widths, heights = zip(*(i.size for i in images))
    
    # somando dimensoes
    total_height = sum(heights)
    max_width = max(widths)
    
    # nova imagem
    new_im = Image.new('RGB', (max_width, total_height))

    # concatenando jpgs - vertical
    y_offset = 0
    for image in images:
        new_im.paste(image, (0, y_offset))
        y_offset += image.size[1]

    # salva jpg tripa
    # new_im.save(os.path.join(save_dir, name_jpg+'.jpg'))
    new_im.save(os.path.join(save_dir, name_jpg+'.jpg')) 
    
    # deleta todas os jpgs exportados
    for jpg in list_jpg:
        os.remove(jpg)
    
    print(Fore.GREEN + "JPEG finalizado !" + Style.RESET_ALL) 
    #new_im.show()

# chamando prog com o caminho do pdf
if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Nenhum PDF foi informado")
        sys.exit(1)
    else:
        export(sys.argv[1])