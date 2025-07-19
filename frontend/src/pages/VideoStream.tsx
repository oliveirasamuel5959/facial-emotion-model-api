import React, { useState } from "react"
import Navbar from "../components/Navbar";
import './stream.css'
const VideoStream = () => {

    const [getVideo, setGetVideo] = useState(false);

    const STREAM_URL = 'http://localhost:5000/video_feed';

    const handleStartStream = () => {
        setGetVideo(true);
    }

    const handleStopStream = () => {
        setGetVideo(false);
    }

    return (
    <div className="video_stream">
        <Navbar />
        {getVideo ? (
            <div className="stream_content">
                <img
                    src={STREAM_URL}
                    alt="Live Video Feed"
                    style={{
                        width: "640px",
                        height: "480px",
                        border: "1px solid black",
                    }}
                />
                <button onClick={handleStopStream}>Stop Stream</button>
            </div>
        ) : (
            <div className="stream_content">
                <h1>Video Stream</h1>
                <button onClick={handleStartStream}>Start Stream</button>
            </div>
        )}
    </div>
);
}

export default VideoStream;