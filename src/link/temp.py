import os

def extract_ascii_from_binary_region(data):
    """
    Convert binary data to a readable ASCII string.
    Replaces non-printable characters with '.'.
    """
    return ''.join(
        chr(b) if 32 <= b < 127 else '.' for b in data
    ).strip()

def extract_pre_image_ascii(filepath, bytes_to_extract=1000, output_dir="readable_pre_image_text"):
    with open(filepath, "rb") as f:
        data = f.read()

    os.makedirs(output_dir, exist_ok=True)

    start_marker = b'\xff\xd8'
    offset = 0
    image_count = 0

    while offset < len(data):
        start = data.find(start_marker, offset)
        if start == -1:
            break

        extract_start = max(0, start - bytes_to_extract)
        region = data[extract_start:start]

        # Convert to readable ASCII (replace non-printables with '.')
        ascii_output = extract_ascii_from_binary_region(region)

        output_filename = os.path.join(output_dir, f"image_{image_count:03d}_ascii.txt")
        with open(output_filename, "w", encoding="utf-8") as out_file:
            out_file.write(ascii_output + "\n")

        print(f"[+] Saved readable text before image {image_count} to {output_filename}")
        image_count += 1

        end = data.find(b'\xff\xd9', start)
        if end == -1:
            break
        offset = end + 2

    print(f"[✓] Extracted readable ASCII text for {image_count} images.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python extract_pre_image_ascii.py yourfile.ldf")
    else:
        extract_pre_image_ascii(sys.argv[1])
