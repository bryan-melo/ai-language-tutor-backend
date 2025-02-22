import React, { useEffect, useState } from 'react';
import fetchMessage from './components/sample';

const App = () => {
    const [message, setMessage] = useState("");  // To store the fetched message

    useEffect(() => {
        const getMessage = async () => {
            const fetchedMessage = await fetchMessage();  // Fetch the message
            setMessage(fetchedMessage);  // Set the message state with the fetched data
        };

        getMessage();
    }, []);  // Empty dependency array means this runs once when the component mounts

    return (
        <div>
            <h1>FastAPI says:</h1>
            <p>{message}</p>  {/* Display the fetched message */}
        </div>
    );
};

export default App;