# coding: UTF-8

import struct
import binascii
import re

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
        return 0
        
    def print_font(self, font_pos):
        data = self.Font[font_pos]
        data = struct.unpack('BBBBBBBB',data)
        for var in data:
            #print '{0:0>8b}'.format(var)
            for i in range(8):
                if( 0 == (var & (0x80>>i))):
                    print " ",
                else:
                    print "*",
                    
            print ""

    def out_file(self, code_list):

        count = 1
        ucs = -1

        print "len 0x{0:X}".format(len(code_list))

        f = open("UCS2.FNT",'wb')
        for sjis in code_list :
            ucs = ucs + 1
            
            if( sjis == 0 ): continue
            font_pos = self.search_font(sjis)
            #if( font_pos == 0 ): continue

            if(ucs==0x8c37):
                print "sjis = 0x{0:X} count=0x{1:X}".format(sjis, count)
                self.print_font(font_pos)
                print self.Font[font_pos]

            count = count + 1
            
            f.write( self.Font[font_pos] )
            
        f.close()

class SJIStoUnicode:
    def open(self):
        self.List = [0] * 0xffff
        
        f = open("SHIFTJIS.TXT",'r')        

        line = f.readline()
        while line:
            line = line.rstrip("\n")
            if( line[0] != '#' ):
                data = line.split('\t')
                (sjis, ucs) = int(data[0],16), int(data[1],16)
                #print (sjis, ucs), data[1]
                self.List[ucs] = sjis
                
            line = f.readline()

    def out_table(self):

        (start, end) = (0,0)
        self.block = []
        flg = 0
        ucs = 0
        for sjis in self.List :
            if( sjis == 0 ):
                if( flg == 1 ):
                    flg = 0
                    end = ucs - 1
                    self.block.append((start,end))
                    #print "start - end", sjis, (start,end)
            else:
                if( flg == 0 ):
                    flg = 1
                    start = ucs
                    #print "start - end", sjis, (start,end)
                    
            ucs = ucs + 1

        print len(self.block)


    def out_file(self):
        f = open("UCSCODE.TBL",'wb')

        f.write(struct.pack('H', len(self.block))) # Tnum

        cnt = 0
        for (start,end) in self.block :
            f.write(struct.pack('HH', start, end)) # Block(Start, End)
            if( cnt < 1000): print "[{0:d}] {1:X}, {2:X}".format(cnt, start, end)

            if( cnt == 640 ): print "---->", start
            cnt = cnt + 1

        f.close()
    
#=================================

def TestFontx():
    f = Fontx()
    f.open()
    #a.out_string()
    for code in range( 0xffff ):
        pos = f.search_font(code)
        if(pos != 0 ): 
            print "==", code, "======"
            f.print_font(pos)


sj = SJIStoUnicode()
sj.open()
sj.out_table()
sj.out_file()

f = Fontx()
f.open()
f.out_file(sj.List)



