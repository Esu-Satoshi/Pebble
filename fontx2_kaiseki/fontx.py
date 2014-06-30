import struct
import binascii

class Fontx :
    
    def open(self):
        f = open("MISAKI.FNT",'rb')
        self.Identifier = f.read(6)
        self.FontName = f.read(8)
 
        (self.XSize, self.YSize, self.CodeType, self.Tnum) = struct.unpack('BBBB',f.read(4))

        self.Block = []
        for var in range(self.Tnum):
            (Start,End) = struct.unpack('HH',f.read(4))
            self.Block.append((Start,End))

        font_size = (self.XSize + 7) / 8
        self.font_size = font_size * self.YSize
        print self.font_size


        # 全フォントバッファの取り出し
        self.Font = []
        while 1:
            font = f.read(self.font_size)
            if( font == "" ): break
            
            self.Font.append(font)
            #print binascii.hexlify(font)

    def out_string(self):
        print self.Identifier, self.FontName
        print (self.XSize, self.YSize, self.CodeType, self.Tnum)
        for var in self.Block :
            print var

    def search_font(self, sj_code):
        # Shift_jis Code からビットマップデータ位置を検索

        cnt = 0
        for (start, end) in self.Block :
            if( start <= sj_code and end >= sj_code ):
                return (sj_code - start + cnt)
                break

            cnt = cnt + (end - start + 1)
        
    def print_font(self, font_pos):
        data = self.Font[font_pos]
        data = struct.unpack('BBBBBBBB',data)
        for var in data:
            print '{0:0>8b}'.format(var)
        
#=================================

a = Fontx()
a.open()
#a.out_string()
pos = a.search_font(0x8440)
print pos
a.print_font(pos)



