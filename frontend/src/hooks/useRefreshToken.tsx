import axios from "axios"

const useRefreshToken = () => {

    const refresh = async () => {
        const response = await axios.get('http://localhost:5000/refresh', {
            withCredentials: true
        });
    }

    return (
        <div>  
        
        </div>
    )
}

export default useRefreshToken;
