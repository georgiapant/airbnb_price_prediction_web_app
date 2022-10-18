// import React from 'react'
import axios from "axios";

export const makeModelsPost = async (postData) => {
  const res = await axios.post("/models", postData);
  const data = await res.data;

  return data;
};

export const getStats = async () => {
  const res = await axios("http://127.0.0.1:5000/api/v1.0/stats/");
  const data = await res.data;

  return data;
};
