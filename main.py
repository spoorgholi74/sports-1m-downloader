import os
from argparse import ArgumentParser
from helper import readText, crosscheck_videos, class2index

def main(video_path, ann_file, lable_numbers, output_filename, class_names):
    desired_class = readText(class_names)
    class_to_idx = class2index(lable_numbers)
    idx_to_class = {}
    for name, label in class_to_idx.items():
        idx_to_class[label] = name
    non_existing_videos = crosscheck_videos(video_path, ann_file, desired_class, idx_to_class)
    filename = os.path.join(video_path, "%s.mp4")
    cmd_base = "youtube-dl -f best -f mp4 "
    cmd_base += '"%s" '
    cmd_base += '-o "%s"' % filename
    with open(output_filename, "w") as fobj:
        for vid in non_existing_videos:
            cmd = cmd_base % (vid, vid)
            fobj.write("%s\n" % cmd)


if __name__ == '__main__':
    parser = ArgumentParser(description="Script to double check video content.")
    parser.add_argument("video_path", default="./videos/", help="Where to locate the videos?")
    parser.add_argument("ann_file", help="Where is the annotation file?")
    parser.add_argument("lable_numbers", help="Labels to number txt file")
    parser.add_argument("output_filename", help="Output script location.")
    parser.add_argument("--class_names", default="class_names.txt", type=str, help="Text file of desired labels")
    args = vars(parser.parse_args())
    main(**args)