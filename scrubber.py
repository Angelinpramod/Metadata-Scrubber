from PIL import Image, ExifTags
import os

def analyze_metadata(exif_data, gps_data):
    warnings = []
    if gps_data:
        warnings.append("⚠️ GPS Location detected! Privacy risk!")
    for tag_id, value in exif_data.items():
        tag_name = ExifTags.TAGS.get(tag_id, tag_id)
        if tag_name in ["Make", "Model"]:
            warnings.append(f"⚠️ Device info found: {tag_name} = {value}")
        if tag_name == "Software":
            warnings.append(f"⚠️ Software info found: {value}")
        if tag_name == "DateTime":
            warnings.append(f"⚠️ Timestamp found: {value}")
        if tag_name in ["Author", "Artist"]:
            warnings.append(f"⚠️ Author info found: {value}")
    return warnings

def clean_metadata(input_path):
    img = Image.open(input_path)
    clean = Image.new(img.mode, img.size)
    clean.putdata(list(img.getdata()))
    name, ext = os.path.splitext(input_path)
    output_path = f"{name}_cleaned{ext}"
    clean.save(output_path)
    print(f"✅ Cleaned file saved as: {output_path}")
    return output_path

def main():
    image = Image.open('Kodak_CX7530.jpg')
    exif_data = image.getexif()
    gps_data = exif_data.get_ifd(34853)
    
    # Print raw metadata
    for tag_id, value in exif_data.items():
        tag_name = ExifTags.TAGS.get(tag_id, tag_id)
        print(f"{tag_name:25} : {value}")
    for tag_id, value in gps_data.items():
        gps = ExifTags.GPSTAGS.get(tag_id, tag_id)
        print(f"{gps:25} : {value}")
    
    # Threat analysis
    warnings = analyze_metadata(exif_data, gps_data)
    if warnings:
        print("\n🚨 THREAT ANALYSIS REPORT 🚨")
        print("-" * 40)
        for warning in warnings:
            print(warning)
    else:
        print("✅ No sensitive metadata found!")

if __name__ == "__main__":
    main()
