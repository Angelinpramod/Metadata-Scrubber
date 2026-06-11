from PIL import Image, ExifTags
import os
import argparse

def analyze_metadata(exif_data, gps_data):
    warnings = []
    if gps_data:
        warnings.append("GPS Location detected! Privacy risk!")
    for tag_id, value in exif_data.items():
        tag_name = ExifTags.TAGS.get(tag_id, tag_id)
        if tag_name in ["Make", "Model"]:
            warnings.append(f"Device info found: {tag_name} = {value}")
        if tag_name == "Software":
            warnings.append(f"Software info found: {value}")
        if tag_name == "DateTime":
            warnings.append(f"Timestamp found: {value}")
        if tag_name in ["Author", "Artist"]:
            warnings.append(f"Author info found: {value}")
    return warnings

def clean_metadata(input_path):
    img = Image.open(input_path)
    clean = Image.new(img.mode, img.size)
    clean.putdata(list(img.getdata()))
    name, ext = os.path.splitext(input_path)
    output_path = f"{name}_cleaned{ext}"
    clean.save(output_path)
    print(f"Cleaned file saved as: {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(
        description="🔍 MetaScrubber — Metadata Detection & Removal Tool"
    )
    
    # Add arguments
    parser.add_argument("--input",   required=True, help="Path to input file")
    parser.add_argument("--analyze", action="store_true", help="Analyze metadata")
    parser.add_argument("--clean",   action="store_true", help="Clean metadata")
    parser.add_argument("--output",  help="Custom output path (optional)")
    
    args = parser.parse_args()
    
    # Step 1 - Open image using args
    image = Image.open(args.input)
    exif_data = image.getexif()
    gps_data = exif_data.get_ifd(34853)
    
    # Step 2 - If --analyze flag passed
    if args.analyze:
        print("\n EXTRACTING METADATA...")
        for tag_id, value in exif_data.items():
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
            print(f"{tag_name:25} : {value}")
        for tag_id, value in gps_data.items():
            gps = ExifTags.GPSTAGS.get(tag_id, tag_id)
            print(f"{gps:25} : {value}")
        
        warnings = analyze_metadata(exif_data, gps_data)
        if warnings:
            print("\nTHREAT ANALYSIS REPORT")
            print("-" * 40)
            for warning in warnings:
                print(warning)
        else:
            print("No sensitive metadata found!")
    
    # Step 3 - If --clean flag passed
    if args.clean:
        print("\n Starting sanitization...")
        cleaned_path = clean_metadata(args.input)
        
        # Verify
        print("\n🔍 Verifying...")
        cleaned_image = Image.open(cleaned_path)
        cleaned_exif = cleaned_image.getexif()
        if not cleaned_exif:
            print("VERIFICATION PASSED — Zero metadata found!")
        else:
            print(f"WARNING — {len(cleaned_exif)} fields still present!")
    
    # Step 4 - If neither flag passed
    if not args.analyze and not args.clean :
        print("Please specify --analyze or --clean")
        print("Example: python3 scrubber.py --input photo.jpg --analyze --clean")
if __name__ == "__main__":
    main()
