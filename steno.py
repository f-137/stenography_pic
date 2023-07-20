from PIL import Image
import os
import pandas as pd

def text_to_bits(text):
    bits = []
    encoded_text = text.encode("utf-8")
    for byte in encoded_text:
        # Convert each byte to 8-bit binary representation
        byte_bits = format(byte, '08b')
        bits.extend(byte_bits)
    return bits



def get_txt():
    
    current_file_path = os.path.realpath(__file__)
    current_folder_path =os.path.dirname(current_file_path)
    #print(current_file_path)
    file_path =f"{current_folder_path}\message.txt"
    file=open(file_path,"r")
    
    file_contents = file.read()
    file.close()
    return file_contents



def hide_text_in_image(image_path, text):
    # Open the image file
    image = Image.open(image_path)

    # Convert the image to RGB mode if it's not already
    image = image.convert("RGB")

    # Get the size of the image
    width, height = image.size

    # Convert the text to binary
    bits = text_to_bits(text)

    #add the message length to the end of the bits(4x8bit)
    binary = bin(len(bits))[2:]
    binary = binary.zfill(32)
    binary_array=[]
    for chr in binary:
        binary_array.extend(chr)
    bits = binary_array + bits
    
    print(f"the lenth of message in binary is {len(bits)}")
    print(f"The length of possible message length is {(width * height * 3)-32}")
    # Check if the text is too long to fit within the image
    if len(bits) > width * height * 3:
        print("Text is too long to fit within the image.")
        return

    # Access each pixel's information
    pixels = image.load()
    bit_index = 0
    #print(pixels[0,0])
    #print(pixels[0,16])
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            # Modify the least significant bit of each RGB value
            
            if bit_index < len(bits):
                
                r = (r & 0xFE) | int(bits[bit_index])
                bit_index += 1
            if bit_index < len(bits):
                
                g = (g & 0xFE) | int(bits[bit_index])
                bit_index += 1
            if bit_index < len(bits):
                
                b = (b & 0xFE) | int(bits[bit_index])
                bit_index += 1
            
                
            # Update the pixel values
            #print(pixels[x,y])
            pixels[x, y] = (r, g, b)
                 
            #print(pixels[x,y])
            
    # lol

    # Save the modified image
    current_file_path = os.path.realpath(__file__)
    current_folder_path =os.path.dirname(current_file_path)
    
    image.save(fr"{current_folder_path}\new_image.png")
    
    # Close the image file
    image.close()

def decode_text_from_image(new_image_path):
    new_image = Image.open(new_image_path)
    width, height = new_image.size
    pixels = new_image.load()
    bits = []
      
    
    for y in range(height):
        for x in range(width):
            
            r, g, b = pixels[x, y]
            bits.append(str(format(r,'08b')[-1]))
            bits.append(str(format(g,'08b')[-1]))
            bits.append(str(format(b,'08b')[-1]))
            """
            bits.append(str(r & 1))
            bits.append(str(g & 1))
            bits.append(str(b & 1))
            """

    # Retrieve the length of the hidden message
    message_length = int("".join(bits[:32]), 2)
    bits = bits[32:32 + message_length]

    decoded_text = ""
    bit_index =0
    while bit_index < len(bits):
        byte_array =bits[bit_index:bit_index+8]
        byte="".join(byte_array)
        #byte=int(byte)
        #print(type(byte))
        decoded_text=decoded_text+chr(int(byte,2))
        bit_index+=8
        

    return decoded_text



# Example usage
current_file_path = os.path.realpath(__file__)
current_folder_path =os.path.dirname(current_file_path)
file_path =f"{current_folder_path}\message.txt"
image_path = fr"{current_folder_path}\image.png"
#print(image_path)
#print(file_path)
text = get_txt()

hide_text_in_image(image_path, text)
new_file_path=fr"{current_folder_path}\new_image.png"
#new_file_path=fr"{current_folder_path}\asd.png"
#print(new_file_path)
decoded_text = decode_text_from_image(new_file_path)

print("Decoded Text:", decoded_text)

