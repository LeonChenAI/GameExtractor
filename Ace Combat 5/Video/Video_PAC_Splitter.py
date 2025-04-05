import sys
import os

def search_and_split_binary_file(file_path, hex_string, offset=-75):
    try:
        search_bytes = bytes.fromhex(hex_string)
        search_len = len(search_bytes)
        
        with open(file_path, 'rb') as file:
            file_content = file.read()
        
        segments = []
        current_position = 0

        while True:
            pos = file_content.find(search_bytes, current_position)
            if pos == -1:
                break
            
            start_pos = max(0, pos + offset)

            next_pos = file_content.find(search_bytes, pos + search_len)
            if next_pos == -1:
                # 如果没有下一个匹配项，当前段到文件末尾
                end_pos = len(file_content)
                actual_end_pos = max(start_pos, end_pos)
                segments.append(file_content[start_pos:actual_end_pos])
                break
            else:
                # 应用结尾偏移
                end_pos = next_pos + offset
                actual_end_pos = max(start_pos, end_pos)
                segments.append(file_content[start_pos:actual_end_pos])
            
            current_position = next_pos

        if not segments:
            print("警告: 未找到任何匹配的十六进制字符串作为段的开始。")
            return []

        return segments
    
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
    except ValueError as e:
        print(f"十六进制字符串格式错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

def save_segments_to_files(segments, base_name, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for i, segment in enumerate(segments):
        output_file_path = os.path.join(output_folder, f"{base_name}_{i + 1}.mpg")
        with open(output_file_path, 'wb') as output_file:
            output_file.write(segment)
        print(f"已保存段到文件: {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python Video_PAC_Splitter.py <文件名>")
    else:
        file_path = sys.argv[1]
        hex_string = "21000001B5148A00010000000001B5250505040A020980000001B800080040"
        
        # 提取不带扩展名的基本名称
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_folder = base_name  # 使用基本名称作为输出文件夹
        
        segments = search_and_split_binary_file(file_path, hex_string)
        if segments:
            save_segments_to_files(segments, base_name, output_folder)