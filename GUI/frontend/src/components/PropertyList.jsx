import Stack from "@mui/material/Stack";
import { Property } from "./Property";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";

export const PropertyList = (props) => {
  let properties = [
    { font: "modified" },
    { fontSize: "valid" },
    { images: "incorrect" },
  ];

  return (
    <Container maxWidth="sm" margin='5'>
      <Box margin='5'>
        <Stack spacing={1}>
          {properties.map((element, i) => {
            let name = Object.keys(element);
            return (
              <Property key={i} name={name} value={element[name]}></Property>
            );
          })}
        </Stack>
      </Box>
    </Container>
  );
};

export default PropertyList;
