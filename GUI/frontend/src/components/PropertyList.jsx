import Stack from "@mui/material/Stack";
import { Property } from "./Property";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";

export const PropertyList = (props) => {
  let properties = [
    { font: "valid" },
    { fontSize: "valid" },
    { images: "incorrect" },
  ];

  return (
    <Container maxWidth="sm" margin='5'>
      <Box margin='5'>
        <Stack spacing={1}>
            {Object.keys(props.properties).map((element, i) => {
            return (
              <Property key={i} name={element}></Property>
            );
          })}      
            {Object.keys(props.errors).map((element, i) => {
            return (
              <Property key={i} name={element}></Property>
            );
          })}
        </Stack>
      </Box>
    </Container>
  );
};

export default PropertyList;
