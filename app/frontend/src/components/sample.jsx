import React, { useEffect, useState } from "react";
import api from "../api.js"

const fetchMessage = async () => {
    try {
        const response = await api.get('/');
        return response.data.message;
    } catch (error) {
        console.error("Error fetching message", error);
        return "Error fetching message";
    }
};

export default fetchMessage;
