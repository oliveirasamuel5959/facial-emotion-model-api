import React, { useState } from "react"
import { useLocation } from "react-router-dom";
import './home.css'
import Navbar from "../components/Navbar";
import Welcome from "../components/Welcome";

const Home = () => {
    const location = useLocation();
    console.log("Location: ", location)
    const name = location.state?.name;

    return (
        <div className="home_container">
            <Navbar />
            <h1>Welcome, { name }</h1>
        </div>
    )
}

export default Home;