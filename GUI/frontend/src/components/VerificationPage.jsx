import { useState } from "react";
import Uploader from "./Uploader";
import "./css/VerificationPage.css";
import { Button, Grid } from "@mui/material";
import {
  Container,
  Box,
  CssBaseline,
  Stack,
  Divider,
  ListItem,
} from "@mui/material";
import Paper from "@mui/material/Paper";
import { styled } from "@mui/material/styles";
import PropertyList from "./PropertyList.jsx";
import {AddFiles} from "./Uploader"

export const VerificationPage = () => {
  const [files, setFiles] = useState([]); //major data - uploaded and sent files
  const [pdfChanges, setPdfChanges] = useState([]); //comments to changes done in backend
  const [loggedIn, setLoggedIn] = useState(); //login flag (0 not logged, 1 simple user, 2 admin)
  const [statuses, setStatuses] = useState(); //statuses of files uploaded
  const [recents, setRecents] = useState(); //recents consisted of data saved and downloaded from api and deleted session files

  const deleteFile = (e) => {
    AddFiles(recents, files[e.target.id], setRecents);
    setFiles(files.filter((element) => element !== files[e.target.id]));
  };

  return (
    <Grid container>
      <Container maxWidth="sm">
        <Grid item>
          <Box margin={5} width="500">
            <Uploader setFiles={setFiles} files={files}></Uploader>
          </Box>
          <Box>
            <Stack
              alignItems="center"
              divider={<Divider orientation="vertical" flexItem />}
              spacing={1}
            >
              {files.map((file) => {
                return (
                  <Item>
                    {file.name}
                    <Button
                      color="error"
                      key={files.findIndex((x) => x === file)}
                      id={files.findIndex((x) => x === file)}
                      onClick={(e) => deleteFile(e)}
                      variant="outlined"
                    >
                      Delete
                    </Button>
                  </Item>
                );
              })}
            </Stack>
          </Box>
        </Grid>
      </Container>
      <Container>
        <Grid item margin={5}>
          <PropertyList></PropertyList>
        </Grid>
      </Container>
    </Grid>
  );
};

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === "dark" ? "#1A2027" : "#fff",
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: "center",
  color: theme.palette.text.secondary,
}));

export default VerificationPage;
