import { useState } from "react";
import Uploader from "./Uploader";
import "./css/VerificationPage.css";
import { Grid } from "@mui/material";
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

export const VerificationPage = () => {
  const [files, setFiles] = useState([]);
  const [pdfChanges, setPdfChanges] = useState([]);

  return (
    <Grid container>
    <Container maxWidth="sm">
      <Grid  item xs="12">
        <Box margin={5} width="500">
          <Uploader setFiles={setFiles} files={files}></Uploader>
        </Box>
        <Box>
          <Stack alignItems="center"
            divider={<Divider orientation="vertical" flexItem />}
            spacing={1}
          >
            {files.map((file) => { return <Item>{file.name}</Item>})}
          </Stack>
        </Box>
      </Grid>
    </Container>
    <Container >
      <Grid  xs="12" item margin={5}>
        <PropertyList>

        </PropertyList>
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
