import os
from typing import List
from moviepy import VideoFileClip, concatenate_videoclips, AudioFileClip, afx, CompositeAudioClip

class VideoEditor:
    @staticmethod
    def render(
        video_paths: List[str],
        bg_path: str,
        tts_path: str,
        output_path: str
    ):
        clips = []
        final_video = None
        bg_audio = None
        tts_audio = None
        try:
            clips = [VideoFileClip(p) for p in video_paths]
            final_video = concatenate_videoclips(clips, method="compose")

            bg_audio = AudioFileClip(bg_path).with_effects([afx.AudioLoop(duration=final_video.duration)]).with_volume_scaled(0.2)
            tts_audio = AudioFileClip(tts_path)

            final_video = final_video.with_audio(CompositeAudioClip([bg_audio, tts_audio]))
            final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24, threads=4, logger=None)
            return output_path
        finally:
            if final_video:
                final_video.close()
            if bg_audio:
                bg_audio.close()
            if tts_audio:
                tts_audio.close()
            for c in clips:
                c.close()