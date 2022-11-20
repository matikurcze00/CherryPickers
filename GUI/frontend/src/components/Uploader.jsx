import "./css/Uploader.css";
import React, { useState } from "react";
import { FileUploader } from "react-drag-drop-files";
// const axios = require('axios');
import axios, * as others from 'axios';
const fileTypes = ["PDF"];
axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';
const onUpload = (file) => {
  axios.post('http://localhost:3001/file', file)
    .then(function (response) {
    console.log(response);
  })
}

function Uploader(props) {
//   let files = [...props.files];
//   Array(files[0]).push(3);
//   console.log(files);
  return (
    <div>
      <FileUploader
        types={fileTypes}
        handleChange={(file) => {(props.files == undefined ? 
            props.setFiles(file) :
            props.setFiles(props.files.concat(file)));
            onUpload(file)
        }}
      ></FileUploader>
    </div>
  );
}

export default Uploader;
