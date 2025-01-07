import os
import ntpath
import glob

# gitignore manim cached files that would bloat repo and are not necessary
dir_filetype_list = [
    [r'2024/FrameExtractor/in', ['mp4']], [r'2024/FrameExtractor/out', ['jpg']],

    [r'2024/V1-1/media/images', ['png']],
    [r'2024/V1-1/media/Tex', ['svg','tex']],
    [r'2024/V1-1/media/texts', ['svg']],
    [r'2024/V1-1/media/videos/additionalCounters/300p60', ['mp4']],
    [r'2024/V1-1/media/videos/additionalCounters/480p15', ['mp4']],
    [r'2024/V1-1/media/videos/additionalCounters/2160p60', ['mp4']],
    [r'2024/V1-1/media/videos/additionalCounters/3840p60/partial_movie_files', ['mp4']],
    [r'2024/V1-1/media/videos/Combined/480p15', ['mp4']],
    [r'2024/V1-1/media/videos/Combined/2160p60/partial_movie_files', ['mp4']],
    [r'2024/V1-1/media/videos/counter/480p15', ['mp4']],
    [r'2024/V1-1/media/videos/counter/2160p60/partial_movie_files', ['mp4']],

    #v1-2
    [r'2024/V1-2/media/images', ['png']],
    [r'2024/V1-2/media/Tex', ['svg','tex']],
    [r'2024/V1-2/media/texts', ['svg']],
    [r'2024/V1-2/media/videos/Approximation/480p15/partial_movie_files', ['mp4']],
    [r'2024/V1-2/media/videos/Bezier/480p15/partial_movie_files', ['mp4']],
    [r'2024/V1-2/media/videos/WindEnergie/480p15', ['mp4']],
    [r'2024/V1-2/media/videos/WindEnergie/720p30', ['mp4']],
    [r'2024/V1-2/media/videos/WindEnergie/2160p60/partial_movie_files', ['mp4']],
    [r'2024/V1-2/media/videos/WindEnergieCurrent/480p15', ['mp4']],
    [r'2024/V1-2/media/videos/WindEnergieCurrent/2160p60/partial_movie_files', ['mp4']],
    [r'2024/V1-2/media/videos/WindEnergieVoltage/480p15/', ['mp4']],
    [r'2024/V1-2/media/videos/WindEnergieVoltage/2160p60/partial_movie_files', ['mp4']],

    #v1-3
    [r'2024/V3-1+3/media/images', ['png']],
    [r'2024/V3-1+3/media/Tex', ['svg','tex']],
    [r'2024/V3-1+3/media/texts', ['svg']],
    [r'2024/V3-1+3/media/videos/Wasserstoff/480p15', ['mp4']],
    [r'2024/V3-1+3/media/videos/Wasserstoff/2160p60/partial_movie_files', ['mp4']],

    #v3-2
    [r'2024/V3-2/media/images', ['png']],
    [r'2024/V3-2/media/Tex', ['svg','tex']],
    [r'2024/V3-2/media/texts', ['svg']],
    [r'2024/V3-2/media/videos/Kennlinie/480p15', ['mp4']],
    [r'2024/V3-2/media/videos/Kennlinie/2160p60/partial_movie_files', ['mp4']],

    #v4-1
    [r'2024/V4-1/media/images', ['png']],
    [r'2024/V4-1/media/Tex', ['svg','tex']],
    [r'2024/V4-1/media/texts', ['svg']],
    [r'2024/V4-1/media/videos/Current/480p15', ['mp4']],
    [r'2024/V4-1/media/videos/Current/2160p60/partial_movie_files', ['mp4']],
    [r'2024/V4-1/media/videos/Voltage/480p15', ['mp4']],
    [r'2024/V4-1/media/videos/Voltage/2160p60/partial_movie_files', ['mp4']],
]

#generate centralized gitignore?
central_gitignore = r'2024/.gitignore'
central_gitignore_content = ""
project_folder_path = r'C:\Users\bened\PycharmProjects\h2school'

