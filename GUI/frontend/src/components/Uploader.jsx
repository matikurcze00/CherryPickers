import "./css/Uploader.css";
import React, { useState } from "react";
import { FileUploader } from "react-drag-drop-files";

const fileTypes = ["PDF"];

function Uploader(props) {

  return (
    <div>
      <FileUploader
        multiple={true}
        maxSize={10}
        style={{ outerHeight: "1000px" }}
        types={fileTypes}
        handleChange={(file) => {
          props.files == undefined
            ? props.setFiles(file)
            : AddFiles(props.files, file, props.setFiles);
        }}
      ></FileUploader>
    </div>
  );
}

const AddFiles = (state, files, setFiles) => {
  let temp = [];
  if (files[1] !== undefined) {
    let i = 0;
    while (files[i] != undefined) {
      temp.push(files[i]);
      i++;
    }
    setFiles(state.concat(temp));
  } else {
    setFiles(state.concat(files[0]));
  }
};

export default Uploader;
