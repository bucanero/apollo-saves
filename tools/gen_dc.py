#!/usr/bin/env python3
# Dreamcast save converter for the Apollo online DB
# (c)2026 Damian Parrino
#
# Converts the dreamcast-saves repository (VMI/VMS pairs) into the
# Apollo database layout:
#   DC/games.txt               id=Game title
#   DC/<id>/saves.txt          xyz.zip=(VMU_FILENAME) description
#   DC/<id>/xyz.zip            xyz.vmi + xyz.VMS
#   DC/<id>/icon0.png          game icon
#   DC/README.md, DC/<id>/README.md   Jekyll pages
#
# Usage: gen_dc.py <dreamcast-saves path> <output path>

import os
import shutil
import sys
import zipfile

from PIL import Image

SAVE_TYPE = "DC"
ZIP_DATE = (1980, 1, 1, 0, 0, 0)


def read_list(path):
    entries = []
    with open(path, encoding="latin-1") as f:
        for line in f.read().splitlines():
            if "=" not in line:
                continue
            key, desc = line.split("=", 1)
            entries.append((key.strip(), desc.strip()))
    return entries


def find_file(files, name):
    return files.get(name.lower())


def vmu_filename(vmi_path):
    with open(vmi_path, "rb") as f:
        data = f.read()
    name = data[0x58:0x58 + 12].split(b"\0")[0].split(b" ")[0]
    return name.decode("latin-1")


def write_zip(zip_path, members):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for src in members:
            info = zipfile.ZipInfo(os.path.basename(src), ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(src, "rb") as f:
                z.writestr(info, f.read())


def write_icon(gif_path, png_path):
    with Image.open(gif_path) as img:
        img.seek(0)
        img.convert("RGBA").save(png_path, "PNG", optimize=True)


# Render the first icon frame from the VMS header (16-color ARGB4444 palette, 32x32 4bpp)
def write_vms_icon(vmi_path, vms_path, png_path):
    with open(vmi_path, "rb") as f:
        vmi = f.read()
    with open(vms_path, "rb") as f:
        vms = f.read()

    # game (mini-game) files have the header at 0x200
    hdr = 0x200 if int.from_bytes(vmi[0x64:0x66], "little") & 2 else 0
    if len(vms) < hdr + 0x80 + 512 or int.from_bytes(vms[hdr + 0x40:hdr + 0x42], "little") == 0:
        return False

    palette = []
    for i in range(16):
        c = int.from_bytes(vms[hdr + 0x60 + i * 2:hdr + 0x62 + i * 2], "little")
        palette.append(tuple(((c >> s) & 0xF) * 17 for s in (8, 4, 0, 12)))

    pixels = []
    for b in vms[hdr + 0x80:hdr + 0x80 + 512]:
        pixels += [palette[b >> 4], palette[b & 0xF]]

    img = Image.new("RGBA", (32, 32))
    img.putdata(pixels)
    img.save(png_path, "PNG", optimize=True)
    return True


def md_escape(text):
    return text.replace("|", "\\|")


def front_matter(title, permalink, parent=None, children=False):
    out = "---\nlayout: default\ntitle: \"%s\"\n" % title.replace("\"", "\\\"")
    if parent:
        out += "parent: %s\n" % parent
    out += "permalink: %s\n" % permalink
    if children:
        out += "has_children: true\nhas_toc: false\n"
    return out + "---\n"


def convert_game(src_dir, out_dir, game_id, title, icons_dir):
    files = {f.lower(): os.path.join(src_dir, f) for f in os.listdir(src_dir)}
    saves = []
    seen = set()

    for vmi_name, desc in read_list(os.path.join(src_dir, "SAVELIST.TXT")):
        base = os.path.splitext(vmi_name)[0]
        vmi = find_file(files, base + ".vmi")
        vms = find_file(files, base + ".vms")
        if not vmi or not vms:
            print("warning: %s/%s missing VMI/VMS, skipped" % (game_id, vmi_name), file=sys.stderr)
            continue
        if base.lower() in seen:
            print("warning: %s/%s listed twice, skipped" % (game_id, vmi_name), file=sys.stderr)
            continue
        seen.add(base.lower())
        saves.append((base, vmi, vms, vmu_filename(vmi), desc))

    if not saves:
        return False

    os.makedirs(out_dir)
    for base, vmi, vms, _, _ in saves:
        write_zip(os.path.join(out_dir, base + ".zip"), [vmi, vms])

    icon = os.path.join(out_dir, "icon0.png")
    for _, _, _, vmu, _ in saves:
        gif = os.path.join(icons_dir, vmu + ".GIF")
        if os.path.isfile(gif):
            write_icon(gif, icon)
            break
    else:
        if not any(write_vms_icon(vmi, vms, icon) for _, vmi, vms, _, _ in saves):
            print("warning: %s has no icon" % game_id, file=sys.stderr)

    with open(os.path.join(out_dir, "saves.txt"), "w", newline="\n") as f:
        for base, _, _, vmu, desc in saves:
            f.write("%s.zip=(%s) %s\n" % (base, vmu, desc))

    with open(os.path.join(out_dir, "README.md"), "w", newline="\n") as f:
        f.write(front_matter(title, "%s/%s/" % (SAVE_TYPE, game_id), parent=SAVE_TYPE + " Saves"))
        f.write("# %s\n\n## %s Saves - %s\n\n" % (title, SAVE_TYPE, game_id))
        f.write("| Icon | Filename | VMU File | Description |\n|------|----------|----------|-------------|\n")
        for base, _, _, vmu, desc in saves:
            f.write("| ![%s](icon0.png) | [%s.zip](%s.zip){: .btn .btn-purple } | `%s` | %s |\n"
                    % (md_escape(title), base, base, vmu, md_escape(desc)))

    return True


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: %s <dreamcast-saves path> <output path>" % sys.argv[0])

    src, out = sys.argv[1], sys.argv[2]
    icons_dir = os.path.join(src, "icons")

    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)

    games = []
    for game_id, title in read_list(os.path.join(src, "GAMELIST.TXT")):
        if convert_game(os.path.join(src, game_id), os.path.join(out, game_id), game_id, title, icons_dir):
            games.append((game_id, title))

    with open(os.path.join(out, "games.txt"), "w", newline="\n") as f:
        for game_id, title in games:
            f.write("%s=%s\n" % (game_id, title))

    with open(os.path.join(out, "README.md"), "w", newline="\n") as f:
        f.write(front_matter(SAVE_TYPE + " Saves", SAVE_TYPE + "/", children=True))
        f.write("# Games\n\n| Game | ID |\n|------|----|\n")
        for game_id, title in games:
            f.write("| [%s](%s/) | %s |\n" % (md_escape(title), game_id, game_id))

    print("%d games converted to %s" % (len(games), out))


if __name__ == "__main__":
    main()
