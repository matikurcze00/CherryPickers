import Button from "@mui/material/Button";
import Input from "@mui/material/Input";
import Card from "@mui/material/Card";
import "./css/FileUploader.css";

function FileUploader() {
  return (
    <Card>
      <Button variant="outlined">git</Button>
      <Input type="file"></Input>
    </Card>
  );
}

export default FileUploader;
