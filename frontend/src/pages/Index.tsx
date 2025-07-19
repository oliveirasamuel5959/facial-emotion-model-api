import React from 'react'
import Navbar2 from '../components/Navbar2'
import BannerBackground from '../assets/ai-home-image.jpg'
import BannerImage from '../assets/ai-image-home-banner.jpg'
import { FiArrowRight } from 'react-icons/fi'
import About from '../components/About'
import Work from '../components/Work'
import Contact from '../components/Contact'
import Footer from '../components/Footer'

const Index = () => {
    return (
        <div>
        <Navbar2 />
        <div className='home-banner-container'>
            <div className="home-bannerImage-container">
                {/* <img src={BannerBackground} alt="" /> */}
            </div>
            <div className='home-text-section'>
                <h1 className='primary-heading'>
                    Computer Vision Facial Emotion Recognition
                </h1>
                <p className='primary-text'>
                    Monitoring patients emotions in healthcare
                </p>
                <button className='secondary-button'>
                    Start Now <FiArrowRight />
                </button>
            </div>
            <div className='home-image-container'>
                {/* <img src={BannerImage} alt="" /> */}
            </div>
        </div>
        <About />
        <Work />
        <Contact />
        <Footer />
        </div>
    )
}

export default Index
