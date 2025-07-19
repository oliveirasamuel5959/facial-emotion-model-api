import React, { useState } from "react";
import './fileUpload.css';
import axios, { AxiosError } from "axios";
// import { Tune } from "@mui/icons-material";

const FileUpload = () => {

    interface BaseImageData {
        image: {
            name: string;
            timestamp: number;
            content: string |  null;
        }
        collection_name: string
    }

    const [fileLoaded, setFileLoaded] = useState<File | null>(null);
    const [fileUploaded, setFileUploaded] = useState(false);
    const [fileName, setFileName] = useState('');
    const [errMsg, setErrMsg] = useState('');
    const [imagePreview, setImagePreview] = useState<string | null>(null);
    const [imagePredPreview, setimagePredPreview] = useState<string | null>(null);
    const [base64Data, setBase64Data] = useState<string | null>(null);
    const [responseSuccess, setResponseSuccess] = useState(false);
    const [getResponseSuccess, setGetResponseSuccess] = useState(false);
    const [tryAgain, setTryAgain] = useState(false);

    const PORT_URL = 'https://ai.emovio.com.br/api/v1/predictions/from/image';
    // const GET_URL = 'https://ai.emovio.com.br/api/v1/predictions/Samuel';

    const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {

        try {
                const file = event.target.files?.[0];

                if (file) {
                    setFileLoaded(file);
                    setFileUploaded(true);
                    setFileName(file.name);
                    setTryAgain(false);
                    const imageURL = URL.createObjectURL(file);
                    setErrMsg('Input File Loaded Success');
                    setImagePreview(imageURL);
                } else {
                    setErrMsg('File not loaded');
                }

            } catch (err) {
                const error = err as AxiosError;
                setErrMsg('Fatal Error: ' + {error});
            }
    }

    const handlePredict = (event: React.FormEvent) => {
        event?.preventDefault();
        
        try {
                if (!fileLoaded) {
                    setErrMsg('Nenhum arquivo carregado');
                return;
                }

                const reader = new FileReader();

                reader.onloadend = async() => {
                    const base64String = reader.result as string;

                    // Montar o objeto já com base64
                    const base_data: BaseImageData = {
                        image: {
                            name: fileName,
                            timestamp: Date.now(),
                            content: base64String.split(',')[1],
                        },
                        collection_name: 'Image base64 for Emotion Analysis',
                    };

                    setBase64Data(base64String);
                    console.log('baseData', base_data);

                    // Post Request to send image in base64 format
                    try {
                        setErrMsg('Start predict request...');
                        const response = await axios.post(PORT_URL,
                            JSON.stringify(base_data),
                            {
                                headers: { 'Content-Type': 'application/json' },
                                withCredentials: false
                            }
                        );

                        const parsedBody = JSON.parse(response.data[0].body)
                        const imageSrc = `data:image/png;base64,${parsedBody.pred_image}`;

                        console.log('post response data', parsedBody);

                        if (response.status === 200) {
                            console.log('Success: ', response?.status);
                            setErrMsg('Predict request successful');
                            setimagePredPreview(imageSrc);
                            setResponseSuccess(true);
                        } else {
                            console.log('Failed: ', response?.status);
                            setErrMsg('Predict request failed');
                            setResponseSuccess(true);
                        }

                    } catch (err) {
                        const error = err as AxiosError;
                        if (!error?.response) {
                            setErrMsg('No Server Response');
                        } else if (error.response?.status === 401) {
                            setErrMsg('Unauthorized');
                        } else {
                            setErrMsg('Failed');
                        }
                    }

                    // Get request for prediction response
                    // try {
                    //     const response =  await axios.get(GET_URL);
                    //     setGetResponseSuccess(true);
                    //     console.log("Get response: " + JSON.stringify(response?.data));
                    // } catch(err) {
                    //     const error = err as AxiosError;
                    //     console.log("Get Response Error: " + err)
                    // }

                }
                reader.readAsDataURL(fileLoaded);

        } catch (err) {
            setErrMsg('Erro ao processar a imagem');
        }
    }

    const handleTryAgain = (event: React.FormEvent) => {
        event?.preventDefault();
        setTryAgain(true);
        setResponseSuccess(false);
        setimagePredPreview(null);
        console.log('try again', tryAgain);
    }

    return (
        <div className="main-fileupload-container">
            <>
                {
                    fileUploaded && !tryAgain ? (
                        <div className="image-preview">
                            <p>{errMsg}</p>
                            {
                                imagePreview && !responseSuccess ? (
                                    <img 
                                        src={imagePreview} 
                                        alt="Preview" 
                                    />

                                ) : (
                                    <img 
                                        src={imagePredPreview || undefined} 
                                        alt="Preview" 
                                    />
                                )
                            }

                            <p>{fileName}</p>
                            <div>
                                { responseSuccess ? (
                                    <button className="secondary-button" onClick={handleTryAgain}>Try Again</button>
                                ) : (
                                    <button className="secondary-button" onClick={handlePredict}>Predict</button>
                                )}
                            </div>
                        </div>
    
                    ) :  (
                        <div className="input-file">
                            <input type="file" placeholder="File" onChange={handleFileChange} />
                        </div>
                    ) 
                }
            </>
        </div>
    )
};

export default FileUpload;