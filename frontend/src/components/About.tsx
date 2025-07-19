import React from 'react'
import AboutBackground from '../assets/about-background.png';
import AboutBackgroundImage from '../assets/medicine-ai.jpg';
import { BsFillPlayCircleFill } from 'react-icons/bs';

const About = () => {
  return (
    <div className='about-section-container'>
        <div className="about-background-image">
            {/* <img src={AboutBackground} alt="" /> */}
        </div>
        <div className="about-section-image-container">
            {/* <img src={AboutBackgroundImage} alt="" /> */}
        </div>
        <div className="about-section-text-container">
            <p className='primary-subheading'>About</p>
            <h1 className='primary-heading'>
                Emotions Plays An Important Role In A Patient Health
            </h1>
            <p className="primary-text">
                Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
                Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, 
                when an unknown printer took a galley of type and scrambled it to make a type specimen book.
            </p>
            <p className="primary-text">
                It has survived not only five centuries, but also the leap into electronic typesetting, 
                remaining essentially unchanged. It was popularised in the 1960s with the release of 
                Letraset sheets containing Lorem Ipsum passages, 
                and more recently with desktop publishing software 
                like Aldus PageMaker including versions of Lorem Ipsum
            </p>
            <div className="about-buttons-container">
                <button className='secondary-button'>Learn More</button>
                <button className='watch-video-button'>
                    {" "}
                    <BsFillPlayCircleFill />
                    Watch Video</button>
            </div>
        </div>
    </div>
  )
}

export default About