"""
for dir_filetype in dir_filetype_list:
    dir = project_folder_path +"/" +dir_filetype[0]
    filetypes = dir_filetype[1]
    gitignore = f"{dir}/.gitignore"
    content = os.listdir(dir)
    filtered_content = [f for f in content if f.split('.')[-1] in filetypes]
    dir_gitignore_content = ""
    if len(filtered_content)>0:
        for f in filtered_content:
            dir_gitignore_content += f"{ntpath.basename(dir)}/{f}\n"
            central_gitignore_content += f"\n# {os.path.relpath(dir, os.path.commonprefix([dir, project_folder_path]))}/{f}"
    else:
        dir_gitignore_content += f"#No currently cached files in {os.path.relpath(dir, os.path.commonprefix([dir, project_folder_path]))}\n"
        central_gitignore_content += f"\n#No currently cached files in {os.path.relpath(dir, os.path.commonprefix([dir, project_folder_path]))}\n"
        for ext in filetypes:
            dir_gitignore_content += f"{ntpath.basename(dir)}/.*{ext}\n"
            central_gitignore_content += f"\n# {os.path.relpath(dir, os.path.commonprefix([dir, project_folder_path]))}/.*{ext}"

    if True: #not os.path.exists(gitignore):
        with open(gitignore, 'w') as f:
            f.write(dir_gitignore_content)

    else:
        print(f"Already exists: {gitignore}")
        print(f"Content: {dir_gitignore_content}")
        print(f"Existing Content: {open(gitignore, 'r').read()}")


print(f"Centralized gitignore content: {central_gitignore_content}")
if not os.path.exists(project_folder_path +"/" + central_gitignore):
    with open(project_folder_path +"/" + central_gitignore, 'w') as f:
        f.write(central_gitignore_content)
"""




for dir_filetype in dir_filetype_list:
    dir = project_folder_path +"/" +dir_filetype[0]
    print(f"Dir: {dir}")
    filetypes = dir_filetype[1]
    gitignore = f"{dir}/.gitignore"
    content = [val for sublist in [[os.path.join(i[0], j) for j in i[2]] for i in os.walk(dir)] for val in sublist]#glob.glob(dir, recursive=True)#os.listdir(dir)
    filtered_content = [f for f in content if f.split('.')[-1] in filetypes]
    dir_gitignore_content = ""
    if len(filtered_content)>0:
        for f in filtered_content:
            #dir_gitignore_content += f"{os.path.relpath(dir, os.path.commonprefix([dir, f]))}/{ntpath.basename(f)}\n"
            dir_gitignore_content += f"**/{ntpath.basename(f)}\n"
            print(f"Adding {f} dir {dir} commonPrefix {os.path.commonprefix([dir, f])} and {os.path.relpath(os.path.commonprefix([dir, f]), dir)}")
            central_gitignore_content += f"\n# {os.path.relpath(dir, os.path.commonprefix([dir, project_folder_path]))}/{f}"
    else:
        dir_gitignore_content += f"#No currently cached files in {os.path.relpath(dir, os.path.commonprefix([dir, project_folder_path]))}\n"
        central_gitignore_content += f"\n#No currently cached files in {os.path.relpath(dir, os.path.commonprefix([dir, project_folder_path]))}\n"
        for ext in filetypes:
            dir_gitignore_content += f"{ntpath.basename(dir)}/.*{ext}\n"
            central_gitignore_content += f"\n# {os.path.relpath(dir, os.path.commonprefix([dir, project_folder_path]))}/.*{ext}"

    if True: #not os.path.exists(gitignore):
        with open(gitignore, 'w') as f:
            f.write(dir_gitignore_content)

    else:
        print(f"Already exists: {gitignore}")
        print(f"Content: {dir_gitignore_content}")
        print(f"Existing Content: {open(gitignore, 'r').read()}")


print(f"Centralized gitignore content: {central_gitignore_content}")
if not os.path.exists(project_folder_path +"/" + central_gitignore):
    with open(project_folder_path +"/" + central_gitignore, 'w') as f:
        f.write(central_gitignore_content)
        
"""

#generate centralized gitignore
for filetype in dir_filetype_list:
    dir = filetype[0].split('/', 1)[1]
    for ext in filetype[1]:
        central_gitignore_content += f"\n{dir}/*.{ext}"

print(f"Centralized gitignore content: {central_gitignore_content}")
with open(project_folder_path+"/"+central_gitignore, 'w') as file:
    file.write(central_gitignore_content)
"""