import React from "react";
import FileUpload from "../components/FileUpload";
import Navbar from "../components/Navbar";
import './Image.css';

const Image = () => {

    const data = [
        {
            name: "Happy",
            image_size: "480x640"
        },
        {
            name: "Sad",
            image_size: "480x640"
        },
        {
            name: "Angry",
            image_size: "480x640"
        }
    ];

    return (
        <div className="image-container">
            <Navbar />
            <div className="image-file-container">
                <h1 className="primary-heading">Image Emotion Analysis</h1>
                <FileUpload />
            </div>
        </div>
    )
};

export default Image;