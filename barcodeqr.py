from machine import Pin,I2C,SPI,PWM,ADC
import framebuf
import time
import math

DC = 8
CS = 9
SCK = 10
MOSI = 11
RST = 12

BL = 25

Vbat_Pin = 29
width = 240
height = 240

class LCD_1inch28(framebuf.FrameBuffer): # Waveshare RP2040 1.28" IPS LCD Board Driver - Round Display
    def __init__(self):
        self.width = 240
        self.height = 240
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1,100_000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        
        self.fill(self.white)
        self.show()

        self.pwm = PWM(Pin(BL))
        self.pwm.freq(5000)
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)
    def set_bl_pwm(self,duty):
        self.pwm.duty_u16(duty)#max 65535
    def init_display(self):
        """Initialize display"""  
        self.rst(1)
        time.sleep(0.01)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)
        time.sleep(0.05)
        
        self.write_cmd(0xEF)
        self.write_cmd(0xEB)
        self.write_data(0x14) 
        
        self.write_cmd(0xFE) 
        self.write_cmd(0xEF) 

        self.write_cmd(0xEB)
        self.write_data(0x14) 

        self.write_cmd(0x84)
        self.write_data(0x40) 

        self.write_cmd(0x85)
        self.write_data(0xFF) 

        self.write_cmd(0x86)
        self.write_data(0xFF) 

        self.write_cmd(0x87)
        self.write_data(0xFF)

        self.write_cmd(0x88)
        self.write_data(0x0A)

        self.write_cmd(0x89)
        self.write_data(0x21) 

        self.write_cmd(0x8A)
        self.write_data(0x00) 

        self.write_cmd(0x8B)
        self.write_data(0x80) 

        self.write_cmd(0x8C)
        self.write_data(0x01) 

        self.write_cmd(0x8D)
        self.write_data(0x01) 

        self.write_cmd(0x8E)
        self.write_data(0xFF) 

        self.write_cmd(0x8F)
        self.write_data(0xFF) 


        self.write_cmd(0xB6)
        self.write_data(0x00)
        self.write_data(0x20)

        self.write_cmd(0x36)
        self.write_data(0x98)

        self.write_cmd(0x3A)
        self.write_data(0x05) 


        self.write_cmd(0x90)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08) 

        self.write_cmd(0xBD)
        self.write_data(0x06)
        
        self.write_cmd(0xBC)
        self.write_data(0x00)

        self.write_cmd(0xFF)
        self.write_data(0x60)
        self.write_data(0x01)
        self.write_data(0x04)

        self.write_cmd(0xC3)
        self.write_data(0x13)
        self.write_cmd(0xC4)
        self.write_data(0x13)

        self.write_cmd(0xC9)
        self.write_data(0x22)

        self.write_cmd(0xBE)
        self.write_data(0x11) 

        self.write_cmd(0xE1)
        self.write_data(0x10)
        self.write_data(0x0E)

        self.write_cmd(0xDF)
        self.write_data(0x21)
        self.write_data(0x0c)
        self.write_data(0x02)

        self.write_cmd(0xF0)   
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)

        self.write_cmd(0xF1)    
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37)  
        self.write_data(0x6F)


        self.write_cmd(0xF2)   
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)

        self.write_cmd(0xF3)   
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37) 
        self.write_data(0x6F)

        self.write_cmd(0xED)
        self.write_data(0x1B) 
        self.write_data(0x0B) 

        self.write_cmd(0xAE)
        self.write_data(0x77)
        
        self.write_cmd(0xCD)
        self.write_data(0x63)


        self.write_cmd(0x70)
        self.write_data(0x07)
        self.write_data(0x07)
        self.write_data(0x04)
        self.write_data(0x0E) 
        self.write_data(0x0F) 
        self.write_data(0x09)
        self.write_data(0x07)
        self.write_data(0x08)
        self.write_data(0x03)

        self.write_cmd(0xE8)
        self.write_data(0x34)

        self.write_cmd(0x62)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x71)
        self.write_data(0xED)
        self.write_data(0x70) 
        self.write_data(0x70)
        self.write_data(0x18)
        self.write_data(0x0F)
        self.write_data(0x71)
        self.write_data(0xEF)
        self.write_data(0x70) 
        self.write_data(0x70)

        self.write_cmd(0x63)
        self.write_data(0x18)
        self.write_data(0x11)
        self.write_data(0x71)
        self.write_data(0xF1)
        self.write_data(0x70) 
        self.write_data(0x70)
        self.write_data(0x18)
        self.write_data(0x13)
        self.write_data(0x71)
        self.write_data(0xF3)
        self.write_data(0x70) 
        self.write_data(0x70)

        self.write_cmd(0x64)
        self.write_data(0x28)
        self.write_data(0x29)
        self.write_data(0xF1)
        self.write_data(0x01)
        self.write_data(0xF1)
        self.write_data(0x00)
        self.write_data(0x07)

        self.write_cmd(0x66)
        self.write_data(0x3C)
        self.write_data(0x00)
        self.write_data(0xCD)
        self.write_data(0x67)
        self.write_data(0x45)
        self.write_data(0x45)
        self.write_data(0x10)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)

        self.write_cmd(0x67)
        self.write_data(0x00)
        self.write_data(0x3C)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x54)
        self.write_data(0x10)
        self.write_data(0x32)
        self.write_data(0x98)

        self.write_cmd(0x74)
        self.write_data(0x10)
        self.write_data(0x85)
        self.write_data(0x80)
        self.write_data(0x00) 
        self.write_data(0x00) 
        self.write_data(0x4E)
        self.write_data(0x00)
        
        self.write_cmd(0x98)
        self.write_data(0x3e)
        self.write_data(0x07)

        self.write_cmd(0x35)
        self.write_cmd(0x21)

        self.write_cmd(0x11)
        time.sleep(0.12)
        self.write_cmd(0x29)
        time.sleep(0.02)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xef)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)

