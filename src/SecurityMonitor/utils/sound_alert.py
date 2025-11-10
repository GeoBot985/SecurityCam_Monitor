import platform
import time
import simpleaudio as sa


def play_alert(sound_path=None, repeat=5, interval=0.3):
    """Plays an alert sound (wav) or repeats system beeps if none provided."""
    system = platform.system()

    for i in range(repeat):
        if sound_path:
            try:
                wave_obj = sa.WaveObject.from_wave_file(sound_path)
                play_obj = wave_obj.play()
                play_obj.wait_done()
            except Exception as e:
                print(f"⚠️ Sound play failed: {e}")
                _fallback_beep(system)
        else:
            _fallback_beep(system)

        time.sleep(interval)


def _fallback_beep(system):
    """Cross-platform fallback beep."""
    if system == "Windows":
        import winsound
        winsound.Beep(1000, 3000)  # 1000 Hz for 3 seconds
    else:
        print("\a", end="", flush=True)
        time.sleep(0.3)
