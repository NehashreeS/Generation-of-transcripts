# Generation-of-transcripts

This project allows you to extract transcripts from YouTube videos or playlists. If transcripts are unavailable, the script downloads the audio, converts it to WAV, and transcribes it using the Ollama Llama 3.2 AI model.

## Requirements

- **Python 3.6 or higher**
- **Dependencies:**
    - `pytube`: For downloading YouTube videos.
    - `youtube-transcript-api`: For fetching available transcripts from YouTube.
    - `pydub`: For audio file format conversion (MP4 to WAV).
    - `ffmpeg-python`: A wrapper for FFmpeg, needed by `pydub`.
- **External Tools:**
    - **FFmpeg**: Required for audio processing.
    - **Ollama (Llama 3.2)**: For transcribing audio files.

### Installation

1. **Clone the repository**:
    ```bash
    git clone <your-github-repo-url>
    cd <your-project-directory>
    ```

2. **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Install FFmpeg**:
    - **For Windows**:
        - Download FFmpeg from [FFmpeg's official website](https://ffmpeg.org/download.html).
        - Extract the files and add the `bin` directory to your system's PATH.
    - **For macOS/Linux**:
        ```bash
        brew install ffmpeg   # macOS
        sudo apt install ffmpeg   # Linux
        ```

4. **Install Ollama (for audio transcription with Llama 3.2)**:
    - Follow installation instructions from [Ollama](https://ollama.com/).

---

## How to Use

### Run the script:

To transcribe YouTube videos or playlists, use the following command:

```bash
python youtube_transcriber.py <YouTube_URL> <Output_Folder>
