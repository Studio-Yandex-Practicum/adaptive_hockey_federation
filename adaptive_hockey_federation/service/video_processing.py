import cv2


# TODO моковая реализация для нарезки видео подключается к воркеру
# Пример сигнатуры
# input_file = os.path.join(
#     os.path.dirname(__file__),
#     "test_video/2023-09-26-11.mp4",
# )
# output_file = os.path.join(
#     os.path.dirname(__file__),
#     "test_video/test.mp4",
# )
# frames = [i for i in range(15000, 15430, 5)]


def slicing_video_with_player_frames(input_file, output_file, frames, fps=25):
    cap = cv2.VideoCapture(input_file)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    output = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    for fr in range(len(frames)):  # frames - список фреймов с игроком
        cap.set(cv2.CAP_PROP_POS_FRAMES, frames[fr])
        for _ in range(frames[fr], frames[fr] + 5):
            _, frame = cap.read()
            output.write(frame)
    output.release()
    cap.release()
