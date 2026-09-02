import subprocess
from pathlib import Path

def create_tech_ambient_drone(duration: float, output_path: Path):
    """
    Generates a low, focused, futuristic synth-ambient background drone
    using harmonic sine synthesis and lowpass filtering in FFmpeg.
    """
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"sine=frequency=110:duration={duration+3},aformat=channel_layouts=stereo",
        "-f", "lavfi", "-i", f"sine=frequency=165:duration={duration+3},aformat=channel_layouts=stereo",
        "-f", "lavfi", "-i", f"sine=frequency=220:duration={duration+3},aformat=channel_layouts=stereo",
        "-filter_complex", (
            "[0:a]volume=0.04[a0];"
            "[1:a]volume=0.03[a1];"
            "[2:a]volume=0.02[a2];"
            "[a0][a1][a2]amix=inputs=3:duration=first,lowpass=f=450,afade=t=in:ss=0:d=1,afade=t=out:st={duration}:d=2[outa]"
        ),
        "-map", "[outa]",
        "-c:a", "aac",
        "-b:a", "128k",
        str(output_path)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
