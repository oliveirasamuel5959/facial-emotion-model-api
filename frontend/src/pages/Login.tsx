import React from 'react';
import { FaUser, FaLock } from 'react-icons/fa';
import { useRef, useEffect, useState } from 'react';
import { Navigate, replace, useNavigate } from 'react-router-dom';
import axios, { AxiosError  } from 'axios';
// import axios from '../api/axios';

import './login.css';
import { NavLink } from 'react-router-dom';
import Home from './Home';

const Login = () => {

    const userRef = useRef(null);
    const errRef = useRef(null);

    const [userName, setUserName] = useState("");
    const [password, setPassword] = useState("");
    const [errMsg, setErrMsg] = useState("");
    const [success, setSuccess] = useState(false);

    const navigate = useNavigate();

    const url = 'http://localhost:5000/login';

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();

        const userData = {
            name: userName,
            password: password
        };

        if (userName !== "" || password !== "") {
            setErrMsg('');
        }

        try {
            const response = await axios.post(url, 
                JSON.stringify(userData),
                {
                    headers: { 'Content-Type': 'application/json' },
                    withCredentials: false
                }
            );
            console.log(JSON.stringify(response?.data));
            // const accessToken = response?.data?.accessToken;
            console.log('response', response.data.success)

            if (response.data.success) {
                setSuccess(true);
                navigate('/home', {replace: true})
            }
            else
                setErrMsg('Incorrect username or password')

        } catch (err) {
            const error = err as AxiosError
            if (!error?.response) {
                setErrMsg('No Server Response')
            } else if (error.response?.status === 400) {
                setErrMsg('Missing username or password')
            } else if (error.response?.status === 401) {
                setErrMsg('Unauthorized');
            } else {
                setErrMsg('Login Failed');
            }
            setUserName('');
            setPassword('');
            // errRef.current.focus();
        }   
    }

    return (
        <>
            {success ? (
                <section className='up_message'>
                    <h1>You are logged in</h1>
                </section>
            ) : (
                <div className="container">
                    <p ref={errRef} className="error_mesg">{errMsg}</p>
                    <form onSubmit={handleSubmit}>
                        <h1>Login</h1>
                        <div className='input_field'>
                            <input 
                                type="text"
                                ref={userRef}
                                placeholder="username" 
                                onChange={(e) => setUserName(e.target.value)}
                                value={userName}
                                required
                            /> 
                            <span className="icon">
                                <FaUser />
                            </span>
                        </div>
                        <div className='input_field'>
                            <input 
                                type="password" 
                                placeholder="password"
                                onChange={(e) => setPassword(e.target.value)}
                                value={password}
                                required
                            />
                            <span className="icon">
                                <FaLock />
                            </span>
                        </div>
                        <div className='recall-forget'>
                            <label>
                                <input type="checkbox" />
                                Remember Me
                            </label>
                            <a href="#">Forgot password?</a>
                        </div>
                        <button>Submit</button>
                        <div className="signup-link">
                            <p>
                                Don't have an account ? <a href="#">Register</a>
                            </p>
                        </div>

                    </form>
                </div>
            )}
        </>
    );
};

export default Login;