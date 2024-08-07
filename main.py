#!./venv/bin/python
import os
from pathlib import Path
from shutil import rmtree
import eyed3

from moviepy.editor import AudioFileClip, CompositeAudioClip, VideoFileClip

# from pytube import YouTube
from pytubefix import YouTube
import flet as ft


def main(page: ft.Page):
    page.title = "You Tube Downloader"
    page.window_maximized = True
    page.theme_mode = "dark"
    page.scroll = "always"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.snack_bar = ft.SnackBar(
        content=ft.Text("Hello, world!"),
        action="OK!",
        # open=False,
        bgcolor=ft.colors.ON_ERROR_CONTAINER,
        action_color=ft.colors.ON_INVERSE_SURFACE,
    )
    page.update()
    # minimo de 500px de ancho
    page.window_min_width = 500
    resolucion_pantalla = os.popen(r'xrandr | grep "\*" | cut -d" " -f4').read()
    # obtener el ancho de la pantalla
    ancho = resolucion_pantalla.split("x")[0]
    # obtener el alto de la pantalla
    alto = resolucion_pantalla.rsplit("x")[-1].strip("\n")

    # obtener el ancho de la pantalla
    page_width = int(ancho)
    # obtener el alto de la pantalla
    page_height = int(alto)
    # establecer el ancho del contenedor principal
    body_width = page_width / 3
    body_height = page_height * 0.6

    global my_path
    lista_calidades = []
    # dict_subs = {}
    # lista_subtitulos = ["Español", "Ingles", "Frances", "Aleman", "Italiano"]
    lista_subtitulos = []
    my_path = None
    imagen_fondo = "fondo.png"
    spinner = "spinner.gif"
    # print(imagen_fondo)

    # def cambiar_imagen():
    #     imagen_fondo = spinner
    #     cuadro_imagen.src = imagen_fondo

    def aceptar_url(
        event,
        imagen_video: ft.Image,
    ):
        global yt, titulo, thumbnail, dict_res, dict_subs, lista_subtitulos

        if input_text.value == "":
            page.snack_bar.content = ft.Text("No se ha ingresado ninguna url")
            page.snack_bar.open = True
            page.snack_bar.update()

        else:
            try:
                yt = YouTube(input_text.value)
                titulo = yt.title.replace(" ", "_").replace("/", "_").replace(":", "_")
                thumbnail = yt.thumbnail_url
                # cambiar url de la imagen
                imagen_video.src = thumbnail
                # imagen_video.update()
                resolucion = ["mp3"]
                dict_res = {}
                dict_subs = {}
                lista_subtitulos = []
                dict_res["mp3"] = "mp3"
                if yt.caption_tracks:
                    for i in yt.caption_tracks:
                        dict_subs[i.name] = i.code
                        lista_subtitulos.append(i.name)
                    # print(dict_subs)
                    # print(dict_subs.keys())
                    # print(dict_subs.values())
                    # print(lista_subtitulos)
                    # borro las options de subtitulos
                    drop_subtitulos.options = []
                    for x in lista_subtitulos:
                        print(dict_subs[x])
                        print(x)

                    drop_subtitulos.options = [
                        ft.dropdown.Option(x) for x in lista_subtitulos
                    ]
                    drop_subtitulos.value = drop_subtitulos.options[0].key
                    drop_subtitulos.update()
                    check_subtitulos.visible = True
                    check_subtitulos.disabled = False
                    check_subtitulos.update()
                print("Calidades disponibles:")
                contador = 0
                for stream in (
                    yt.streams.filter(adaptive=True, type="video", subtype="mp4")
                    .order_by("bitrate")
                    .asc()
                ):

                    # resolucion.append(stream.resolution)
                    if stream.resolution not in resolucion:
                        resolucion.append(stream.resolution)
                        dict_res[stream.resolution] = str(stream.itag)
                        # print(dict_res[stream.resolution])
                        # print(f"{contador} - {stream.resolution} - {stream.fps} fps")
                        contador += 1
                # dict_res['mp3'] = 'mp3'
                # cambiar el listado de calidades disponibles
                drop_calidades.options = [ft.dropdown.Option(x) for x in resolucion]
                # seleccionar la primera opcion por defecto
                drop_calidades.value = drop_calidades.options[0].key

                # print(drop_calidades.value,'calidad')
                drop_calidades.update()
                imagen_video.update()
                input_text.value = ""
                input_text.update()
                print(resolucion)
                print(dict_res)
                # print(titulo)

            except Exception as e:
                print(f"Error: {e}")
                page.snack_bar.content = ft.Text("Url no valida")
                page.snack_bar.open = True
                page.snack_bar.update()

    def activar_subtitulos(_):
        if not drop_subtitulos.visible:
            drop_subtitulos.visible = True
        else:
            drop_subtitulos.visible = False
        page.update()
        # print(drop_subtitulos.visible)

    # Open directory dialog
    def get_directory_result(e: ft.FilePickerResultEvent):
        global my_path
        open_folder_button.text = f"Se descargara en: {e.path}"
        open_folder_button.update()
        my_path = e.path if e.path else None
        # print(e.path)
        # directory_path.value = e.path if e.path else "Cancelled!"
        # directory_path.update()
        # if input_text.value != "":
        if titulo != "":
            download_button.disabled = False
            download_button.update()
        return my_path

    get_directory_dialog = ft.FilePicker(on_result=get_directory_result)
    # directory_path = ft.Text()

    # hide all dialogs in overlay
    page.overlay.extend([get_directory_dialog])

    def descargar_video(_, calidad, path_videos):
        # bloquear el boton de descargar
        download_button.disabled = True
        download_button.update()
        # bloquear el boton de seleccionar carpeta
        open_folder_button.disabled = True
        open_folder_button.update()
        # bloquear el boton de subtitulos
        # activar_subtitulos.disabled = True
        # activar_subtitulos.update()
        # bloquear el cuadro de texto
        input_text.disabled = True
        input_text.update()
        # bloquear el boton de aceptar
        input_text.disabled = True
        input_text.update()

        resolucion = calidad
        print(resolucion)
        if resolucion == "360p":  # or resolucion == "720p":
            print(f"descargando video a {resolucion}")
            cuadro_imagen.src = spinner
            cuadro_imagen.update()
            print(f"Descargando video {yt.title} en {resolucion}")
            # obtener el stream del video
            (
                yt.streams.filter(progressive=True, subtype="mp4", type="video")
                .get_by_resolution(resolucion)
                .download(output_path=path_videos, filename=f"{titulo}.mp4")
                # .download(output_path=path_videos, filename=f"{titulo}.mp4")
            )
        elif resolucion == "mp3":
            scriptPath = Path(__file__).parent
            path_videos = Path(path_videos)
            path_temporal = scriptPath / "temporal"
            #  / "temporal"
            path_temporal.mkdir(exist_ok=True)
            cuadro_imagen.src = spinner
            cuadro_imagen.update()
            # obtener el stream del audio
            stream = (
                yt.streams.get_audio_only(subtype="webm")
                # .download(output_path=path_videos, filename="mp3tmp")
                # -----audio con moviepy
                .download(output_path=path_temporal, filename="tmp.webm")
            )
            webm = path_temporal / "tmp.webm"
            audio = AudioFileClip(str(webm))
            new_audioclip = audio.subclip(0)
            new_audioclip.write_audiofile(webm.with_suffix(".mp3"))
            # os.remove(webm)
            os.rename(webm.with_suffix(".mp3"), path_videos / f"{titulo}.mp3")
            audiofile = eyed3.load(path_videos / f"{titulo}.mp3")
            rmtree(path_temporal)
            try:
                # print(yt.metadata[0]['Artist'])
                audiofile.tag.artist = yt.metadata[0]["Artist"]
                audiofile.tag.save()
            except Exception as e:
                print(f"No se pudo guardar el artista: {e}")

            try:
                audiofile.tag.title = yt.metadata[0]["Song"]
                audiofile.tag.save()
            except Exception as e:
                print(f"No se pudo guardar el titulo: {e}")
            try:
                audiofile.tag.album = yt.metadata[0]["Album"]
                audiofile.tag.save()
            except Exception as e:
                print(f"No se pudo guardar el album: {e}")
        else:
            print(f"entro donde no debia")
            scriptPath = Path(__file__).parent
            path_videos = Path(path_videos)
            path_temporal = scriptPath / "temporal"
            # path_videos = Path(path_videos)
            # path_temporal = path_videos/ "temporal"
            #  / "temporal"
            path_temporal.mkdir(exist_ok=True)
            print(path_videos)
            print(path_temporal)
            # obtener el stream del video
            # yt.streams.get_by_itag(dict_res[resolucion]).download(output_path=path_temporal, filename="tmp.mp4")
            yt.streams.filter(adaptive=True, type="video", subtype="mp4").get_by_itag(
                dict_res[resolucion]
            ).download(output_path=path_temporal, filename="tmp.mp4")
            cuadro_imagen.src = spinner
            cuadro_imagen.update()
            # obtener el stream del audio
            yt.streams.get_audio_only().download(
                output_path=path_temporal, filename="tmp.webm"
            )
            # unir el video y el audio

            path_video_sa = path_temporal / "tmp.mp4"
            video_sa = VideoFileClip(str(path_video_sa))
            path_audio_sa = path_temporal / "tmp.webm"
            audio_sv = AudioFileClip(str(path_audio_sa))
            # video = video.set_audio(audio)
            nuevo_audio = CompositeAudioClip([audio_sv])
            video_sa.audio = nuevo_audio
            path_video = path_videos / f"{titulo}.mp4"
            print(path_video)
            video_sa.write_videofile(str(path_video))
            audio_sv.close()
            video_sa.close()
            nuevo_audio.close()

            # borrar la carpeta temporal con el video y el audio
            rmtree(path_temporal)
        # finally:
        # si se descargo algun video y se selecciono el checkbox de subtitulos se descargan los subtitulos
        if check_subtitulos.value:
            print("Descargando subtitulos")
            print(drop_subtitulos.value)
            print(dict_subs)
            print(dict_subs[drop_subtitulos.value])
            # quit()
            subtitulo = yt.captions.get_by_language_code(
                dict_subs[drop_subtitulos.value]
            )
            # print(subtitulo)
            subtitulo.download(output_path=path_videos, title=f"{titulo}")
            # print("Subtitulos descargados")
        # si calidad es None se despliega un mensaje de error
        print(f"Se descargara en: {path_videos}")
        # print(input_text.value)
        print(f"calidad: {calidad}")
        print(f"Titulo: {titulo}")
        # bloquear el boton de descargar
        download_button.disabled = False
        download_button.update()
        # bloquear el boton de seleccionar carpeta
        open_folder_button.disabled = False
        open_folder_button.update()
        # bloquear el boton de subtitulos
        # activar_subtitulos.disabled = False
        # activar_subtitulos.update()
        # bloquear el cuadro de texto
        input_text.disabled = False
        input_text.update()
        # bloquear el boton de aceptar
        input_text.disabled = False
        input_text.update()
        # actualizar la cuadro_imagen
        cuadro_imagen.src = imagen_fondo
        cuadro_imagen.update()
        drop_calidades.disabled = False
        drop_calidades.options = []
        drop_calidades.update()
        drop_subtitulos.visible = False
        drop_subtitulos.options = []
        drop_subtitulos.update()
        check_subtitulos.visible = False
        check_subtitulos.disabled = True
        check_subtitulos.update()

    # cuadro de ingreso de url del video a descargar
    input_text = ft.TextField(
        label="Ingrese la url del video",
        label_style=ft.TextStyle(
            color=ft.colors.ON_SURFACE_VARIANT,
        ),
        # width=500,
        # height=100,
        border_radius=10,
        border_color=ft.colors.BLUE_GREY,
        border_width=2,
        bgcolor=ft.colors.SURFACE_VARIANT,
        text_align=ft.TextAlign.CENTER,
        expand=8,
        # al aceprar se se ejecuta el metodo on_click de download_button
        # on_submit=lambda _:print(_., input_text.value),
        on_submit=lambda _: aceptar_url(_, cuadro_imagen),
    )

    # boton para descargar el video
    download_button = ft.ElevatedButton(
        text="Descargar",
        width=body_width,
        height=40,
        bgcolor=ft.colors.SURFACE_VARIANT,
        color=ft.colors.ON_SURFACE_VARIANT,
        disabled=True,
        on_click=lambda _: descargar_video(_, drop_calidades.value, my_path),
    )

    # boton para abrir la carpeta de descargas

    open_folder_button = ft.ElevatedButton(
        text="Abrir carpeta de descargas",
        width=body_width,
        height=40,
        bgcolor=ft.colors.SURFACE_VARIANT,
        color=ft.colors.ON_SURFACE_VARIANT,
        on_click=lambda _: get_directory_dialog.get_directory_path(),
        disabled=page.web,
    )

    # contenedor para los botones
    button_container = ft.Container(
        width=body_width,
        height=body_height * 0.3,
        # padding=10,
        border_radius=10,
        content=ft.Column(
            [
                open_folder_button,
                download_button,
            ],
            col=1,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
    # boton aceptar entrada de texto
    accept_button = ft.ElevatedButton(
        text="Aceptar",
        width=100,
        # height=50,
        bgcolor=ft.colors.SURFACE_VARIANT,
        color=ft.colors.ON_SURFACE_VARIANT,
        expand=2,
        on_click=lambda _: aceptar_url(_, cuadro_imagen),
    )

    # contenedor para el cuadro de texto
    input_container = ft.Container(
        width=body_width * 1.4,
        height=body_height * 0.2,
        # padding=10,
        border_radius=10,
        col=1,
        # padding=2,
        content=ft.Row(
            [
                input_text,
                accept_button,
            ],
            col=1,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )
    drop_calidades = ft.Dropdown(
        options=[ft.dropdown.Option(i) for i in lista_calidades],
        label="Seleccione la calidad del video",
        label_style=ft.TextStyle(
            color=ft.colors.ON_SURFACE_VARIANT,
        ),
        border_color=ft.colors.BLUE_GREY,
        border_width=1,
        bgcolor=ft.colors.SURFACE_VARIANT,
    )

    drop_subtitulos = ft.Dropdown(
        options=[ft.dropdown.Option(i) for i in lista_subtitulos],
        label="Seleccione el idioma del subtitulo",
        label_style=ft.TextStyle(
            color=ft.colors.ON_SURFACE_VARIANT,
        ),
        # width=body_width,
        # height=70,
        border_color=ft.colors.BLUE_GREY,
        border_width=1,
        bgcolor=ft.colors.SURFACE_VARIANT,
        # visibilidad desactivada
        visible=False,
        # on_change=set_calidad,
    )
    cuadro_imagen = ft.Image(
        src=imagen_fondo,
        height=body_height * 0.7,
        border_radius=10,
        width=body_width,
        fit=ft.ImageFit.CONTAIN,
    )

    check_subtitulos = ft.Checkbox(
        label="Descargar subtitulos",
        value=False,
        on_change=activar_subtitulos,
        visible=False,
        disabled=True,
    )
    # cuerpo de la pagina
    body = ft.Container(
        height=body_height,
        width=body_width,
        border_radius=10,
        # padding= 10,
        content=ft.Column(
            [
                drop_calidades,
                ft.Row(
                    [
                        drop_subtitulos,
                        # ft.Checkbox(
                        #     label="Descargar subtitulos",
                        #     value=False,
                        #     on_change=activar_subtitulos,
                        #     # visible=False,
                        #     # disabled=True,
                        # ),
                        check_subtitulos,
                    ],
                    col=2,
                    alignment=ft.MainAxisAlignment.CENTER,
                    width=body_width,
                ),
                cuadro_imagen,
            ],
            col=1,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    tituloLabel = ft.AppBar(
        title=ft.Text(
            "You Tube Downloader",
            color=ft.colors.ON_SURFACE_VARIANT,
            # text_align=ft.TextAlign.CENTER,
            style=ft.TextThemeStyle.HEADLINE_LARGE,
        ),
        color=ft.colors.ON_SURFACE_VARIANT,
        bgcolor=ft.colors.ON_INVERSE_SURFACE,
        center_title=True,
    )

    # mostrar
    page.add(
        tituloLabel,
        input_container,
        body,
        button_container,
    )


if __name__ == "__main__":
    ft.app(
        target=main,
        # view=ft.WEB_BROWSER,
        assets_dir="assets",
        name="You Tube Downloader",
        use_color_emoji=True,
        route_url_strategy="path",
    )
