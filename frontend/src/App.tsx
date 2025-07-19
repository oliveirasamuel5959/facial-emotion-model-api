import React from 'react';
import './App.css';

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Home from './pages/Home';
import Index from './pages/Index';
import VideoStream from './pages/VideoStream';
import Image from './pages/Image';

const App = () => {
  return (
    <BrowserRouter >
      {/* <Navbar /> */}
      <Routes>
        <Route path="/" element={<Index />} />
        <Route path="/login" element={<Login />} />
        <Route path="/home" element={<Home />} />
        <Route path="/stream" element={<VideoStream />} />
        <Route path="/image" element={<Image />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
