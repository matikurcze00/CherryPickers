import "./css/Uploader.css";
import React, { useState } from "react";
import { FileUploader } from "react-drag-drop-files";
import axios, * as others from "axios";

const fileTypes = [
  "PDF",
  "ZIP",
  "TXT",
  "RTF",
  "XPS",
  "ODT",
  "ODS",
  "ODP",
  "DOC",
  "XLS",
  "PPT",
  "DOCX",
  "XLSX",
  "PPTX",
  "CSV",
  "JPG",
  "TIF",
  "GEOTIF",
  "PNG",
  "SVG",
  "WAV",
  "MP3",
  "AVI",
  "MPG",
  "MP4",
  "OGG",
  "OGV",
  "TAR",
  "GZ",
  "7Z",
  "HTML",
  "XHTML",
  "CSS",
  "XML",
  "XSD",
  "GML",
  "RNG",
  "XSL",
  "XSLT",
  "TSL",
  "XMLsig",
  "XADES",
  "PADEES",
  "CADES",
  "ASIC",
  "XMLENC",
];
axios.defaults.headers.post["Access-Control-Allow-Origin"] = "*";

const onUpload = (file, onSetProperties, onSetErrors) => {
  const formData = new FormData();
  formData.append("file", file);
  axios.post("http://127.0.0.1:5000/file", formData).then(function (response) {
    onSetProperties(response.data.parse_data);
    onSetErrors(response.data.errors);
  }).catch(function (response) {
    onSetErrors({})
    onSetProperties({})
  })
};



function Uploader(props) {
  
  return (
    <div>
      <FileUploader
        multiple={true}
        maxSize={10}
        style={{ outerHeight: "1000px" }}
        types={fileTypes}
        handleChange={(file) => {
            AddFiles(props.files, file, props.setFiles, props.onSetProperties, props.onSetErrors);
        }}
      ></FileUploader>
    </div>
  );
}

export const AddFiles = (state, files, setFiles, onSetProperties, onSetErrors) => {
  let temp = [];
  console.log(state);
  console.log(files);

  if(state === undefined)
    setFiles(files);
  else if (files[1] !== undefined) {
    let i = 0;
    while (files[i] != undefined) {
      temp.push(files[i]);
      onUpload(files[i], onSetProperties, onSetErrors)
      i++;
    }
    setFiles(state.concat(temp));
  } else {
    onUpload(files[0], onSetProperties, onSetErrors)
    setFiles(state.concat(files[0]));
  }
};

export const AddFiles2 = (state, files, setFiles) => {
    let temp = [];
  
    if(state === undefined)
      setFiles(files);
    else if (files[1] !== undefined) {
      console.log("here");
      let i = 0;
      while (files[i] != undefined) {
        temp.push(files[i]);
        i++;
      }
      setFiles(state.concat(temp));
    } else {
      console.log("there");
      setFiles(state.concat(files));
    }
  };

export default Uploader;
