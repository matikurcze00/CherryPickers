import ErrorIcon from "@mui/icons-material/Error";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutline";
import HelpOutlineIcon from "@mui/icons-material/HelpOutline";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";

export const Property = (props) => {
  const Item = styled(Paper)(({ theme }) => ({
    backgroundColor: theme.palette.mode === "dark" ? "#1A2027" : "#fff",
    ...theme.typography.body2,
    padding: theme.spacing(1),
    textAlign: "center",
    color: theme.palette.text.secondary,
  }));

  return (
    <Item>
      {/* <Stack direction="row" marginTop='auto' marginBottom='auto'>
            {props.value === "incorrect" && <ErrorIcon />}
            {props.value === "valid" && <CheckCircleOutlineIcon />}
            {props.value === "modified" && <HelpOutlineIcon />}
            {props.name + " " + props.value}
      </Stack> */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          flexWrap: "wrap",
        }}
      >
        {props.value === "incorrect" && <ErrorIcon />}
        {props.value === "valid" && <CheckCircleOutlineIcon />}
        {props.value === "modified" && <HelpOutlineIcon />}
        <span style={{ marginLeft: 10 }}>{props.name + " " + props.value}</span>
      </div>
    </Item>
  );
};
