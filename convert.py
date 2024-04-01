import argparse
import os
from music21 import converter, midi

def process_mxl_file(input_file, input_dir, output_dir):
    try:
        # Load the MusicXML file
        score = converter.parse(input_file)

        # Construct relative path from input_dir to maintain directory structure
        relative_path = os.path.relpath(os.path.dirname(input_file), input_dir)
        specific_output_dir = os.path.join(output_dir, relative_path)

        # Ensure the specific output directory exists
        os.makedirs(specific_output_dir, exist_ok=True)

        # Get the base name for the output file
        file_name = os.path.splitext(os.path.basename(input_file))[0]
        midi_path = os.path.join(specific_output_dir, f"{file_name}.mid")

        # Initialize a MIDI stream for combining parts
        combined_midi = midi.MidiFile()

        # Add each part to the combined MIDI stream
        for part in score.parts:
            mf = midi.translate.streamToMidiFile(part)
            for track in mf.tracks:
                combined_midi.tracks.append(track)

        # Write the combined MIDI stream to a file
        combined_midi.open(midi_path, 'wb')
        combined_midi.write()
        combined_midi.close()

    except Exception as e:
        print(f"Error processing {input_file}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Process MusicXML files and convert to a single combined MIDI file.")
    parser.add_argument("input_dir", type=str, help="Directory containing MusicXML files")
    parser.add_argument("output_dir", type=str, help="Directory to save combined MIDI files")

    args = parser.parse_args()

    if os.path.abspath(args.output_dir).startswith(os.path.abspath(args.input_dir)):
        print("The output directory cannot be inside the input directory.")
        return

    for root, dirs, files in os.walk(args.input_dir):
        # Skip the output directory if it is inside the input directory
        if args.output_dir.startswith(root):
            continue

        for file in files:
            if file.endswith(".mxl"):
                input_file = os.path.join(root, file)
                print("processing: " + input_file)
                process_mxl_file(input_file, args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()