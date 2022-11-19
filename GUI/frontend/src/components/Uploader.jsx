import "./css/Uploader.css";
import React, { useState } from "react";
import { FileUploader } from "react-drag-drop-files";

const fileTypes = ["PDF"];

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
        }}
      ></FileUploader>
    </div>
  );
}

export default Uploader;
