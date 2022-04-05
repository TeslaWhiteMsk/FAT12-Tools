import binascii
def ms_date_from_byte(source):
    sourceint=int.from_bytes(source,byteorder="little")
    day=(sourceint&0x001F)
    month=(sourceint&0x01E0)>>5
    year=((sourceint&0xFE00)>>9)+1980
    result=str(day)+"-"+str(month)+"-"+str(year)
    return result

def ms_time_from_byte(source):
    sourceint=int.from_bytes(source,byteorder="little")
    second=(sourceint&0x001F)*2
    minute=(sourceint&0x07E0)>>5
    hour=(sourceint&0xF800)>>11
    result=str(hour)+":"+str(minute)+":"+str(second)
    return result

def ret_fat_nums(image):
    image.seek(22)
    result=int.from_bytes(image.read(2),byteorder='little')
    return result

def ret_fat_tables(image):
    image.seek(16)
    result=int.from_bytes(image.read(1),byteorder='little')
    return result

def ret_rsv_sec(image):
    image.seek(14)
    result=int.from_bytes(image.read(2),byteorder='little')
    return result

def ret_root_dir_ent(image):
    image.seek(17)
    result=int.from_bytes(image.read(2),byteorder='little')
    return result

def ret_root_dir_start(image):
    bytes_per_sector=ret_bytes_per_sector(image)
    fat_nums=ret_fat_nums(image)
    fat_tables=ret_fat_tables(image)
    reserved_sectors=ret_rsv_sec(image)
    root_dir_ent=ret_root_dir_ent(image)
    root_dir_sec=((root_dir_ent*32)//bytes_per_sector)
    root_dir_start=(reserved_sectors+(fat_tables*fat_nums))*bytes_per_sector
    return root_dir_start

def ret_root_dir_end (image):
    bytes_per_sector=ret_bytes_per_sector(image)
    fat_nums=ret_fat_nums(image)
    fat_tables=ret_fat_tables(image)
    reserved_sectors=ret_rsv_sec(image)
    root_dir_ent=ret_root_dir_ent(image)
    root_dir_sec=((root_dir_ent*32)//bytes_per_sector)
    root_dir_end=(reserved_sectors+(fat_tables*fat_nums)+root_dir_sec)*bytes_per_sector
    return root_dir_end

def ret_normalized_filename(image):
    filename= image.read(8)
    extension=image.read(3)
    if int.from_bytes(filename,byteorder='little')==0:
        return ""
    filename=filename.decode('ascii')
    extension=extension.decode('ascii')
    result=filename.replace(" ","")+"."+extension.replace(" ","")
    return result
def print_files(img_name):
    image=open(img_name,"rb")
    print("\nFILE NAME\t|R   |H   |S   |V   |D   |A\t|CREATION TIME\t|CREATION DATE\t|LAST ACC TIME\t|LAST WRT TIME\t|LAST WRT DATE")
    print("____________________________________________________________________________________________________________________________")
    root_dir_start=ret_root_dir_start(image)
    root_dir_end=ret_root_dir_end(image)
    for i in range(root_dir_start,root_dir_end,32):
        image.seek(i)
        filename=ret_normalized_filename(image)
        if filename=="":
            break
        atributes=int.from_bytes(image.read(1),byteorder="little")
        read_only=atributes&0x01
        hidden=(atributes&0x02)>>1
        system=(atributes&0x04)>>2
        volume_label_byte=(atributes&0x08)>>3
        subdirectory=(atributes&0x10)>>4
        archive=(atributes&0x20)>>5
        image.seek(i+14)
        creation_time=ms_time_from_byte(image.read(2))
        creation_date=ms_date_from_byte(image.read(2))
        last_access_date=ms_date_from_byte(image.read(2))
        image.seek(i+22)
        last_write_time=ms_time_from_byte(image.read(2))
        last_write_date=ms_date_from_byte(image.read(2))
        first_logical_cluster= image.read(2)
        filesize=image.read(4)
        print(filename,"\t|",read_only," |",hidden," |",system," |",volume_label_byte," |",subdirectory," |",archive,"\t|",creation_time,"\t|",creation_date,"\t|",last_access_date,"\t|",last_write_time,"\t|",last_write_date)
    image.close()

def bytes_to_mbytes(source):
    result=""
    if (source//1024) == 0:
        result+=str(source)+" B"
        return result
    kbytes=source//1024
    if (kbytes//1024) == 0:
        result+=str(kbytes)+" KB"
        return result
    mbytes=kbytes/1024
    result=str(round(mbytes,3))+" MB"
    return result

def short_print_files(img_name):
    image=open(img_name,"rb")
    print("\nFILE NAME\t|LAST WRT TIME\t|LAST WRT DATE\t|FILE SIZE")
    print("________________________________________________________")
    root_dir_start=ret_root_dir_start(image)
    root_dir_end=ret_root_dir_end(image)
    for i in range(root_dir_start,root_dir_end,32):
        image.seek(i)
        filename=ret_normalized_filename(image)
        if filename=="":
            break
        extension=image.read(3)
        image.seek(i+22)
        last_write_time=ms_time_from_byte(image.read(2))
        last_write_date=ms_date_from_byte(image.read(2))
        image.seek(i+28)
        filesize=bytes_to_mbytes(int.from_bytes(image.read(4),byteorder="little"))
        print(filename,"\t|",last_write_time,"\t|",last_write_date,"\t|",filesize)
    image.close()

def ret_bytes_per_sector(image):
    image.seek(11)
    bytes_per_sector=int.from_bytes(image.read(2),byteorder="little")
    return bytes_per_sector

def print_info(img_name):
    image=open(img_name,"rb")
    image.seek(3)
    oem_name=image.read(8)
    print("OEM Name:\t\t", oem_name.decode('ascii'))
    bytes_per_sector=ret_bytes_per_sector(image)
    print("Bytes per sector:\t",bytes_per_sector)
    sectors_per_cluster=int.from_bytes(image.read(1),byteorder='little')
    print("Sectors per cluster:\t",sectors_per_cluster)
    reserved_sectors=ret_rsv_sec(image)
    print("Reserved sectors:\t",reserved_sectors)
    fatcopies=ret_fat_tables(image)
    print("FAT copies:\t\t",fatcopies)
    root_directory_entries=ret_root_dir_ent(image)
    print("Root Directory Entries :", root_directory_entries)
    number_of_sectors_in_fs=int.from_bytes(image.read(2),byteorder='little')
    if number_of_sectors_in_fs==0:
        image.seek(32)
        number_of_sectors_in_fs=int.from_bytes(image.read(4),byteorder='little')
    print("Total number of sectors in the filesystem:\t",number_of_sectors_in_fs)
    image.seek(21)
    media_descriptor=image.read(1)
    media_desc_dict={
        b'\xe5':"200mm (250.25K)    1 side, 26 sectors, 77 tracks (DRDOS only)",
        b'\xf0':"3.5 (1.44 MB) 2 sides, 18 sectors or \n \t \t 3.5 (2.88 MB)  2 sides, 36 sectors or \n \t \t 5.25 (1.2 MB)  2 sides, 15 sectors",
        b'\xf8':"fixed disk",
        b'\xf9':"3.5  (720K)    2 sides,  9 sectors, 80 tracks or \n \t \t 5.25 (1.2 MB)  2 sides, 15 sectors, 80 tracks",
        b'\xfa':"5.25 (320K)    1 side,   8 sectors, 80 tracks",
        b'\xfb':"3.5  (640K)    2 sides,  8 sectors, 80 tracks",
        b'\xfc':"5.25 (180K)    1 side,   9 sectors, 40 tracks",
        b'\xfd':"5.25 (360K)    2 sides,  9 sectors, 40 tracks",
        b'\xfe':"5.25 (160K)    1 side,   8 sectors, 40 tracks (DOS) or \n \t \t 3.5  (1.2 MB) 2 side, 8 sectors (NEC PC)",
        b'\xff':"5.25 (320K)    2 sides,  8 sectors, 40 tracks"
        }
    print("Media type:\t",media_desc_dict[media_descriptor])
    sectors_per_fat=ret_fat_nums(image)
    print("Number of sectors per FAT:\t",sectors_per_fat)
    print("Sectors per track:\t", int.from_bytes(image.read(2),byteorder='little'))
    print("Number of heads:\t", int.from_bytes(image.read(2),byteorder='little'))
    print("Hidden sectors:\t",int.from_bytes(image.read(2),byteorder='little'))
    image.seek(39)
    volume_id=image.read(4)
    print("Volume ID:\t",binascii.b2a_hex(volume_id))
    volume_label=image.read(11)
    print("Volume label:\t",volume_label.decode('ascii'))
    #fstype=image.read(8)
    #print("Filesystem Type:",fstype.decode('ascii'))
    image.close()
