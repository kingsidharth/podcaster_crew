import os
from crewai.tools import BaseTool, tool
from typing import Type
from pydantic import BaseModel, Field
from crewai_tools import FileWriterTool, FileReadTool, SerperDevTool
from google import genai
from google.genai import types
import wave
import datetime
import base64

def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)
    

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."

file_writer_tool = FileWriterTool()

# result_1 = file_writer_tool._run('example.txt', 'This is a test content.', 'knowledge/')


file_read_tool = FileReadTool()

# result_2 = FileReadTool(file_path='knowledge/')

search_tool = SerperDevTool()


@tool
def gemini_voice_tool(script: str) -> str:
    """
    Use this tool to generate a voice for the text.
    """
    client = genai.Client(api_key=(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")))
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=script,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                    speaker_voice_configs=[
                    types.SpeakerVoiceConfig(
                        speaker='Joe',
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name='Kore',
                            )
                        )
                    ),
                    types.SpeakerVoiceConfig(
                        speaker='Jane',
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name='Puck',
                            )
                        )
                    ),
                    ]
                )
            )
        )
    )
    
    parts = getattr(response.candidates[0].content, 'parts', [])
    inline = None
    for p in parts:
        maybe_inline = getattr(p, 'inline_data', None)
        if maybe_inline is not None and getattr(maybe_inline, 'data', None):
            inline = maybe_inline
            break

    if inline is None or getattr(inline, 'data', None) is None:
        raise ValueError("Gemini did not return inline audio data.")

    audio_bytes = inline.data
    if isinstance(audio_bytes, str):
        audio_bytes = base64.b64decode(audio_bytes)
    else:
        audio_bytes = bytes(audio_bytes)

    if not audio_bytes:
        raise ValueError("Gemini returned empty audio data.")

    # Ensure output directory exists and create a unique filename
    output_dir = os.path.join(os.getcwd(), "outputs")
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(output_dir, f"podcast-{timestamp}.wav")
    wave_file(filename, audio_bytes)
    return filename
