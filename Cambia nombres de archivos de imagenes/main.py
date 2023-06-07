from PIL import Image
import pytesseract
import os


pytesseract.pytesseract.tesseract_cmd = <RUTA DE INSTALACION>

pathScans = <RUTA DE SCANS>
suppliers = ["TERNIUM", "FERROSIDER"]
clients = ["GUIDI", "MI-PA-MET", "C.G.R.", "ROTOPLAS", "MIPAMET"]

ext = ".jpg"
numFile = 1

contentDir = os.listdir(pathScans)

print(contentDir)


for file in contentDir:

    fileName, extension = file.split(".jp")
    text = pytesseract.image_to_string(Image.open(pathScans + "/" + fileName + ".jp" + extension))

    print(text)
    print("*"*20)

    if file[:5] != "remito":

        print(file)
        print("Change to:")
        #print(text)

        proveedor = ""
        cliente = ""
        numDoc = ""
        page = ""

        for supplier in suppliers:
            if supplier in text:
                proveedor = supplier.title()
                break

        for client in clients:

            if client in text:
                cliente = client.title()
                break

        if proveedor == "Ferrosider":
            numDoc = text[text.index("Remito")+7:text.index("Remito")+20].replace("-", " ").replace("\n","")
            page = ""
        else:
            if "Hoja " in text:
                page = text[text.index("Hoja")+4:text.index("Hoja")+8].replace("/","-").replace("\n","")

        #print("*" * 20)
        print("Remito " + proveedor + " " + cliente + " " + numDoc + " " + page + " " + str(numFile) + ext)
        print("-"*40)
        os.rename(pathScans + "/" + file,pathScans + "/" + "Remito " + proveedor + " " + cliente + " " + numDoc + " " + page + " " + str(numFile) + ext)
        numFile += 1

#LOGS
#En los remitos de ferrosider no reconoce el cliente
#Nose como poner los numeros de REM
#Nose como poner los numeros de pagina