import textencoder
import placement
import renderer

class DataMatrixEncoder:
    def __init__(self, text):
        enc = textencoder.TextEncoder()
        codewords = enc.encode(text)
        self.width = 0
        self.height = 0
        matrix_size = enc.mtx_size*enc.regions
        self.regions = enc.regions
        self.matrix = [[None] * matrix_size for _ in range(0, matrix_size)]
        placer = placement.DataMatrixPlacer()
        placer.place(codewords, self.matrix)

    def get_ascii(self):
        dmtx = renderer.DataMatrixRenderer(self.matrix, self.regions)
        return dmtx.get_ascii()


def show_datamatrix(text, lcd):
    encoder = DataMatrixEncoder(text)
    raw_matrix = encoder.matrix
    original_size = len(raw_matrix)
    
    print(f"Datamatrix: '{text}' ({len(text)} znaků) → {original_size}x{original_size}")
    
    # Kontrola podle délky textu
    if len(text) > 5:
        print("→ Používám PyStrich renderer")
        
        # PyStrich renderer pro dlouhé texty
        dmtx = renderer.DataMatrixRenderer(encoder.matrix, encoder.regions)
        final_matrix = dmtx.matrix
        size = len(final_matrix)
        
        # Převeď na boolean
        matrix = []
        for row in final_matrix:
            bool_row = [cell == 1 for cell in row]
            matrix.append(bool_row)
        
        scale = min(200 // size, 6)
        scale = max(scale, 2)
        
        print(f"PyStrich: {size}x{size}, scale={scale}")
        
    else:
        print("→ Používám vlastní finder patterns")
        
        # Vlastní finder patterns pro krátké texty
        new_size = original_size + 2
        matrix = [[False for _ in range(new_size)] for _ in range(new_size)]
        
        # Zkopíruj data
        for row in range(original_size):
            for col in range(original_size):
                cell = raw_matrix[row][col]
                is_black = (cell == 1)
                matrix[row + 1][col + 1] = is_black
        
        # Přidej finder patterns
        for row in range(new_size):
            matrix[row][0] = True  # Levý solid
            matrix[row][new_size-1] = (row % 2) == 1  # Pravý alternating
        for col in range(new_size):
            matrix[0][col] = (col % 2) == 0  # Horní alternating  
            matrix[new_size-1][col] = True  # Spodní solid
        
        scale = min(200 // new_size, 10)
        scale = max(scale, 6)
        
        print(f"Vlastní: {original_size}x{original_size} → {new_size}x{new_size}, scale={scale}")
    
    # Vykresli
    size = len(matrix)
    total_size = size * scale
    start_x = (240 - total_size) // 2
    start_y = (240 - total_size) // 2
    
    lcd.fill(0xFFFF)
    for row in range(size):
        for col in range(size):
            if matrix[row][col]:
                for dy in range(scale):
                    for dx in range(scale):
                        px, py = start_x + col * scale + dx, start_y + row * scale + dy
                        if 0 <= px < 240 and 0 <= py < 240:
                            lcd.pixel(px, py, 0x0000)
    lcd.show()

if __name__ == "__main__":
    lcd = LCD_1inch28()
    show_datamatrix("Hello world 123456", lcd)
