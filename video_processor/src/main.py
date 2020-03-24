import argparse
from .processors.VideoProcessor import VideoProcessor

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-c", "--capture", help="Main funcionality, captures frames and sends them to other processors. The expected argument is a port for pool_vd - output_module websocket communication",
                       type=int, default=8888)
    group.add_argument(
        "-r", "--record", help="Recording only. Expects the recording path", type=int, default=8444)

    parser.add_argument("-p", "--port", help="UDP listening port",
                        required=True, type=int, default=8444)
    parser.add_argument("-w", "--width", help="Width", required=True, type=int)
    parser.add_argument("-ht", "--height", help="Height",
                        required=True, type=int)
    parser.add_argument("-f", "--fps", help="Used in recording",
                        required=False, type=int, default=30)
    args = parser.parse_args()

    vp = VideoProcessor(args.port)
    if args.capture:
        vp.capture(args.width, args.height, args.capture)

    if args.record:
        if args.fps:
            vp.record(args.width, args.height, args.record, args.fps)
        else:
            vp.record(args.width, args.height, args.record)
