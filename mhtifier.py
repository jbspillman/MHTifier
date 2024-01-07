import email
import email.message
import os
import shutil


def main():
    print("##############################################################################")
    print("################### Extract MHT File Archive to Directory. ###################")
    print("##############################################################################")
    print("## Step Recording Tool in Windows no longer saves the images into the file. ##")
    print("## This is my workaround for that issue..                                   ##")
    print("##############################################################################")

    data_folder = os.path.join("data")
    os.makedirs(data_folder, exist_ok=True)

    src_folder = os.path.join("data", "inputs")
    os.makedirs(src_folder, exist_ok=True)

    dst_folder = os.path.join("data", "outputs")
    os.makedirs(dst_folder, exist_ok=True)

    for mht_file in os.listdir(src_folder):
        mht_file_path = os.path.join(src_folder, mht_file)
        print("MHT File:".ljust(30), mht_file)
        mht_base = os.path.basename(mht_file).split(".")[0]
        project_folder = os.path.join(dst_folder, mht_base)
        os.makedirs(project_folder, exist_ok=True)

        mht = open(mht_file_path, "rb")
        a = email.message_from_bytes(mht.read())
        parts = a.get_payload()
        if not type(parts) is list:
            parts = [a]

        for p in parts:
            ct = p.get_content_type()
            fp = p.get("content-location") or "index.html"
            print("Writing:".ljust(30), "%s to %s, %d bytes..." % (ct, fp, len(p.get_payload())))

            new_file_path = os.path.join(project_folder, fp)
            open(new_file_path, "wb").write(p.get_payload(decode=True))

            if fp == "main.htm":
                print("Rename me to: index.htm")
                new_index_path = os.path.join(project_folder, "index.htm")
                shutil.move(new_file_path, new_index_path)

            elif fp == "index.htm":
                print("Already Edited.")
            elif fp.endswith(".htm"):
                with open(new_file_path, "r", encoding="utf-8") as htm_file:
                    htm_code = htm_file.read()
                new_htm_code = htm_code.replace("main.htm", "index.htm")
                with open(new_file_path, "w", encoding="utf-8") as htm_file:
                    htm_file.write(new_htm_code)
            else:
                print('Unsupported file type.')

        print("##############################################################################")
        print("project_completed:".ljust(30), project_folder)
        print("##############################################################################")
        print()


if __name__ == "__main__":
    main()
