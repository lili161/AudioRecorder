import pyaudio as au;
import wave;
import keyboard;
import time;
import sys;

RATE = 16000;
CHANNEL = 2;
FORMAT = au.paInt32;
data = [];
isRecord = False;


def main(arg):
    if len(arg) > 2:
        print("TOO MANY ARGUMENTS");
    if len(arg) == 2:
        if (arg[1] == "-h"):
            global RATE;
            RATE = 24000;
    print("Press [R] and hold on to record");
    while not keyboard.record('r'):
        if keyboard.record('r'):
            break;
    record();


def keyListener(x):
    global isRecord;
    press = keyboard.KeyboardEvent('down', 28, 'r');
    release = keyboard.KeyboardEvent('up', 28, 'r');
    if x.event_type == 'down' and x.name == press.name:
        isRecord = True;
    if x.event_type == 'up' and x.name == release.name:
        isRecord = False;


def callback(in_data, frame_count, time_info, status):
    if isRecord:
        data.append(in_data);
        print('Recording------------ Press [Esc] to stop.')

    return (in_data, au.paContinue)


def record():
    p = au.PyAudio();
    stream = p.open(format=FORMAT, channels=CHANNEL, rate=RATE, input=True, stream_callback=callback);
    stream.start_stream();
    while True:
        keyboard.hook(keyListener)
        if keyboard.record('esc'):
            times = time.strftime("%Y年%m月%d日%H时%M分%S秒", time.localtime()) + '.wav';
            wf = wave.open(times, 'wb');
            wf.setnchannels(CHANNEL)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(data))
            wf.close()
            break;

    stream.stop_stream();
    stream.close();
    p.terminate();
    print("\n")
    print("file saved.")


if __name__ == '__main__':
    main(sys.argv);
