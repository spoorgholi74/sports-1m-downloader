# Helper function for reading and writing text files
import glob
import json
import os


def saveText(my_list, name):
    with open('%s' % name, 'w') as f:
        for item in my_list:
            f.write("%s\n" % item)


def readText(name):
    with open('%s' % name, 'r') as f:
        x = f.read().splitlines()
    return x


def class2index(label_file):
    i = 0
    label_index = {}
    with open(label_file, "r") as f:
        for line in f:
            label_index[line.strip()] = i
            i += 1
    return label_index


def crosscheck_videos(video_path, ann_file, desired_class, idx_to_class):
    # Get existing videos
    existing_vids = glob.glob("%s/*.mp4" % video_path)
    for idx, vid in enumerate(existing_vids):
        basename = os.path.basename(vid).split(".mp4")[0]
        if len(basename) == 13:
            existing_vids[idx] = basename[2:]
        elif len(basename) == 11:
            existing_vids[idx] = basename
        else:
            raise RuntimeError("Unknown filename format: %s", vid)

    database = readText(ann_file)
    all_vids = {}
    for item in database:
        link = item.split(" ")[0]
        annotation = item.split(" ")[-1].split(",")
        all_vids[link] = annotation

    non_existing_videos = []
    for vid in all_vids:
        if vid in existing_vids:
            continue
        else:
            non_existing_videos.append(vid)

    # Here we have the nonexisting videos
    # We need to apply a method to get only classes that we need
    label_list = []
    wanted = []
    i = 0
    j = 0
    k = 0
    loops = 0
    # print(non_existing_videos)
    for idx, vid in enumerate(non_existing_videos):
        loops += 1
        # print(idx, vid)
        index = all_vids[vid]
        annotation = []
        for item in index:
            annotation.append(idx_to_class[int(item)])
        url = vid

        if len(annotation) > 0:
            for label in annotation:
                if label in label_list:
                    pass
                else:
                    label_list.append(label)
            # print(len(label_list))
            # check if desired labels are in the label_list of the video
            # 7440 videos
            for classes in desired_class:
                if classes in label_list:
                    print('url -->', url)
                    print("labeles --> ", label_list)
                    j += 1
                    wanted.append(vid)
                else:
                    k += 1
                    # non_existing_videos.remove(vid)

        else:  # 2570
            # non_existing_videos.remove(vid)
            i += 1

        label_list = []
    print("Number of unlabeled videos --> ", i)
    print("Number of desired videos --> ", j)
    print("Number of not contain classes --> ", k)
    # print("Number of vids in non-existanse loop --> ", loops)
    return wanted