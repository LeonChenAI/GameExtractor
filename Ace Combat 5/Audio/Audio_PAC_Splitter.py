import os, struct, sys, argparse

def split_file(fp):
    BLOCKSIZE = 0x800
    marker = b"NPSF"  # 直接定义为字节串
    current = b''  # 使用字节串来累积数据

    try:
        for block in iter(lambda: fp.read(BLOCKSIZE), b''):
            # 检查块是否以标记开头（只比较前4个字节）
            if block.startswith(marker):
                if current:
                    yield current
                current = block
            else:
                current += block
        # 返回最后一个累积的块（如果有）
        if current:
            yield current
    except IOError as e:
        # 处理文件读取错误
        print(f"Error reading file: {e}")

def dump_content(filename, content):
    with open(filename, "wb") as f:
        f.write(content)

def get_filename_from_npsf(npsf):
    filename = npsf[0x34:0x34+16].decode('utf-8', 'replace')
    filename = filename[0:filename.find("\x00")]
    return filename

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("radio_file", help="radio file to extract",
                    type=argparse.FileType('rb'))
    parser.add_argument("-o", "--dest_dir", help="output destination directory",
                    type=str, default="rip")
    opt = parser.parse_args()
    result = split_file(opt.radio_file)

    if not os.path.exists(opt.dest_dir):
        os.makedirs(opt.dest_dir)

    print ("Dumping from radio file: %s" % (opt.radio_file.name))

    for r in result:
        filename = get_filename_from_npsf(r)
        fullname = os.path.join(opt.dest_dir, os.path.splitext(filename)[0] + ".npsf")
        print ("dumping %s as %s, %d bytes" % (filename, fullname, len(r)))
        dump_content(fullname, r)

if __name__ == "__main__":
    main()

# vim: set sw=4 tabstop=4 expandtab:
