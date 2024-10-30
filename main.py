import os
import platform
import subprocess

import flet as ft
import ffmpeg

video_extensions = [
    "mp4",
    "webm",
    "mkv",
    "flv",
    "vob",
    "ogv",
    "rrc",
    "gifv",
    "mng",
    "mov",
    "avi",
    "qt",
    "wmv",
    "yuv",
    "rm",
    "asf",
    "amv",
    "m4p",
    "mpg",
    "mp2",
    "mpeg",
    "mpe",
    "mpv",
    "m4v",
    "svi",
    "3gp",
    "3g2",
    "mxf",
    "roq",
    "nsv",
    "flv",
    "f4v",
    "f4p",
    "f4a",
    "f4b",
    "mod",
    "ts",
]

audio_extensions = [
    "mp3",  # MPEG Layer 3 Audio
    "wav",  # Waveform Audio File
    "flac",  # Free Lossless Audio Codec
    "aac",  # Advanced Audio Coding
    "ogg",  # Ogg Vorbis
    "m4a",  # MPEG-4 Audio
    "wma",  # Windows Media Audio
    "aiff",  # Audio Interchange File Format
    "alac",
]

ALLOW_EXTENSTIONS = video_extensions + audio_extensions


def main(page: ft.Page):
    page.title = "Extracker"
    page.window_min_height = 720
    page.window_min_width = 1080

    selected_type = ft.Text("mp4")

    main_section = ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    left_naviations = ft.Container(
        bgcolor=ft.colors.AMBER,
        width=300,
        border_radius=ft.border_radius.all(5),
        content=ft.Column(expand=True, wrap=False, scroll="always"),
    )

    def radiogroup_changed(e):
        selected_type.value = e.control.value

    def handle_export(path: str, fileName: str):
        dirName, ex = path.split(fileName)

        if selected_type.value.lower() == "mp4":
            main_section.controls.append(
                ft.ProgressBar(color="#a616fb", bgcolor="#e58969", border_radius=4)
            )
            page.update()
            convert_to_mp4(path, f"{dirName}{fileName}_extracker.mp4")
            main_section.controls.pop()
            page.update()
        if selected_type.value.lower() == "mp3":
            main_section.controls.append(
                ft.ProgressBar(color="#a616fb", bgcolor="#e58969", border_radius=4)
            )
            page.update()
            convert_to_mp3(path, f"{dirName}{fileName}_extracker.mp3")
            main_section.controls.pop()
            page.update()

    def handleFilePick(e: ft.FilePickerResultEvent):
        if e.files:

            for singleFile in e.files:
                fileName, extention = singleFile.name.split(".")
                if extention.lower() in video_extensions:
                    main_section.controls[0] = ft.Row(
                        controls=[
                            ft.RadioGroup(
                                content=ft.Row(
                                    [
                                        ft.Radio(value="mp4", label="MP4"),
                                        ft.Radio(value="mp3", label="MP3"),
                                    ]
                                ),
                                value="mp4",
                                on_change=radiogroup_changed,
                            ),
                            ft.FilledButton(
                                "Open",
                                on_click=lambda _: file_picker.pick_files(
                                    allowed_extensions=ALLOW_EXTENSTIONS
                                ),
                                icon=ft.icons.ADD,
                            ),
                            ft.ElevatedButton(
                                "Export",
                                on_click=lambda _: handle_export(
                                    singleFile.path, fileName
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    )

                    if len(main_section.controls) > 1:
                        main_section.controls.pop(1)
                    main_section.controls.append(
                        ft.Container(
                            content=ft.Video(
                                playlist=[ft.VideoMedia(singleFile.path)],
                                expand=True,
                                filter_quality=ft.FilterQuality.HIGH,
                            ),
                            border_radius=ft.border_radius.all(5),
                            expand=True,
                        )
                    )

                    page.update()
                elif extention.lower() in audio_extensions:

                    main_section.controls[0] = ft.Row(
                        controls=[
                            ft.RadioGroup(
                                content=ft.Row(
                                    [
                                        ft.Radio(value="mp4", label="MP4"),
                                        ft.Radio(value="mp3", label="MP3"),
                                    ]
                                ),
                                value="mp4",
                                on_change=radiogroup_changed,
                            ),
                            ft.FilledButton(
                                "Open",
                                on_click=lambda _: file_picker.pick_files(
                                    allowed_extensions=ALLOW_EXTENSTIONS
                                ),
                                icon=ft.icons.ADD,
                            ),
                            ft.ElevatedButton(
                                "Export",
                                on_click=lambda _: handle_export(
                                    singleFile.path, fileName
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    )
                    # ffmpeg.input(
                    #     singleFile.path,
                    # ).output(f"{singleFile.name}.png", vframes=1).run()

                    if len(main_section.controls) > 1:
                        main_section.controls.pop(1)
                    main_section.controls.append(
                        ft.Container(
                            content=ft.Video(
                                playlist=[ft.VideoMedia(singleFile.path)],
                                expand=True,
                                filter_quality=ft.FilterQuality.HIGH,
                            ),
                            border_radius=ft.border_radius.all(5),
                            expand=True,
                        )
                    )
                    page.update()

    file_picker = ft.FilePicker(on_result=handleFilePick)

    main_section.controls.append(
        ft.Container(
            content=ft.Column(
                [
                    ft.Icon(
                        name=ft.icons.ATTACH_FILE_OUTLINED,
                        size=64,
                    ),
                    ft.Text(
                        "Click to upload",
                        text_align=ft.alignment.center,
                        selectable=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            alignment=ft.alignment.center,
            border=ft.border.all(1, ft.colors.WHITE38),
            border_radius=ft.border_radius.all(5),
            expand=True,
            on_click=lambda _: file_picker.pick_files(
                allowed_extensions=ALLOW_EXTENSTIONS
            ),
        )
    )

    exportRow = ft.Row(
        [
            main_section,
        ],
        spacing=2,
        expand=True,
    )
    page.overlay.append(file_picker)
    page.add(
        exportRow,
    )


def convert_to_mp4(path: str, output: str):
    try:
        stream = ffmpeg.input(path).output(output, codec="copy")
        ffmpeg.run(stream, overwrite_output=True, quiet=True)
        open_file_explorer(path, output)
    except ffmpeg.Error as e:
        print(e)


def convert_to_mp3(path: str, output: str):
    try:

        # Run the ffmpeg conversion
        stream = ffmpeg.input(path).output(output, format="mp3", audio_bitrate="192k")
        ffmpeg.run(stream, overwrite_output=True, quiet=True)
        open_file_explorer(path, output)
    except ffmpeg.Error as e:
        print(f"Error during conversion: {e}")


def open_file_explorer(dir, fileName):
    # home_dir = os.path.expanduser("~")

    downloads_dir = os.path.join(dir, fileName)

    abs_path = os.path.abspath(os.path.expanduser(downloads_dir))

    # Check if path exists
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Path does not exist: {abs_path}")

    # Detect the operating system
    system = platform.system().lower()

    try:
        # macOS
        if system == "darwin":
            subprocess.run(["open", abs_path])

        # Windows
        elif system == "windows":
            subprocess.run(["explorer", abs_path])

        # Linux (will try common file managers)
        elif system == "linux":
            # List of common Linux file managers
            file_managers = [
                ["xdg-open", abs_path],  # Generic open command
                ["nautilus", abs_path],  # GNOME
                ["dolphin", abs_path],  # KDE
                ["nemo", abs_path],  # Cinnamon
                ["thunar", abs_path],  # XFCE
                ["pcmanfm", abs_path],  # LXDE
            ]

            # Try each file manager until one works
            for fm_command in file_managers:
                try:
                    subprocess.run(fm_command)
                    break
                except FileNotFoundError:
                    continue
            else:
                raise FileNotFoundError("No supported file manager found")

        return True

    except Exception as e:
        print(f"Error opening file explorer: {str(e)}")
        return False


ft.app(main)
